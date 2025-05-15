from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Folder for image uploads
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB file size limit
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# MongoDB connection
try:
    client = MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=5000)
    client.admin.command('ping')
    print("MongoDB connection successful")
except Exception as e:
    print(f"MongoDB connection failed: {e}")
    exit(1)

db = client['crimeDB']
crimes = db['crimes']
users = db['users']

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
bcrypt = Bcrypt(app)

# Ensure uploads folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class User(UserMixin):
    def __init__(self, user_id, username, role):
        self.id = str(user_id)
        self.username = username
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    user = users.find_one({'_id': ObjectId(user_id)})
    if user:
        return User(user['_id'], user['username'], user['role'])
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users.find_one({'username': username})
        if user and bcrypt.check_password_hash(user['password'], password):
            login_user(User(user['_id'], user['username'], user['role']))
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        flash('Invalid username or password.', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        if users.find_one({'username': username}):
            flash('Username already exists!', 'danger')
            return redirect(url_for('signup'))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        users.insert_one({
            'username': username,
            'password': hashed_password,
            'role': role
        })
        flash('Account created successfully! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_crime():
    if current_user.role not in ['admin', 'officer']:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('index'))
    if request.method == 'POST':
        case_id = request.form['case_id']
        crime_type = request.form['crime_type']
        date = request.form['date']
        location = request.form['location']
        description = request.form['description']
        status = request.form['status']
        suspect = request.form.get('suspect', '')
        
        # Check for duplicate case_id
        if crimes.find_one({'case_id': case_id}):
            flash('Case ID already exists!', 'danger')
            return redirect(url_for('add_crime'))
        
        # Handle image upload
        image_path = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file.filename != '':
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    try:
                        file.save(file_path)
                        image_path = f'uploads/{filename}'
                    except Exception as e:
                        flash(f'Error uploading image: {e}', 'danger')
                        return redirect(url_for('add_crime'))
                else:
                    flash('Invalid file type. Allowed types: png, jpg, jpeg, gif', 'danger')
                    return redirect(url_for('add_crime'))
        
        crime_data = {
            'case_id': case_id,
            'crime_type': crime_type,
            'date': datetime.strptime(date, '%Y-%m-%d'),
            'location': location,
            'description': description,
            'status': status,
            'suspect': suspect,
            'created_by': current_user.username,
            'image_path': image_path
        }
        try:
            crimes.insert_one(crime_data)
            flash('Crime record added successfully!', 'success')
            return redirect(url_for('view_crimes'))
        except Exception as e:
            flash(f'Error adding crime: {e}', 'danger')
            return redirect(url_for('add_crime'))
    
    return render_template('add_crime.html')

@app.route('/view', methods=['GET', 'POST'])
@login_required
def view_crimes():
    if request.method == 'POST':  # AJAX request
        data = request.get_json()
        search_query = data.get('search', '')
        crime_type = data.get('crime_type', '')
        status = data.get('status', '')
        start_date = data.get('start_date', '')
        end_date = data.get('end_date', '')
        location = data.get('location', '')
        
        query = {}
        if search_query:
            query['$or'] = [
                {'case_id': {'$regex': search_query, '$options': 'i'}},
                {'description': {'$regex': search_query, '$options': 'i'}},
                {'suspect': {'$regex': search_query, '$options': 'i'}}
            ]
        if crime_type:
            query['crime_type'] = crime_type
        if status:
            query['status'] = status
        if location:
            query['location'] = {'$regex': location, '$options': 'i'}
        if start_date or end_date:
            query['date'] = {}
            if start_date:
                query['date']['$gte'] = datetime.strptime(start_date, '%Y-%m-%d')
            if end_date:
                query['date']['$lte'] = datetime.strptime(end_date, '%Y-%m-%d')
        
        crime_list = list(crimes.find(query).sort('date', -1))
        for crime in crime_list:
            crime['_id'] = str(crime['_id'])
            crime['date'] = crime['date'].strftime('%Y-%m-%d')
        return jsonify({'crimes': crime_list})
    
    crime_list = list(crimes.find().sort('date', -1))
    for crime in crime_list:
        crime['_id'] = str(crime['_id'])
        crime['date'] = crime['date'].strftime('%Y-%m-%d')
    return render_template('view_crimes.html', crimes=crime_list)

@app.route('/update/<case_id>', methods=['GET', 'POST'])
@login_required
def update_crime(case_id):
    if current_user.role not in ['admin', 'officer']:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('view_crimes'))
    crime = crimes.find_one({'case_id': case_id})
    if not crime:
        flash('Crime not found!', 'danger')
        return redirect(url_for('view_crimes'))
    # Format date for form input
    crime['date'] = crime['date'].strftime('%Y-%m-%d')
    crime['_id'] = str(crime['_id'])
    if request.method == 'POST':
        updated_data = {
            'case_id': request.form['case_id'],
            'crime_type': request.form['crime_type'],
            'date': datetime.strptime(request.form['date'], '%Y-%m-%d'),
            'location': request.form['location'],
            'description': request.form['description'],
            'status': request.form['status'],
            'suspect': request.form.get('suspect', ''),
            'updated_by': current_user.username
        }
        # Handle image upload for update
        if 'photo' in request.files:
            file = request.files['photo']
            if file.filename != '':
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    try:
                        file.save(file_path)
                        updated_data['image_path'] = f'uploads/{filename}'
                    except Exception as e:
                        flash(f'Error uploading image: {e}', 'danger')
                        return redirect(url_for('update_crime', case_id=case_id))
                else:
                    flash('Invalid file type. Allowed types: png, jpg, jpeg, gif', 'danger')
                    return redirect(url_for('update_crime', case_id=case_id))
        else:
            # Preserve existing image_path if no new file is uploaded
            updated_data['image_path'] = crime.get('image_path')
        
        if crimes.find_one({'case_id': updated_data['case_id'], '_id': {'$ne': ObjectId(crime['_id'])}}):
            flash('Case ID already exists!', 'danger')
            return redirect(url_for('update_crime', case_id=case_id))
        crimes.update_one({'_id': ObjectId(crime['_id'])}, {'$set': updated_data})
        flash('Crime record updated successfully!', 'success')
        return redirect(url_for('view_crimes'))
    return render_template('update_crime.html', crime=crime)

@app.route('/delete/<case_id>')
@login_required
def delete_crime(case_id):
    if current_user.role not in ['admin']:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('view_crimes'))
    crime = crimes.find_one({'case_id': case_id})
    if crime:
        crimes.delete_one({'_id': crime['_id']})
        flash('Crime record deleted successfully!', 'success')
    else:
        flash('Crime not found!', 'danger')
    return redirect(url_for('view_crimes'))

if __name__ == '__main__':
    app.run(debug=True)