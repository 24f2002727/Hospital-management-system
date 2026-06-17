# Hospital Management System

A full-stack Hospital Management System built using Flask and SQLAlchemy that provides role-based access for Admin, Doctor, and Patient users. The application streamlines hospital operations including appointment scheduling, doctor availability management, patient records, and treatment history.

## Key Features

Admin Module

* Manage doctors, patients, and departments
* Search doctors and patients using SQLAlchemy filters
* View and monitor all appointments
* Activate, block, or remove users
* Dashboard statistics for doctors, patients, departments, and appointments

Doctor Module

* Manage weekly availability schedules
* View upcoming and past appointments
* Access patient history
* Create and update treatment records
* Mark appointments as completed or cancelled

Patient Module

* Search doctors by name, specialization, or department
* View doctor profiles and availability schedules
* Book appointments based on available time slots
* Cancel appointments
* Access treatment history and medical records

## Technologies Used
- **Framework**: Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5, Jinja2
- **Authentication**: werkzeug for password hashing
- **Backend**: Python 3

## Highlights

* Implemented Role-Based Access Control (RBAC) for Admin, Doctor, and Patient users.
* Developed appointment scheduling with real-time doctor availability management.
* Built secure authentication using password hashing and session management.
* Designed and managed a relational database using SQLAlchemy ORM.
* Implemented search functionality with SQLAlchemy filters and dynamic Jinja2 rendering.
* Added appointment tracking, treatment management, and patient history features.

## Project Structure

Hospital-Management-System/
│
├── app.py
├── models.py
├── requirements.txt
├── hms.db
├── static/
│   ├── style.css
│   └── register_button.css
│
├── templates/
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── admin_dashboard.html
│   ├── doctor_dashboard.html
│   ├── patient_dashboard.html
│   └── ...
│
└── screenshots/

## Screenshots

- Home Page
- Admin Dashboard
- Doctor Dashboard
- Patient Dashboard
- Appointment Booking Interface


## Run Locally

```bash
git clone <repository-url>
cd Hospital-management-system
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open `http://localhost:5000` in the browser.

## Default Admin Login

A default admin account is automatically created during the first application startup. Configure credentials in `create_admin()` before deployment.


## Notes

This project is suitable for demonstrating full-stack Flask development, user roles, and hospital workflow management.

### Admin Routes
- `/admin_dashboard` - Admin dashboard
- `/admin_search` - Search patients/doctors
- `/create_doctor` - Create doctor
- `/edit_doctor/<id>` - Edit doctor
- `/delete_doctor/<id>` - Remove doctor
- `/create_department` - Create department
- `/edit_department/<id>` - Edit department

### Doctor Routes
- `/doctor_dashboard` - Doctor dashboard
- `/update_availability` - Set availability schedule
- `/doctor_patient_history/<id>` - View patient history
- `/create_treatment/<id>` - Add treatment notes

### Patient Routes
- `/patient_dashboard` - Patient dashboard
- `/search_doctors` - Find doctors
- `/doctor_profile/<id>` - View doctor profile
- `/create_appointment` - Book appointment
- `/patient_treatment_history` - View medical records
- `/edit_patient/<id>` - Edit profile

## Security Features
- Password hashing with werkzeug
- Role-based access control
- Login required decorators on protected routes
- Session management
- Account status tracking (active/blocked/removed)

## Customization

### Modify Admin Credentials
Edit `create_admin()` function in `app.py`:
```python
admin = Admin(
    username="your_username",
    email="your_email@gmail.com",
    contact="your_contact",
    password=generate_password_hash("your_password", method="pbkdf2:sha256"),
)
```

### Styling
CSS files are located in `/static/` directory:
- `style.css` - Main stylesheet
- `register_button.css` - Registration page styling

## Troubleshooting

### Database Issues
If you encounter database errors, delete `hms.db` and run `python app.py` again.

### Import Errors
Ensure all dependencies are installed: `pip install -r requirements.txt`

### Port Already in Use
Change the port in `app.py`: `app.run(debug=True, port=5001)`

## Future Enhancements
- Email notifications for appointments
- SMS alerts
- Online payment integration
- Prescription management system
- Analytics and reporting dashboard
- Multi-location support
- Video consultation feature

## Learning Outcomes

This project helped in gaining practical experience with:

* Flask web development
* SQLAlchemy ORM
* Database design and migrations
* Authentication and authorization
* RESTful routing
* Jinja2 templating
* Session management
* Full-stack application development

## License

This project is developed for educational and learning purposes.