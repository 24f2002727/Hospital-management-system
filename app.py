from functools import wraps
from datetime import datetime, timedelta
import json

from flask import Flask, flash, redirect, render_template, request, session, url_for
from sqlalchemy import inspect, text, and_, or_
from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from models import Admin, Appointment, Department, Doctor, Patient, Treatment, DoctorAvailability, db


app = Flask(__name__)
app.config["SECRET_KEY"] = "12346"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hms.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)


def login_required(role=None):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            if "user_id" not in session:
                flash("Please login to continue.", "warning")
                return redirect(url_for("login"))
            if role and session.get("role") != role:
                flash("You do not have access to that page.", "danger")
                return redirect(url_for("home"))
            return view(*args, **kwargs)

        return wrapped

    return decorator


def status_badge(status):
    return {
        "active": "success",
        "pending": "warning",
        "completed": "success",
        "cancelled": "danger",
        "blocked": "danger",
        "closed": "secondary",
        "removed": "secondary",
    }.get(status, "info")


app.jinja_env.filters["status_badge"] = status_badge


def migrate_database():
    """Keep older bootcamp databases usable after model improvements."""
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()

    if "admin" in tables:
        admin_columns = {column["name"] for column in inspector.get_columns("admin")}
        if "name" not in admin_columns:
            db.session.execute(text("ALTER TABLE admin ADD COLUMN name VARCHAR(100) DEFAULT 'Admin'"))
    
    if "doctor" in tables:
        doctor_columns = {column["name"] for column in inspector.get_columns("doctor")}
        if "availability" not in doctor_columns:
            db.session.execute(text("ALTER TABLE doctor ADD COLUMN availability VARCHAR(200) DEFAULT 'Available on request'"))
        if "name" not in doctor_columns:
            db.session.execute(text("ALTER TABLE doctor ADD COLUMN name VARCHAR(100) DEFAULT 'Doctor'"))
        if "specialization" not in doctor_columns:
            db.session.execute(text("ALTER TABLE doctor ADD COLUMN specialization VARCHAR(100)"))

    if "patient" in tables:
        patient_columns = {column["name"] for column in inspector.get_columns("patient")}
        if "name" not in patient_columns:
            db.session.execute(text("ALTER TABLE patient ADD COLUMN name VARCHAR(100) DEFAULT 'Patient'"))
        if "date_of_birth" not in patient_columns:
            db.session.execute(text("ALTER TABLE patient ADD COLUMN date_of_birth VARCHAR(20)"))
        if "address" not in patient_columns:
            db.session.execute(text("ALTER TABLE patient ADD COLUMN address VARCHAR(200)"))

    if "appointment" in tables:
        appt_columns = {column["name"] for column in inspector.get_columns("appointment")}
        if "reason" not in appt_columns:
            db.session.execute(text("ALTER TABLE appointment ADD COLUMN reason VARCHAR(300)"))

        indexes = inspector.get_indexes("appointment")
        unique_indexes = [idx for idx in indexes if idx.get("unique")]
        if unique_indexes:
            db.session.execute(text("ALTER TABLE appointment RENAME TO appointment_old"))
            db.session.execute(
                text(
                    """
                    CREATE TABLE appointment (
                        id INTEGER NOT NULL PRIMARY KEY,
                        date VARCHAR(20) NOT NULL,
                        time VARCHAR(20) NOT NULL,
                        reason VARCHAR(300),
                        patient_id INTEGER NOT NULL,
                        doctor_id INTEGER NOT NULL,
                        status VARCHAR(20) NOT NULL DEFAULT 'pending',
                        schedule INTEGER,
                        FOREIGN KEY(patient_id) REFERENCES patient (id),
                        FOREIGN KEY(doctor_id) REFERENCES doctor (id),
                        FOREIGN KEY(schedule) REFERENCES schedule_doctors (id)
                    )
                    """
                )
            )
            old_columns = {column["name"] for column in inspector.get_columns("appointment_old")}
            reason_expr = "reason" if "reason" in old_columns else "NULL"
            db.session.execute(
                text(
                    f"""
                    INSERT INTO appointment (id, date, time, reason, patient_id, doctor_id, status, schedule)
                    SELECT id, date, time, {reason_expr}, patient_id, doctor_id, status, schedule
                    FROM appointment_old
                    """
                )
            )
            db.session.execute(text("DROP TABLE appointment_old"))

    if "treatment" in tables:
        treatment_columns = {column["name"] for column in inspector.get_columns("treatment")}
        if "diagonsis" in treatment_columns and "diagnosis" not in treatment_columns:
            db.session.execute(text("ALTER TABLE treatment ADD COLUMN diagnosis VARCHAR(500)"))
        if "created_at" not in treatment_columns:
            db.session.execute(text("ALTER TABLE treatment ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP"))

    db.session.commit()


