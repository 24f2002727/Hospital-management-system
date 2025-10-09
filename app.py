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
            admin = Admin(username='admin', email='shivam@gmail.com', contact=1234567890, password='admin123')
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
            user=Admin.query.filter_by(username='username').first()

        elif role=='doctor':
            user=Admin.query.filter_by(username=username).first()

        elif role=='patient':
            user=Admin.query.filter_by(username='username').first()


        #check password and lohin
        if user:
            if check_password_hash(user.password,password):
                session['user_id']=user.id
                session['role']=role
                flash(f"Loggen in as {role}","Succes")
                return redirect(url_for(f"{role}_dashboard"))
            
            else:
                flash("Incorrect password")
                      

        else:
            flash(f"No {role} found with that username")

    
    return render_template('login.html')       


        

if __name__=="__main__":
    create_admin()
    app.run(debug=True,port=5005)

