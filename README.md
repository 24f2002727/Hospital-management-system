# Hospital-management-system
It is the dummy hospital mangement repository for the bootcamp

Day-1

Create a "templates folder" --> inside this only all the HTML pages will be made and saved.
Home page of your application --> home.html --> will be your landing page of the application.
Patient Registration HTML page is made with the help of HTML forms tag.
User (Admin, Doctor and Patient) Login HTML page is made with the help of HTML forms tag.
Flask app initialization is done in the file --> app.py.
1st route --> initial route --> for rendering your home page is done.
Models for 5 tables especially - Doctor, Patient, Appointment, Treatment, Department --> is completed --> models.py file.
Database Initialization is done in the file --> app.py
When you run the python file (app.py), your database is getting created with name "your_db_name.db" --> with all the tables created in models.py.
Please install SQLite Viewer in your VSCode extensions to see your database clearly.

Day-2

Establishing the relationship between the tables created inside models.py file.
Once done, and database is getting created, commit your changes.
Setting up or predefining the code for admin credentials in app.py file.
Once done commit this change as well.
Create a base.html page --> containing the rules of flashing the message for success and danger.
Template inheritance is done in registration.html and login.html file from base.html file, using jinja2.
Create a route for Patient Registration HTML page --> to render the HTML page.
Create a route for Login of 3 users --> Admin, Doctor and Patient --> to render the HTML page.
Create a basic HTML page for --> Admin Dashboard.
Create a basic HTML page for --> Doctor Dashboard.
Create a basic HTML page for --> Patient Dashboard.
Create a route for Admin Dashboard HTML page --> to render the HTML page.
Create a route for Doctor Dashboard HTML page --> to render the HTML page.
Create a route for Patient Dashboard HTML page --> to render the HTML page.
Once done, commit the changes of registration and login, with dashboard routes and HTML pages.
After cross reviewing your task with me, then only you will push your codes on github repository.

Day-3

Create a HTML Page for --> creating department --> done by admin.
Create a route for creating department HTML page --> to render the HTML page.
Create a button on admin dashboard --> to redirect to create department page.
Table creation showing the list of all the present departments --> with edit and delete button --> on admin dashboard.
Using jinja2, all the details of departments are shown on admin dashboard inside the table.
Create a HTML page --> for editing the department --> done by admin.
Create a route for editing the department HTML page --> to render the HTML page.
Create a route for deleting the department --> done by admin.
Once done, commit all the changes done till now.
After cross reviewing your task with me, then only you will push your codes on github repository.
Create a HTML page --> for creating doctors profile --> done by admin.
Create a route for creating doctors profile HTML page --> to render the HTML page.
Create a button on admin dashboard --> to redirect to create doctor profile page.
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