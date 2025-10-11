from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    role = db.Column(db.String(20), default="admin", nullable=False)
    # One Admin can create many doctors
    doctors = db.relationship('Doctor', backref='created_by', lazy=True)
    ## One Admin can create many dept
    depts = db.relationship('Department', backref='created_by', lazy=True)


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # created by admin
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    #link to department
    dept_id=db.Column(db.Integer,db.ForeignKey('department.id'))
    # NEW: status field -> active / blocked / deleted
    status = db.Column(db.String(20), default="active")
    # Role of the user
    role = db.Column(db.String(20), default="doctor")
    
    # Link to Admin
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'),default='admin')
    # Doctor has many appointments
    schedules = db.relationship('Schedule_doctors', backref='doctor', lazy=True)
    # Appointment request by patient
    appointment = db.relationship('Appointment', backref='doctor', lazy=True)

    

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    # Appointment request by Customer
    appointment = db.relationship('Appointment', backref='patient', lazy=True)
    # NEW: status field -> active / blocked / deleted
    status = db.Column(db.String(20), default="active", nullable=False)
    role = db.Column(db.String(20), default="customer", nullable=False)
    

    

class Schedule_doctors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(100), nullable=False)
    doctor_availability = db.Column(db.Integer, nullable=False)

    # Belongs to one doctor
    doct_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)

    #giving schedule data for taking appointment availability
    appointment=db.relationship('Appointment')


class Appointment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    #for checking the time of doctors availability
    date=db.Column(db.Integer,nullable=False)
    time=db.Column(db.Integer,nullable=False)

    patient_id=db.Column(db.Integer,db.ForeignKey('patient.id'),nullable=False,unique=True)
    doctor_id=db.Column(db.Integer,db.ForeignKey('doctor.id'),nullable=False,unique=True)
    
    
    status=db.Column(db.String(20),default="pending",nullable=False)

    #schedule time createed by doctor
    schedule=db.Column(db.Integer,db.ForeignKey('schedule_doctors.id'))
    #doctors create treatment of patient
    treatment=db.relationship('Treatment',backref='doctor')

class Department(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(),nullable=False)
    description=db.Column(db.String(),nullable=False)
    building=db.Column(db.String(),nullable=False)
    status=db.Column(db.String(),default="active",nullable=False)

    #every doctor refers to a department
    doctors=db.relationship('Doctor',lazy=True)

    # Link to Admin
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'),default="admin", nullable=False)

class Treatment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    diagonsis=db.Column(db.String(),nullable=False)
    prescription=db.Column(db.String(),nullable=False)
    notes=db.Column(db.String(),nullable=False)

    #appointment refers to the doctor details 
    appt_id=db.Column(db.Integer,db.ForeignKey('appointment.id'),nullable=False)


