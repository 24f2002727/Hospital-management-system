from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default="admin", nullable=False)

    # One Admin can create many doctors
    doctors = db.relationship('Doctor', backref='created_by', lazy=True)


class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # created by admin
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default="doctor", nullable=False)
    # NEW: status field -> active / blocked / deleted
    status = db.Column(db.String(20), default="active", nullable=False)

    # Link to Admin
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'), nullable=False)

    #link to department
    dept_id=db.column(db.Integer,db.ForeignKey('dept.id'),nullable=False)

    # Doctor has many appointments
    schedules = db.relationship('Schedule', backref='doctor', lazy=True)

    # Appointment request by patient
    appointment = db.relationship('Appointmemt', backref='doctor', lazy=True)

    

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default="customer", nullable=False)

    # NEW: status field -> active / blocked / deleted
    status = db.Column(db.String(20), default="active", nullable=False)

    # Appointment request by Customer
    appointment = db.relationship('Appointment', backref='patient', lazy=True)

class Schedule_doctors(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    doctor_name = db.Column(db.String(100), nullable=False)
    doctor_availability = db.Column(db.Integer, nullable=False)

    # Belongs to one doctor
    doct_id = db.Column(db.Integer, db.ForeignKey('doct.id'), nullable=False)

class Appointment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    #for checking the time of doctors availability
    date=db.Column(db.Integer,nullable=False)
    time=db.Column(db.Integer,nullable=False)

    patient_id=db.Column(db.Integer,nullable=False,unique=True)
    doctor_id=db.Column(db.Integer,nullable=False,unique=True)
    
    status=db.Column(db.String(20),default="pending",nullable=False)

    #appointment references a doctor
    doctor=db.relationship('Schedule',backref='appointment')

class Department(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(),nullable=False)
    description=db.Column(db.String(),nullable=False)
    reg_doctors_id=db.Column(db.Integer,nullable=False)

class Treatment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    appt_id=db.column(db.Integer,nullable=False,unique=True)
    diagonsis=db.Column(db.String(),nullable=False)
    prescription=db.Column(db.String(),nullable=False)
    notes=db.Column(db.String(),nullable=False)
