from flask import Flask,render_template
from models import db,User

app=Flask(__name__)

#app.config['SECRET_KEY']='12346'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///hms.db'


db.init_app(app)

with app.app_context():
    db.create_all() 

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/login')
def login():
    return render_template("login.html")
   


if __name__=="__main__":
    app.run(debug=True)