def create_admin():
    with app.app_context():
        db.create_all()
        migrate_database()
        admin = Admin.query.filter_by(username="admin").first()
        if not admin:
            admin = Admin(
                username="admin",
                email="shivam@gmail.com",
                contact="12345678900",
                password=generate_password_hash("123456", method="pbkdf2:sha256"),
            )
            db.session.add(admin)
            db.session.commit()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        username = request.form["username"].strip()
        email = request.form["email"].strip().lower()
        contact = request.form["contact"].strip()
        password = request.form["password"]

        existing_user = Patient.query.filter((Patient.username == username) | (Patient.email == email)).first()
        if existing_user:
            flash("Username or email already registered.", "danger")
            return redirect(url_for("register"))

        patient = Patient(
            name=name,
            username=username,
            email=email,
            contact=contact,
            password=generate_password_hash(password, method="pbkdf2:sha256"),
        )
        db.session.add(patient)
        db.session.commit()

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form["role"]
        username = request.form["username"].strip()
        password = request.form["password"]
        model = {"admin": Admin, "doctor": Doctor, "patient": Patient}.get(role)
        user = model.query.filter_by(username=username).first() if model else None

        if user and check_password_hash(user.password, password):
            if getattr(user, "status", "active") in {"blocked", "removed"}:
                flash("Your account is not active. Please contact the administrator.", "danger")
                return redirect(url_for("login"))
            session["user_id"] = user.id
            session["role"] = role
            flash(f"Logged in as {role}.", "success")
            return redirect(url_for(f"{role}_dashboard"))

        flash("Invalid role, username, or password.", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))


@app.route("/admin_dashboard")
@login_required("admin")
def admin_dashboard():
    doctors = Doctor.query.order_by(Doctor.id.desc()).all()
    patients = Patient.query.order_by(Patient.id.desc()).all()
    departments = Department.query.order_by(Department.id.desc()).all()
    appointments = Appointment.query.order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    
    # Calculate statistics
    today = datetime.now().strftime("%Y-%m-%d")
    upcoming_appts = Appointment.query.filter(Appointment.date >= today, Appointment.status != 'cancelled').count()
    completed_appts = Appointment.query.filter_by(status='completed').count()
    
    return render_template(
        "admin_dashboard.html",
        doctors=doctors,
        patients=patients,
        departments=departments,
        appointments=appointments,
        stats={
            "doctors": Doctor.query.filter_by(status="active").count(),
            "patients": Patient.query.filter_by(status="active").count(),
            "departments": Department.query.count(),
            "appointments": Appointment.query.count(),
            "upcoming_appointments": upcoming_appts,
            "completed_appointments": completed_appts,
        },
    )


