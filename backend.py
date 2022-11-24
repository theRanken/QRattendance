from __future__ import print_function
from flask import (
	render_template as render, 
	redirect, request, flash, 
	url_for, 
	send_file,
	session
	)
from app import *
from qr_code import *
from utils import list_contains
import logging, traceback, io
from admin.views import dashboard


@app.route('/')
def index():
	return render('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
	fields = ['email','password']
	if request.method == 'POST':
		if list_contains(request.form, fields):
			e = request.form.get('email')
			p = request.form.get('password')

			# Get The Account Entered And Return an Error if not found
			account = Lecturer.query.filter_by(email=e).first()
			if account and p == account.password:			
				try:
						session.clear()
						session['authenticated'] = True
						session['id'] = account.id
						session['username'] = account.email
						session.permanent = True
						flash('Login Success!')
						print(session, flush=True)
						return redirect(url_for('dashboard.admin'))
				except Exception as e:
					flash('Oops Cannot Login, Something Went Wrong!')
					print(f"Error: {e}", flush=True)
			elif not account:
				flash('Username is incorrect')
			elif p != account.password:
				flash('Password is Incorrect')

	return render('login.html')
	
@app.route('/logout')	
def logout():
	# Clears session data, this will log the user out
    session.clear()
   # Redirect to login page
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])	
def register():
	fields = ['surname','firstname','email','phone','password'] 
	if request.method == 'POST':
		if list_contains(request.form, fields):
			sname = request.form.get('surname')
			fname = request.form.get('firstname')
			e = request.form.get('email')
			dept = request.form.get('department')
			pwd = request.form.get('password')

			try:
				admin = Lecturer(
					firstname = sname,
					lastname = fname,
					email = e,
					department_id  = int(dept),
					password = pwd
				)
				db.session.add(admin)
				db.session.commit()
				flash('New Admin Added!')
				return redirect(url_for('login'))
			except Exception as e:
				return f'Error: {e}'
	schools = School.query.all()
	return render('register.html', s=schools)
	
###-----------------###	
###----CRUD----###
###-----------------###
@app.route('/add-student/', methods=["GET", "POST"])
def addStudent():
	if request.method == 'POST':
		first_name = request.form.get('surname', 'None')
		last_name = request.form.get('firstname', 'None')
		phone_no = request.form.get('phone', 'None')
		e_mail = request.form.get('email', 'None')
		matric_num = request.form.get('mat_no', 'None')
		dept = request.form.get('department', 'None')

		student_qr = generate_code(f'{first_name} {last_name};', matric_num, mat_no=matric_num)
		get_student_qr = get_qr_code(student_qr)

		try:
			mat_no_exists = Students.query.filter_by(mat_no=matric_num).first() is not None
			if  mat_no_exists:
				flash('Matric number already exist in the database, You can proceed to view details associated with this matric number, or check, contact support')
				return redirect(url_for('addStudents'))
			else:
				student = Students(
					firstname = first_name,
					lastname = last_name,
					mat_no = matric_num,
					phone = phone_no,
					department_id = int(dept),
					qr_code = get_student_qr
				)
				db.session.add(student)
				db.session.commit()

				#Deletes the image from local storage
				clean_image(student_qr)
				flash('Enrollment Successful!')
				return redirect(url_for('index'))
				
		except Exception as e:
			print(f'Error: {e}', flush=True)		

	s = School.query.all()
	return render('enroll.html', schools=s)

@app.route('/view-profile')
def view_profile():
	return render('view-profile.html')




####--------------HELPER VIEWS-----------------####
@app.route('/get-departments')
def get_departments():
	arg = request.args.get('school')
	school =  School.query.filter_by(name=arg).first()
	list_of_departments = Department.query.filter_by(school_id=school.id).all()

	return render('./utilities/department_list.html', departments=list_of_departments)

@app.route('/view-student-info')
def view_student():
	n = request.args.get('mat')
	s = Students.query.filter_by(mat_no=n).first()
	if s is None:
		return f'<h2>No student with Matric Number: {n}</h2>'
	return render('./utilities/show-profile-info.html', st = s)

@app.route('/images/<int:image>')
def get_image(image):
	student = Students.query.filter_by(id=image).first_or_404()
	bytes = io.BytesIO(student.qr_code)
	return send_file(bytes, mimetype="image/png")

@app.route('/student/attendance/count')
def get_students_count():
	lecturer_id = session['id']
	attendance = Attendance.query.filter_by(course_lecturer_id=lecturer_id)
	return f'Students Present: {attendance.count()}'

app.register_blueprint(dashboard)
print(app.url_map, flush=True)

if __name__  == '__main__':	
	# db.drop_all()
	db.create_all()
	app.run(debug=True, host="0.0.0.0", port=5000, ssl_context='adhoc')