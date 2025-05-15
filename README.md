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