@app.route("/admin_search", methods=["POST"])
@login_required("admin")
def admin_search():
    search_query = request.form["search_query"].strip()
    search_type = request.form.get("search_type", "all")
    doctors = []
    patients = []
    departments = []

    if search_query:
        if search_type in ["doctors", "all"]:
            doctors = Doctor.query.filter(
                or_(
                    Doctor.name.ilike(f"%{search_query}%"),
                    Doctor.username.ilike(f"%{search_query}%"),
                    Doctor.specialization.ilike(f"%{search_query}%")
                )
            ).all()
        if search_type in ["patients", "all"]:
            patients = Patient.query.filter(
                or_(
                    Patient.name.ilike(f"%{search_query}%"),
                    Patient.username.ilike(f"%{search_query}%"),
                    Patient.email.ilike(f"%{search_query}%"),
                    Patient.contact.ilike(f"%{search_query}%")
                )
            ).all()
        if search_type in ["departments", "all"]:
            departments = Department.query.filter(
                Department.name.ilike(f"%{search_query}%")
            ).all()

    today = datetime.now().strftime("%Y-%m-%d")
    upcoming_appts = Appointment.query.filter(Appointment.date >= today, Appointment.status != 'cancelled').count()
    
    return render_template(
        "admin_dashboard.html",
        doctors=doctors if search_type in ["doctors", "all"] else [],
        patients=patients if search_type in ["patients", "all"] else [],
        departments=departments if search_type in ["departments", "all"] else [],
        appointments=Appointment.query.order_by(Appointment.date.desc(), Appointment.time.desc()).all(),
        search_performed=True,
        search_query=search_query,
        search_type=search_type,
        stats={
            "doctors": Doctor.query.filter_by(status="active").count(),
            "patients": Patient.query.filter_by(status="active").count(),
            "departments": Department.query.count(),
            "appointments": Appointment.query.count(),
            "upcoming_appointments": upcoming_appts,
        },
    )


@app.route("/create_doctor", methods=["GET", "POST"])
@login_required("admin")
def create_doctor():
    departments = Department.query.filter_by(status="active").order_by(Department.name).all()
    if request.method == "POST":
        doctor = Doctor(
            name=request.form["name"].strip(),
            username=request.form["username"].strip(),
            password=generate_password_hash(request.form["password"], method="pbkdf2:sha256"),
            email=request.form["email"].strip().lower(),
            contact=request.form["contact"].strip(),
            specialization=request.form.get("specialization", "").strip(),
            dept_id=request.form["dept_id"],
            availability=request.form.get("availability", "Available on request").strip(),
        )
        db.session.add(doctor)
        try:
            db.session.commit()
            flash("Doctor created successfully.", "success")
            return redirect(url_for("admin_dashboard"))
        except IntegrityError:
            db.session.rollback()
            flash("Doctor username or email already exists.", "danger")

    return render_template("create_doctor.html", departments=departments)


