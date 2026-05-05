from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db=SQLAlchemy()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    name = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(20), default="admin", nullable=False)
    # One Admin can create many doctors
    doctors = db.relationship('Doctor', backref='created_by', lazy=True)
    ## One Admin can create many dept
    depts = db.relationship('Department', backref='created_by', lazy=True)


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # created by admin
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    specialization = db.Column(db.String(100), nullable=True)
    #link to department
    dept_id=db.Column(db.Integer,db.ForeignKey('department.id'))
    availability = db.Column(db.String(200), default="Available on request")
    # NEW: status field -> active / blocked / deleted
    status = db.Column(db.String(20), default="active")
    # Role of the user
    role = db.Column(db.String(20), default="doctor")
    
    # Link to Admin
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), default=1)
    # Doctor has many appointments
    schedules = db.relationship('Schedule_doctors', backref='doctor', lazy=True)
    # Appointment request by patient
    appointment = db.relationship('Appointment', backref='doctor', lazy=True)
    # Doctor availability for 7 days
    availability_schedule = db.relationship('DoctorAvailability', backref='doctor', lazy=True, cascade="all, delete-orphan")

    

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    date_of_birth = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    # Appointment request by Customer
    appointment = db.relationship('Appointment', backref='patient', lazy=True)
    # NEW: status field -> active / blocked / deleted
    status = db.Column(db.String(20), default="active", nullable=False)
    role = db.Column(db.String(20), default="patient", nullable=False)
    

    

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
    date=db.Column(db.String(20),nullable=False)
    time=db.Column(db.String(20),nullable=False)
    reason=db.Column(db.String(300), nullable=True)

    patient_id=db.Column(db.Integer,db.ForeignKey('patient.id'),nullable=False)
    doctor_id=db.Column(db.Integer,db.ForeignKey('doctor.id'),nullable=False)
    
    
    status=db.Column(db.String(20),default="pending",nullable=False)

    #schedule time createed by doctor
    schedule=db.Column(db.Integer,db.ForeignKey('schedule_doctors.id'))
    #doctors create treatment of patient
    treatment=db.relationship('Treatment',backref='appointment')

class Department(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(),nullable=False)
    description=db.Column(db.String(),nullable=False)
    building=db.Column(db.String(),nullable=False)
    status=db.Column(db.String(),default="active",nullable=False)

    #every doctor refers to a department
    doctors=db.relationship('Doctor', backref='department', lazy=True)

    # Link to Admin
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), default=1)

class Treatment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    diagnosis=db.Column(db.String(), nullable=False)
    prescription=db.Column(db.String(), nullable=False)
    notes=db.Column(db.String(), nullable=False)
    created_at=db.Column(db.DateTime, default=datetime.now)

    #appointment refers to the doctor details 
    appt_id=db.Column(db.Integer,db.ForeignKey('appointment.id'),nullable=False)


class DoctorAvailability(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'), nullable=False)
    date = db.Column(db.String(20), nullable=False)  # Format: YYYY-MM-DD
    time_slots = db.Column(db.String(500), nullable=False)  # JSON array of available times like "09:00,10:00,11:00"
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
