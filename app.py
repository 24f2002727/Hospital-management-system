from flask import Flask,render_template,request,redirect,url_for,session,flash
from models import db,Admin,Patient,Doctor,Department,Appointment,Treatment,Schedule_doctors
from werkzeug.security import generate_password_hash,check_password_hash

app=Flask(__name__)

app.config['SECRET_KEY']='12346'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///hms.db'


db.init_app(app)

#create predefined admin credentials
def create_admin():
    with app.app_context():
        db.create_all()
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            hashed_pwd=generate_password_hash('123456',method='pbkdf2:sha256')
            admin = Admin(username='admin', email='shivam@gmail.com', contact='12345678900', password=hashed_pwd)
            db.session.add(admin)
            db.session.commit()



@app.route('/')
def home():
    return render_template("home.html")


#register route
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        username=request.form['username']
        email=request.form['email']
        contact=request.form['contact']
        password=request.form['password']
        print(username)

        #hassh the password
        hashed_pwd=generate_password_hash(password,method='pbkdf2:sha256')

        #chek if useername already exists
        #existing_user=Patient.query.filter(Patient.username==username or Patient.email==email).first()
        existing_user = Patient.query.filter((Patient.username == username) | (Patient.email == email)).first()
        if existing_user:
            flash("Username or email already registered")
            return(redirect(url_for('register')))


        #creating the new registered customer
        new_patient=Patient(username=username,email=email,contact=contact,password=hashed_pwd)

        #adding to the databasse
        db.session.add(new_patient)
        db.session.commit()

        flash("Registration successful,Please log in")
        return redirect(url_for('login'))

    #return redirect(url_for('register.html'))
    return render_template("register.html")
    

#login route
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='POST':
        role=request.form['role']
        username=request.form['username']
        password=request.form['password']
        user=None

        #Get user based on the role
        if role=='admin':
            user=Admin.query.filter_by(username=username).first()

        elif role=='doctor':
            user=Doctor.query.filter_by(username=username).first()

        elif role=='patient':
            user=Patient.query.filter_by(username=username).first()


        #check password and lohin
        if user:
            if check_password_hash(user.password,password):
                session['user_id']=user.id
                session['role']=role
                flash(f"Logged in as {role}","Succees")
                return redirect(url_for(f"{role}_dashboard"))
            
            else:
                flash("Incorrect password")
                      

        else:
            flash(f"No {role} found with that username")

    
    return render_template('login.html')       


@app.route('/admin_dashboard')
def admin_dashboard():
    doctors = Doctor.query.all()
    patients = Patient.query.all()
    departments=Department.query.all()
    #appointments=Appointment.query.all()
    return render_template('admin_dashboard.html',doctors=doctors,patients=patients,departments=departments)    


@app.route('/create_doctor', methods=['GET', 'POST'])
def create_doctor():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        contact = request.form['contact']
        department = request.form['dept_id']

        # Hash the password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_doctor = Doctor(username=username,password=hashed_password,email=email, contact=contact, dept_id=department)
        db.session.add(new_doctor)
        db.session.commit()

        flash("Doctor created successfully!", "success")
        return redirect(url_for('admin_dashboard'))

    return render_template('create_doctor.html')

@app.route('/edit_doctor/<doctor_id>', methods=['GET', 'POST'])
def edit_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    if request.method == 'POST':
        doctor.username = request.form['username']
        doctor.email = request.form['email']
        doctor.contact = request.form['contact']
        doctor.dept_id = request.form['dept_id']
        doctor.status = request.form['status']
        db.session.commit()
        flash("Doctor data updated!", "success")
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_doctor.html', doctor=doctor)


@app.route('/delete_doctor/<doctor_id>', methods=['GET','POST'])
def delete_doctor(doctor_id):
    doctor = Doctor.query.get(doctor_id)
    db.session.delete(doctor)
    db.session.commit()
    flash("Doctor deleted successfully!", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/doctor_dashboard')
def doctor_dashboard():
    return render_template('doctor_dashboard.html') 

@app.route('/patient_dashboard')
def patient_dashboard(patient_id):
    patient=Patient.query.get(session.get(patient_id))
    return render_template('patient_dashboard.html',patient=patient)

@app.route('/create_department', methods=['GET', 'POST'])
def create_department():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']        
        building = request.form['building']

        new_department = Department(name=name, description=description, building=building)
        db.session.add(new_department)
        db.session.commit() 
        flash("Department created successfully!", "success")
        return redirect(url_for('admin_dashboard')) 

    return render_template('create_department.html')

@app.route('/edit_department/<dept_id>', methods=['GET', 'POST'])
def edit_department(dept_id):   
    department = Department.query.get(dept_id)
    if request.method == 'POST':
        department.name = request.form['name']
        department.description = request.form['description']
        department.building = request.form['building']
        department.status = request.form['status']
        db.session.commit()
        flash("Department data updated!", "success")
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_department.html', department=department)

@app.route('/delete_department/<dept_id>', methods=['GET','POST'])
def delete_department(dept_id):
    department = Department.query.get(dept_id)
    db.session.delete(department)
    db.session.commit()
    flash("Department deleted successfully!", "success")
    return redirect(url_for('admin_dashboard'))

@app.route('/edit_patient/<patient_id>', methods=['GET', 'POST'])
def edit_patient(patient_id):
    patient = Patient.query.get(patient_id)
    if request.method == 'POST':
        patient.username = request.form['username']
        patient.email = request.form['email']
        patient.contact = request.form['contact']
        patient.status = request.form['status']
        db.session.commit()
        flash("Patient data updated!", "success")
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_patient.html', patient=patient)

@app.route('/delete_patient/<patient_id>', methods=['GET','POST'])
def delete_patient(patient_id):
    patient = Patient.query.get(patient_id)
    db.session.delete(patient)
    db.session.commit()
    flash("Patient deleted successfully!", "success")
    return redirect(url_for('admin_dashboard'))


if __name__=="__main__":
    create_admin()
    app.run(debug=True,port=5005)

