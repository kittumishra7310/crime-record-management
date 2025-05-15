# Crime Record Management System

A web-based application for managing crime records, built with **Flask** and **MongoDB**. It enables authorized users (Admins and Officers) to add, view, update, and delete crime records, featuring secure user authentication, role-based access control, and evidence image uploads. The application offers a responsive **Bootstrap**-based UI with real-time filtering of records.

---

## 🚀 Features

### 🔐 User Authentication
- Secure login/signup with **Flask-Login**
- Password hashing using **Flask-Bcrypt**

### 👤 Role-Based Access Control
- **Admin**: Add, view, update, and delete crime records.
- **Officer**: Add, view, and update crime records.
- **User**: View crime records.

### 📝 Crime Record Management
- Add records with:
  - Case ID, Crime Type, Date, Location, Description, Status, Suspect, and optional evidence image
- View with AJAX filters:
  - Case ID, Crime Type, Status, Location, Date Range
- Update records (including image replacement)
- Delete records (Admin only)

### 🖼️ Image Uploads
- Formats: PNG, JPG, JPEG, GIF (max 5MB)
- Stored in `static/uploads/` with paths saved in MongoDB

### 💻 Responsive UI
- **Bootstrap 5.3.3**
- Gradient backgrounds, dark/light theme toggle, animations

### 💾 MongoDB Integration
- Efficient storage and querying of user and crime data

---

## 📸 Screenshots

> Add screenshots in the `screenshots/` folder and update this section with image paths.

- View Crimes  
- Add Crime  

---

## 🛠️ Tech Stack

- **Backend**: Flask 3.0.3, Python 3.12
- **Database**: MongoDB 4.0+
- **Authentication**: Flask-Login 0.6.3, Flask-Bcrypt 1.0.1
- **Frontend**: Bootstrap 5.3.3, HTML, CSS, JavaScript
- **Dependencies**: pymongo 4.8.0, Werkzeug 3.0.4

---

## 📋 Prerequisites

- Python 3.12
- MongoDB 4.0+
- pip
- Git
- mongosh (optional)

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/kittumishra7310/crime-record-management.git
cd crime-record-management
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
Or Manually:
```bash
pip install flask==3.0.3 pymongo==4.8.0 flask-login==0.6.3 flask-bcrypt==1.0.1
```

### 4. Set up MongoDB
- Install MongoDB
- Start server:
```bash
mongod
```
- verify port:
```bash
lsof -iTCP -sTCP:LISTEN | grep mongod
```
- If using a different port (e.g., 27018), update in app.py:
```bash
client = MongoClient('mongodb://localhost:27018/')
```

### 5. Create Uploads Directory

```bash
mkdir -p static/uploads
chmod -R 755 static/uploads
```

### 6. Run the Application
```bash
python app.py
```
Open in browser: http://localhost:5000

## 📁 Project Structure
```php
crime-record-management/
├── screenshots/            # Store screenshots for README
├── static/
│   ├── uploads/            # Evidence images
├── templates/
│   ├── add_crime.html
│   ├── update_crime.html
│   ├── view_crimes.html
│   ├── index.html
│   ├── login.html
│   ├── signup.html
├── .gitignore
├── app.py
├── requirements.txt
└── README.md
```

## 🔧 Usage
### 1. Access the App
Open: http://localhost:5000

### 2. Signup
- Navigate to /signup
- Create an account
  Example: testadmin/password123, role: admin

### 3. Login
- Go to /login and login with your credentials

### 4. Add a Crime Record (Admin/Officer)
- Go to /add
- Fill in:
  - Case ID, Crime Type, Date, Location
  - Description, Status, Suspect
  - Upload Image (< 5MB)
- Sumbmit

### 5. View Crime Records
- Navigate to /view
- Use filters
- View image in "image" column

### 6. Update a Crime Record (Admin/Officer)
- Click "Edit" in /view
- Modify fields or uplaod a new image
- Submit

### 7. Delete a Crime Record (Admin only)
- Click "Delete"
- Confirm

## 🧪 Verify in MongoDB
```bash
mongosh
```
```javascript
use CrimeDB
db.crimes.find().pretty()
```

## 🧾 Example MongoDB Record

```json
{
  "_id": ObjectId("..."),
  "case_id": "105",
  "crime_type": "Theft",
  "date": ISODate("2025-05-15T00:00:00Z"),
  "location": "Shop",
  "description": "Test theft",
  "status": "Open",
  "suspect": "Jane Doe",
  "created_by": "testadmin",
  "image_path": "uploads/test.jpg"
}
```

## 🌍 Deployment

### 1. Set Environment Variables
```bash
export FLASK_SECRET_KEY="your-secret-key"
export MONGODB_URI="mongodb+srv://user:pass@cluster0.mongodb.net/crimeDB"
```

## 2. Use WSGI Server (Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 app:app
```

## 3. Cloud Storage for Images
- Replace static/uploads with AWS S3 or Cloudinary
- Use boto3 or Cloudinary's Python SDK

## 4. Deploy to Heroku (Example)
```bash
heroku create
heroku addons:create mongolab
git push heroku main
heroku open
```

## 🛠️ Troubleshooting

### MongoDB Not Connecting
```bash
mongod
cat /usr/local/var/log/mongodb/mongo.log
sudo mkdir -p /data/db
sudo chown $(whoami) /data/db
```
### Image Upload Issues
- Check permissions
```bash
chmod -R 755 static/uploads
```

- validate file type/size

### Image Not Displaying
- Verify image path in MongoDB
- Check browser console
- Confirm:
```bash
ls static/uploads/
```

### No Data in /view
```javascript
db.crimes.countDocuments()

db.crimes.insertOne({
  case_id: "105",
  crime_type": "Theft",
  date: ISODate("2025-05-15"),
  location: "Shop",
  description: "Test theft",
  status: "Open",
  suspect: "Jane Doe",
  created_by: "testadmin",
  image_path: "uploads/test.jpg"
})
```

## 🔐 Security Notes
- File Uploads: Validate file type/size. Use image content check (PIL) in production.
- Passwords: Securely hashed via Flask-Bcrypt.
- Production Tips:
  - Use environment variables
  - Use Gunicorn + Nginx
  - Enable HTTPS
  - Use cloud storage for images

## 🤝 Contributing
1. Fork the repo
2. Create a new branch:
```bash
git checkout -b feature-name
```
3. Commit your changes
```bash
git commit -m "Add feature-name"
```
4. Push and open a PR
```bash
git push origin feature-name
```

## 📜 License
Licensed under the MIT License. See LICENSE for details.
