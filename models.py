from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class User(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(),nullable=False,unique=True)
    password=db.Column(db.String(),nullable=False)
    email=db.Column(db.String(),nullable=False,unique=True)

class Person(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(),nullable=False)
    gender=db.Column(db.String(),nullable=False)
    phone=db.Column(db.Integer,nullable=False)
    aadhar=db.Column(db.Integer,unique=True,nullable=False)
    email=db.Column(db.Integer)

class Patient(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    height=db.Column(db.Integer,nullable=False)
    weight=db.Column(db.Integer,nullable=False)
    blood=db.Column(db.String(),nullable=False)
    allergy=db.Column(db.String())
    problem=db.Column(db.String(),nullable=False)

class Doctor(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    dept_id=db.Column(db.Integer,nullable=False)
    specilisation=db.Column(db.String(),nullable=False)
    reg_no=db.Column(db.Integer,nullable=False,unique=True)
    degree=db.Column(db.Integer)
    
class Appointment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    patient_id=db.Column(db.Integer,nullable=False,unique=True)
    doctor_id=db.Column(db.Integer,nullable=False,unique=True)
    date=db.Column(db.Integer,nullable=False)
    time=db.Column(db.Integer,nullable=False,unique=True)

class Department(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(),nullable=False)
    building=db.Column(db.String(),nullable=False)

class Treatment(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    patient_id=db.Column(db.Integer,nullable=False)
    doctor_id=db.Column(db.Integer,nullable=False,unique=True)
    diagonsis=db.Column(db.String(),nullable=False)
    medicine=db.Column(db.String(),nullable=False)