@app.route("/edit_doctor/<int:doctor_id>", methods=["GET", "POST"])
@login_required("admin")
def edit_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    departments = Department.query.order_by(Department.name).all()
    if request.method == "POST":
        doctor.name = request.form["name"].strip()
        doctor.username = request.form["username"].strip()
        doctor.email = request.form["email"].strip().lower()
        doctor.contact = request.form["contact"].strip()
        doctor.specialization = request.form.get("specialization", "").strip()
        doctor.dept_id = request.form["dept_id"]
        doctor.availability = request.form.get("availability", "").strip()
        doctor.status = request.form["status"]
        db.session.commit()
        flash("Doctor data updated.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("edit_doctor.html", doctor=doctor, departments=departments)


@app.route("/delete_doctor/<int:doctor_id>")
@login_required("admin")
def delete_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    doctor.status = "removed"  # Blacklist instead of delete
    db.session.commit()
    flash("Doctor removed from the system.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/blacklist_doctor/<int:doctor_id>")
@login_required("admin")
def blacklist_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    doctor.status = "blocked"
    db.session.commit()
    flash("Doctor has been blocked.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/activate_doctor/<int:doctor_id>")
@login_required("admin")
def activate_doctor(doctor_id):
    doctor = Doctor.query.get_or_404(doctor_id)
    doctor.status = "active"
    db.session.commit()
    flash("Doctor has been activated.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/create_department", methods=["GET", "POST"])
@login_required("admin")
def create_department():
    if request.method == "POST":
        department = Department(
            name=request.form["name"].strip(),
            description=request.form["description"].strip(),
            building=request.form["building"].strip(),
        )
        db.session.add(department)
        db.session.commit()
        flash("Department created successfully.", "success")
        return redirect(url_for("admin_dashboard"))

    return render_template("create_department.html")


@app.route("/edit_department/<int:dept_id>", methods=["GET", "POST"])
@login_required("admin")
def edit_department(dept_id):
    department = Department.query.get_or_404(dept_id)
    if request.method == "POST":
        department.name = request.form["name"].strip()
        department.description = request.form["description"].strip()
        department.building = request.form["building"].strip()
        department.status = request.form["status"]
        db.session.commit()
        flash("Department data updated.", "success")
        return redirect(url_for("admin_dashboard"))
    return render_template("edit_department.html", department=department)


@app.route("/delete_department/<int:dept_id>")
@login_required("admin")
def delete_department(dept_id):
    department = Department.query.get_or_404(dept_id)
    db.session.delete(department)
    db.session.commit()
    flash("Department deleted successfully.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/doctor_dashboard")
@login_required("doctor")
def doctor_dashboard():
    doctor = Doctor.query.get_or_404(session["user_id"])
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Get upcoming appointments for this week
    week_end = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    upcoming_appointments = Appointment.query.filter(
        Appointment.doctor_id == doctor.id,
        Appointment.date >= today,
        Appointment.date <= week_end,
        Appointment.status != 'cancelled'
    ).order_by(Appointment.date, Appointment.time).all()
    
    # Get all appointments (for history)
    all_appointments = Appointment.query.filter_by(doctor_id=doctor.id).order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    
    # Get patients assigned to this doctor
    patient_ids = set([appt.patient_id for appt in all_appointments])
    patients = Patient.query.filter(Patient.id.in_(patient_ids)).all() if patient_ids else []
    
    treatments = Treatment.query.join(Appointment).filter(Appointment.doctor_id == doctor.id).all()
    
    return render_template(
        "doctor_dashboard.html",
        doctor=doctor,
        upcoming_appointments=upcoming_appointments,
        all_appointments=all_appointments,
        patients=patients,
        treatments=treatments,
        stats={
            "upcoming": len(upcoming_appointments),
            "patients": len(patients),
            "completed": Appointment.query.filter_by(doctor_id=doctor.id, status='completed').count(),
        }
    )


@app.route("/update_availability", methods=["GET", "POST"])
@login_required("doctor")
def update_availability():
    doctor = Doctor.query.get_or_404(session["user_id"])
    
    if request.method == "POST":
        action = request.form.get("action", "set_general")
        
        if action == "set_general":
            # Set general availability message
            doctor.availability = request.form["availability"].strip()
            db.session.commit()
            flash("Availability updated.", "success")
        elif action == "set_schedule":
            # Set availability for 7 days
            today = datetime.now().date()
            for i in range(7):
                date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
                is_available = request.form.get(f"available_{i}") == "on"
                time_slots = request.form.get(f"times_{i}", "09:00,10:00,11:00,14:00,15:00,16:00").strip()
                
                # Check if already exists
                existing = DoctorAvailability.query.filter_by(doctor_id=doctor.id, date=date).first()
                if existing:
                    existing.is_available = is_available
                    existing.time_slots = time_slots
                    existing.updated_at = datetime.now()
                else:
                    availability = DoctorAvailability(
                        doctor_id=doctor.id,
                        date=date,
                        time_slots=time_slots,
                        is_available=is_available
                    )
                    db.session.add(availability)
            
            db.session.commit()
            flash("7-day availability schedule updated.", "success")
        
        return redirect(url_for("doctor_dashboard"))
    
    # Get 7-day availability schedule
    today = datetime.now().date()
    schedule = []
    for i in range(7):
        date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
        availability = DoctorAvailability.query.filter_by(doctor_id=doctor.id, date=date).first()
        schedule.append({
            'day_num': i,
            'date': date,
            'day_name': (today + timedelta(days=i)).strftime("%A"),
            'available': availability.is_available if availability else False,
            'time_slots': availability.time_slots if availability else "09:00,10:00,11:00,14:00,15:00,16:00"
        })
    
    return render_template("update_availability.html", doctor=doctor, schedule=schedule)


@app.route("/patient_dashboard")
@login_required("patient")
def patient_dashboard():
    patient = Patient.query.get_or_404(session["user_id"])
    today = datetime.now().strftime("%Y-%m-%d")
    
    # Upcoming appointments
    upcoming_appointments = Appointment.query.filter(
        Appointment.patient_id == patient.id,
        Appointment.date >= today,
        Appointment.status != 'cancelled'
    ).order_by(Appointment.date, Appointment.time).all()
    
    # Past appointments
    past_appointments = Appointment.query.filter(
        Appointment.patient_id == patient.id,
        Appointment.date < today
    ).order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    
    # All appointments
    all_appointments = Appointment.query.filter_by(patient_id=patient.id).order_by(Appointment.date.desc(), Appointment.time.desc()).all()
    
    departments = Department.query.filter_by(status="active").order_by(Department.name).all()
    doctors = Doctor.query.filter_by(status="active").order_by(Doctor.name).all()
    treatments = Treatment.query.join(Appointment).filter(Appointment.patient_id == patient.id).all()
    
    return render_template(
        "patient_dashboard.html",
        patient=patient,
        upcoming_appointments=upcoming_appointments,
        past_appointments=past_appointments,
        all_appointments=all_appointments,
        departments=departments,
        doctors=doctors,
        treatments=treatments,
        stats={
            "upcoming": len(upcoming_appointments),
            "past": len(past_appointments),
            "completed": Appointment.query.filter_by(patient_id=patient.id, status='completed').count(),
        }
    )


@app.route("/edit_patient/<int:patient_id>", methods=["GET", "POST"])
@login_required()
def edit_patient(patient_id):
    if session.get("role") == "patient" and session["user_id"] != patient_id:
        flash("You can edit only your own profile.", "danger")
        return redirect(url_for("patient_dashboard"))

    patient = Patient.query.get_or_404(patient_id)
    if request.method == "POST":
        patient.name = request.form["name"].strip()
        patient.username = request.form["username"].strip()
        patient.email = request.form["email"].strip().lower()
        patient.contact = request.form["contact"].strip()
        patient.date_of_birth = request.form.get("date_of_birth", "").strip()
        patient.address = request.form.get("address", "").strip()
        if session.get("role") == "admin":
            patient.status = request.form["status"]
        db.session.commit()
        flash("Patient data updated.", "success")
        return redirect(url_for("admin_dashboard" if session.get("role") == "admin" else "patient_dashboard"))
    return render_template("edit_patient.html", patient=patient)


@app.route("/view_doctor_availability/<int:doctor_id>")
def view_doctor_availability(doctor_id):
    """API endpoint to get doctor availability"""
    doctor = Doctor.query.get_or_404(doctor_id)
    if doctor.status != "active":
        return {"error": "Doctor not available"}, 404
    
    today = datetime.now().date()
    availability_schedule = []
    for i in range(7):
        date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
        availability = DoctorAvailability.query.filter_by(doctor_id=doctor.id, date=date).first()
        if availability and availability.is_available:
            time_slots = availability.time_slots.split(',')
            # Check which times are already booked
            available_slots = []
            for slot in time_slots:
                slot = slot.strip()
                booked = Appointment.query.filter_by(
                    doctor_id=doctor.id,
                    date=date,
                    time=slot
                ).filter(Appointment.status.in_(['pending', 'completed'])).first()
                available_slots.append({
                    'time': slot,
                    'available': booked is None
                })
            availability_schedule.append({
                'date': date,
                'available': True,
                'slots': available_slots
            })
    
    return {"availability": availability_schedule}, 200


@app.route("/delete_patient/<int:patient_id>")
@login_required("admin")
def delete_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    patient.status = "removed"  # Blacklist instead of delete
    db.session.commit()
    flash("Patient removed from the system.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/blacklist_patient/<int:patient_id>")
@login_required("admin")
def blacklist_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    patient.status = "blocked"
    db.session.commit()
    flash("Patient has been blocked.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/activate_patient/<int:patient_id>")
@login_required("admin")
def activate_patient(patient_id):
    patient = Patient.query.get_or_404(patient_id)
    patient.status = "active"
    db.session.commit()
    flash("Patient has been activated.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route("/create_appointment", methods=["GET", "POST"])
@login_required("patient")
def create_appointment():
    doctors = Doctor.query.filter_by(status="active").order_by(Doctor.name).all()
    departments = Department.query.filter_by(status="active").order_by(Department.name).all()
    
    if request.method == "POST":
        doctor_id = int(request.form["doctor_id"])
        date = request.form["appointment_date"]
        time = request.form["appointment_time"]
        reason = request.form.get("reason", "").strip()
        
        # Check if doctor exists and is active
        doctor = Doctor.query.get_or_404(doctor_id)
        if doctor.status != "active":
            flash("This doctor is not available.", "danger")
            return redirect(url_for("create_appointment"))
        
        # Check if doctor has availability set for that date
        availability = DoctorAvailability.query.filter_by(doctor_id=doctor_id, date=date).first()
        if not availability or not availability.is_available:
            flash("Doctor is not available on that date.", "warning")
            return redirect(url_for("create_appointment"))
        
        # Check if that time slot is available for the doctor
        time_slots = availability.time_slots.split(',')
        time_slots = [slot.strip() for slot in time_slots]
        if time not in time_slots:
            flash("That time slot is not available.", "warning")
            return redirect(url_for("create_appointment"))
        
        # Check if doctor already has an appointment at that time
        exists = Appointment.query.filter_by(
            doctor_id=doctor_id,
            date=date,
            time=time
        ).filter(Appointment.status.in_(['pending', 'completed'])).first()
        
        if exists:
            flash("That doctor already has an appointment at the selected time.", "warning")
            return redirect(url_for("create_appointment"))

        appointment = Appointment(
            patient_id=session["user_id"],
            doctor_id=doctor_id,
            date=date,
            time=time,
            reason=reason,
            status='pending'
        )
        db.session.add(appointment)
        db.session.commit()
        flash("Appointment request booked successfully.", "success")
        return redirect(url_for("patient_dashboard"))

    return render_template("create_appointment.html", doctors=doctors, departments=departments)


@app.route("/appointment/<int:appointment_id>/<action>")
@login_required()
def update_appointment(appointment_id, action):
    appointment = Appointment.query.get_or_404(appointment_id)
    role = session.get("role")

    allowed = role == "admin" or (
        role == "doctor" and appointment.doctor_id == session["user_id"]
    ) or (
        role == "patient" and appointment.patient_id == session["user_id"] and action == "cancelled"
    )
    if not allowed or action not in {"pending", "completed", "cancelled"}:
        flash("You cannot update that appointment.", "danger")
        return redirect(url_for(f"{role}_dashboard"))

    appointment.status = action
    db.session.commit()
    flash(f"Appointment marked as {action}.", "success")
    return redirect(url_for(f"{role}_dashboard"))


@app.route("/create_treatment/<int:appointment_id>", methods=["GET", "POST"])
@login_required("doctor")
def create_treatment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    if appointment.doctor_id != session["user_id"]:
        flash("You can add treatment notes only for your appointments.", "danger")
        return redirect(url_for("doctor_dashboard"))

    treatment = Treatment.query.filter_by(appt_id=appointment.id).first()
    if request.method == "POST":
        if not treatment:
            treatment = Treatment(
                appt_id=appointment.id,
                diagnosis="",
                prescription="",
                notes=""
            )
            db.session.add(treatment)
        treatment.diagnosis = request.form["diagnosis"].strip()
        treatment.prescription = request.form["prescription"].strip()
        treatment.notes = request.form["notes"].strip()
        treatment.created_at = datetime.utcnow()
        appointment.status = "completed"
        db.session.commit()
        flash("Treatment record saved.", "success")
        return redirect(url_for("doctor_dashboard"))

    return render_template("treatment_form.html", appointment=appointment, treatment=treatment)


@app.route("/patient_treatment_history")
@login_required("patient")
def patient_treatment_history():
    patient = Patient.query.get_or_404(session["user_id"])
    treatments = Treatment.query.join(Appointment).filter(
        Appointment.patient_id == patient.id,
        Appointment.status == 'completed'
    ).order_by(Treatment.created_at.desc()).all()
    
    return render_template("patient_treatment_history.html", patient=patient, treatments=treatments)


@app.route("/doctor_patient_history/<int:patient_id>")
@login_required("doctor")
def doctor_patient_history(patient_id):
    """View patient history and previous treatment records"""
    patient = Patient.query.get_or_404(patient_id)
    doctor_id = session["user_id"]
    
    # Get all appointments between this doctor and patient
    appointments = Appointment.query.filter_by(
        doctor_id=doctor_id,
        patient_id=patient_id
    ).order_by(Appointment.date.desc()).all()
    
    # Get treatments from completed appointments
    treatments = Treatment.query.join(Appointment).filter(
        Appointment.doctor_id == doctor_id,
        Appointment.patient_id == patient_id,
        Appointment.status == 'completed'
    ).order_by(Treatment.created_at.desc()).all()
    
    return render_template("doctor_patient_history.html", patient=patient, appointments=appointments, treatments=treatments)


@app.route("/search_doctors", methods=["GET", "POST"])
@login_required("patient")
def search_doctors():
    """Search for doctors by name, specialization, or department"""
    doctors = []
    specializations = set()
    
    if request.method == "POST":
        search_query = request.form.get("search_query", "").strip()
        search_type = request.form.get("search_type", "all")
        
        if search_query:
            if search_type in ["name", "all"]:
                doctors.extend(Doctor.query.filter(
                    Doctor.name.ilike(f"%{search_query}%"),
                    Doctor.status == "active"
                ).all())
            if search_type in ["specialization", "all"]:
                doctors.extend(Doctor.query.filter(
                    Doctor.specialization.ilike(f"%{search_query}%"),
                    Doctor.status == "active"
                ).all())
            if search_type in ["department", "all"]:
                dept = Department.query.filter(
                    Department.name.ilike(f"%{search_query}%")
                ).first()
                if dept:
                    doctors.extend(Doctor.query.filter_by(dept_id=dept.id, status="active").all())
        
        # Remove duplicates
        doctors = list({d.id: d for d in doctors}.values())
    else:
        doctors = Doctor.query.filter_by(status="active").order_by(Doctor.name).all()
    
    # Get all specializations for filter
    all_specializations = db.session.query(Doctor.specialization).filter(
        Doctor.specialization.isnot(None),
        Doctor.status == "active"
    ).distinct().all()
    
    return render_template("search_doctors.html", doctors=doctors, specializations=[s[0] for s in all_specializations if s[0]])


@app.route("/doctor_profile/<int:doctor_id>")
@login_required()
def doctor_profile(doctor_id):
    """View doctor profile with availability"""
    doctor = Doctor.query.get_or_404(doctor_id)
    if doctor.status != "active":
        flash("This doctor is not available.", "warning")
        return redirect(url_for("search_doctors"))
    
    # Get 7-day availability
    today = datetime.now().date()
    availability_schedule = []
    for i in range(7):
        date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
        availability = DoctorAvailability.query.filter_by(doctor_id=doctor.id, date=date).first()
        if availability and availability.is_available:
            time_slots = availability.time_slots.split(',')
            # Check which times are available (not booked)
            available_slots = []
            for slot in time_slots:
                slot = slot.strip()
                booked = Appointment.query.filter_by(
                    doctor_id=doctor.id,
                    date=date,
                    time=slot
                ).filter(Appointment.status.in_(['pending', 'completed'])).first()
                available_slots.append({
                    'time': slot,
                    'available': booked is None
                })
            availability_schedule.append({
                'date': date,
                'day': (today + timedelta(days=i)).strftime("%A"),
                'available': True,
                'slots': available_slots
            })
    
    return render_template("doctor_profile.html", doctor=doctor, availability_schedule=availability_schedule)


@app.route("/my_appointments")
@login_required("patient")
def my_appointments():
    return redirect(url_for("patient_dashboard"))


@app.route("/view_appointments")
@login_required("doctor")
def view_appointments():
    return redirect(url_for("doctor_dashboard"))


@app.route("/my_reports")
@login_required()
def my_reports():
    return redirect(url_for(f"{session.get('role')}_dashboard"))


if __name__ == "__main__":
    create_admin()
    app.run(debug=True)
