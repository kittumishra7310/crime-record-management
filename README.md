Crime Record Management System

A web-based application for managing crime records, built with Flask and MongoDB. It enables authorized users (Admins and Officers) to add, view, update, and delete crime records, featuring secure user authentication, role-based access control, and evidence image uploads. The application offers a responsive Bootstrap-based UI with real-time filtering of records.
Features

User Authentication: Secure login/signup with Flask-Login and password hashing via Flask-Bcrypt.
Role-Based Access Control:
Admin: Add, view, update, and delete crime records.
Officer: Add, view, and update crime records.
User: View crime records.


Crime Record Management:
Add records with Case ID, Crime Type, Date, Location, Description, Status, Suspect, and optional evidence image.
View records with AJAX-powered filters (Case ID, Crime Type, Status, Location, Date Range).
Update records, including replacing evidence images.
Delete records (Admin only).


Image Uploads: Supports PNG, JPG, JPEG, GIF (max 5MB), stored in static/uploads with paths in MongoDB.
Responsive UI: Bootstrap 5.3.3 with gradient backgrounds, dark/light theme toggle, and animations.
MongoDB Integration: Efficient storage and querying of user and crime data.

Screenshots



View Crimes
Add Crime







Note: Add screenshots to the screenshots/ folder and update paths above after capturing them.
Tech Stack

Backend: Flask 3.0.3, Python 3.12
Database: MongoDB 4.0+
Authentication: Flask-Login 0.6.3, Flask-Bcrypt 1.0.1
Frontend: Bootstrap 5.3.3, HTML, CSS, JavaScript
Dependencies: pymongo 4.8.0, Werkzeug 3.0.4

Prerequisites

Python: 3.12
MongoDB: 4.0 or higher
pip: For installing dependencies
Git: To clone the repository
mongosh: For MongoDB interaction (optional)

Setup Instructions

Clone the Repository:
git clone https://github.com/kittumishra7310/crime-record-management.git
cd crime-record-management


Create a Virtual Environment (recommended):
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate


Install Dependencies:
pip install -r requirements.txt

Or manually:
pip install flask==3.0.3 pymongo==4.8.0 flask-login==0.6.3 flask-bcrypt==1.0.1


Set Up MongoDB:

Install MongoDB: MongoDB Installation Guide
Start the server:mongod


Verify port (localhost:27017):lsof -iTCP -sTCP:LISTEN | grep mongod


If different (e.g., 27018), update app.py:client = MongoClient('mongodb://localhost:27018/')






Create Uploads Directory:
mkdir -p static/uploads
chmod -R 755 static/uploads


Run the Application:
python app.py


Access at http://localhost:5000.



Project Structure
crime-record-management/
├── screenshots/            # Store screenshots for README
├── static/
│   ├── uploads/            # Evidence images
├── templates/
│   ├── add_crime.html      # Add crime record form
│   ├── update_crime.html   # Update crime record form
│   ├── view_crimes.html    # View and filter crime records
│   ├── index.html          # Homepage
│   ├── login.html          # Login page
│   ├── signup.html         # Signup page
├── .gitignore              # Git ignore file
├── app.py                  # Main Flask application
├── requirements.txt        # Dependencies
└── README.md               # Documentation

Usage

Access the App:

Open http://localhost:5000.


Signup:

Navigate to /signup.
Create an account (e.g., Username: testadmin, Password: password123, Role: admin).


Login:

Go to /login with your credentials.


Add a Crime Record:

Go to /add (Admin/Officer only).
Enter details (e.g., Case ID: 105, Crime Type: Theft, Date: 2025-05-15, Location: Shop, Description: Test theft, Status: Open, Suspect: Jane Doe).
Upload an image (PNG, JPG, JPEG, GIF; <5MB).
Submit.


View Crime Records:

Go to /view.
Filter by Case ID, Crime Type, Status, Location, or Date Range.
View images in the “Image” column.


Update a Crime Record:

In /view, click “Edit” (Admin/Officer only).
Modify fields or upload a new image.
Submit.


Delete a Crime Record:

In /view, click “Delete” (Admin only).
Confirm deletion.


Verify in MongoDB:

Connect:mongosh


Check:use crimeDB
db.crimes.find().pretty()





Example MongoDB Record
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

Deployment
To deploy to a production environment (e.g., Heroku, Render, or AWS):

Set Environment Variables:

FLASK_SECRET_KEY: Replace "supersecretkey" in app.py.
MONGODB_URI: Use a cloud MongoDB (e.g., MongoDB Atlas).
Example:export FLASK_SECRET_KEY="your-secret-key"
export MONGODB_URI="mongodb+srv://user:pass@cluster0.mongodb.net/crimeDB"




Use a WSGI Server:

Install Gunicorn:pip install gunicorn


Run:gunicorn -w 4 app:app




Cloud Storage:

Replace static/uploads with AWS S3 or Cloudinary for images.
Update app.py to use an S3 client (e.g., boto3).


Sample Heroku Deployment:
heroku create
heroku addons:create mongolab
git push heroku main
heroku open



Troubleshooting

MongoDB Connection:

Ensure MongoDB runs:mongod


Check logs:cat /usr/local/var/log/mongodb/mongo.log


Create data directory:sudo mkdir -p /data/db
sudo chown $(whoami) /data/db




Image Upload Issues:

Verify static/uploads permissions:chmod -R 755 static/uploads


Check file type/size.


Images Not Displaying:

Verify image_path:db.crimes.find().pretty()


Check browser console (F12 → Console) for 404s.
Confirm:ls static/uploads/




No Data in /view:

Check collection:db.crimes.countDocuments()


Insert test record:db.crimes.insertOne({
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





Security Notes

File Uploads: Server-side validation for PNG, JPG, JPEG, GIF. Add image content validation (e.g., PIL) for production.
Passwords: Hashed with Flask-Bcrypt.
Production:
Use environment variables for sensitive data.
Deploy with Gunicorn/Nginx.
Enable HTTPS.
Use cloud storage for images.



Contributing

Fork the repository.
Create a branch:git checkout -b feature-name


Commit:git commit -m "Add feature-name"


Push:git push origin feature-name


Open a Pull Request.

License
Licensed under the MIT License. See LICENSE for details.
Contact
Open issues at GitHub Issues or contact kittumishra7310.

Built by 
