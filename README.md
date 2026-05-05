# Hospital Management System (HMS)

A comprehensive Flask-based Hospital Management System with role-based access control for Admins, Doctors, and Patients.

## Features

### 🔐 User Management & Authentication
- Role-based login (Admin, Doctor, Patient)
- Patient self-registration
- Admin pre-created (no registration allowed)
- Doctor account creation only by admin
- Account blocking and removal capabilities

### 👨‍💼 Admin Functionalities
- **Dashboard**: View statistics (total doctors, patients, departments, appointments)
- **Doctor Management**:
  - Create new doctor profiles with name, specialization, email, contact
  - Edit doctor details (name, specialization, department, availability status)
  - Remove/Block doctors from the system
  - Search doctors by name or specialization
  
- **Patient Management**:
  - View all patient profiles
  - Edit patient information
  - Search patients by name, email, or contact information
  - Remove/Block patients from the system
  
- **Department Management**:
  - Create new departments
  - Edit department details (name, description, location)
  - Delete departments
  
- **Appointment Management**:
  - View all upcoming and past appointments
  - Track appointment status (pending, completed, cancelled)
  - Advanced search functionality

### 👨‍⚕️ Doctor Functionalities
- **Dashboard**: 
  - View upcoming appointments for the week
  - See all assigned patients
  - Track completed appointments statistics
  
- **Appointment Management**:
  - View upcoming appointments with patient details
  - Mark appointments as completed or cancelled
  - View full appointment history
  
- **Availability Management**:
  - Set general availability message
  - Create 7-day availability schedule with specific time slots
  - Enable/disable availability for each day
  - Manage time slots for each available day
  
- **Patient Management**:
  - View list of assigned patients
  - View complete patient history and previous treatments
  - Access patient medical records
  
- **Treatment Records**:
  - Add diagnosis, prescription, and notes for completed appointments
  - View patient treatment history for informed consultation

### 👥 Patient Functionalities
- **Dashboard**:
  - View available doctors and specializations
  - See upcoming and past appointments
  - Access medical records and treatment history
  - Statistics on appointments and medical records
  
- **Doctor Discovery**:
  - Search doctors by name, specialization, or department
  - View doctor profiles with qualifications
  - See doctor's 7-day availability schedule
  - Browse by specialization categories
  
- **Appointment Management**:
  - Book appointments with available doctors
  - Select from available time slots based on doctor's schedule
  - Specify reason for visit
  - Cancel upcoming appointments
  - View appointment status (pending, completed, cancelled)
  
- **Medical Records**:
  - View complete treatment history with diagnosis and prescriptions
  - Access doctor's notes for each appointment
  - Track health records over time
  
- **Profile Management**:
  - Edit personal information (name, email, contact, DOB, address)
  - Manage account details

### 🔧 Core System Features
- **Double-Booking Prevention**: Prevents multiple appointments at the same date and time for the same doctor
- **Dynamic Appointment Status**: Track appointments through status flow (Pending → Completed/Cancelled)
- **7-Day Doctor Availability**: Doctors set availability for the next 7 days with specific time slots
- **Treatment Records**: Store diagnosis, prescriptions, and doctor notes for each appointment
- **Search & Filter**: Advanced search for doctors, patients, departments, and specializations
- **Role-Based Access Control**: Secure role-based routes and operations

## Installation & Setup

### Prerequisites
- Python 3.8+
- Flask
- SQLAlchemy
- SQLite (included with Python)

### Installation Steps

1. **Clone the repository**:
```bash
git clone <repository-url>
cd Hospital-management-system
```

2. **Create a virtual environment** (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install flask flask-sqlalchemy
```

4. **Initialize the database**:
```bash
python app.py
```

The database will be created automatically, and a default admin account will be created with:
- **Username**: admin
- **Password**: 123456
- **Email**: shivam@gmail.com

## Running the Application

```bash
python app.py
```

The application will run on `http://localhost:5000`

## User Access

### Admin Account (Pre-created)
- **Username**: admin
- **Password**: 123456
- **Access**: Full system access, create/edit doctors, manage departments and patients

### Creating Doctors
1. Login as Admin
2. Navigate to Admin Dashboard
3. Click "Create Doctor"
4. Fill in all details (name, username, password, email, contact, specialization, department)
5. Doctor can now login with created credentials

### Patient Registration
1. Click "Register" on home page
2. Fill in registration form (name, email, contact, username, password)
3. Login with credentials
4. Access patient dashboard

## Database Schema

### Tables

**Admin**
- id, username, password, email, contact, name, role

**Doctor**
- id, name, username, password, email, contact, specialization, dept_id, availability, status, role, admin_id

**Patient**
- id, name, username, password, email, contact, date_of_birth, address, status, role

**Department**
- id, name, description, building, status, admin_id

**Appointment**
- id, date, time, reason, patient_id, doctor_id, status, schedule

**Treatment**
- id, diagnosis, prescription, notes, created_at, appt_id

**DoctorAvailability**
- id, doctor_id, date, time_slots, is_available, created_at, updated_at

**Schedule_doctors**
- id, doctor_name, doctor_availability, doct_id

## Key Routes

### Authentication
- `/` - Home page
- `/register` - Patient registration
- `/login` - User login
- `/logout` - User logout

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

## Technologies Used
- **Framework**: Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5, Jinja2
- **Authentication**: werkzeug for password hashing
- **Backend**: Python 3

## License
This project is for educational purposes.
Table creation showing the list of all the present doctors --> with edit, blacklist and delete button --> on admin dashboard.
Using jinja2, all the details of doctors are shown on admin dashboard inside the table.
Table creation showing the list of all the present patients --> with edit, blacklist and delete button --> on admin dashboard.
Using jinja2, all the details of patients are shown on admin dashboard inside the table.
Create a HTML page --> for editing the doctor profile --> done by admin.
Create a route for editing the doctor profile HTML page --> to render the HTML page.
Create a HTML page --> for editing the patient profile --> done by admin.
Create a route for editing the patient profile HTML page --> to render the HTML page.
Create a route for deleting the doctor profile --> done by admin.
Create a route for deleting the patient profile --> done by admin.
Create a route for blacklisting the doctor profile --> done by admin.
Create a route for blacklisting the patient profile --> done by admin.
Once done, commit all the changes done till now.
After cross reviewing your task with me, then only you will push your codes on github repository.
Create a Search bar on admin dashboard --> to search the doctor and patient by name.
Create a route for searching the doctor and patient by name --> to render the HTML page with searched details.
Once done, commit all the changes done till now.
After cross reviewing your task with me, then only you will push your codes on github repository.

Day-4
Search functionality is done using SQLAlchemy filter function --> search route made, done by admin, to search doctors and patients by name.
Search route mentioned inside admin_dashboard.html page as well.
Show all the departments created by admin --> inside Patient dashboard using jinja2 --> with button to view doctors inside that department.
Each department should have a button --> to view all the doctors present in that department --> inside Patient dashboard.
Create a route --> to show all the doctors present in that department --> inside Patient dashboard.
Give the route link inside patient_dashboard.html page as well.
Search bar on Patient dashboard --> to search the doctor by name.
Create a route for searching the doctor by name --> shown on patient dashboard..
Doctor table should have a column of "Available" --> to show the availability status of the doctor --> inside models.py file as well.
Create a route --> to update the availability status of the doctor --> done by doctor himself.
Create a button on doctor dashboard --> to redirect to update availability status page.
Create a HTML page --> for updating the availability status of the doctor --> done by doctor himself.
Once done, commit all the changes done till now.
Patient Dashboard --> when a particular department view details button clicked --> show all doctors inside that department using jinja2.
On patient dashboard --> when list of doctor of particular department is shown --> create a button to show availability of that doctor.
Create a route --> to show availability of that doctor --> on patient dashboard.
Create a HTML page --> to show availability of that doctor --> on patient dashboard.
Once done, commit all the changes done till now.
when checking each doctors availability --> show all the mentioned available dates of that doctor --> give a select option, which patient can select any one date from the available dates --> and give a button book appointment to confirm and save that booking into appointment table.
Create a route --> to book the appointment of that doctor on selected date --> on patient dashboard.
once appointment is booked, show that appointment details on patient dashboard as well.
Create a HTML page --> to show all the appointments booked by that patient --> on patient dashboard.
Create a button on patient dashboard --> to cancel the booked appointement.
Create a route --> to cancel the booked appointement --> on patient dashboard.
Once done, commit all the changes done till now.
show that booked appointment to that particular doctor --> on doctor dashboard in a table format with 2 button, completed and cancel.
Create a route --> to mark that appointment as completed --> on doctor dashboard.
Create a route --> to cancel that appointment --> on doctor dashboard.
Once done, commit all the changes done till now.
show all the appointments table data on the admin dashboard as well.
give a check route that whatever date of doctor is booked is not shown again in the availability of that doctor to other patients.
Once done, commit all the changes done till now.
On admin dashboard --> show total number of doctors, patients and appointments using SQLAlchemy count function.
After cross reviewing your task with me, then only you will push your codes on github repository.