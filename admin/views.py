from flask import Blueprint, redirect, send_file, render_template as render, session, request, flash, url_for , make_response
from utils import auth_required, list_contains
from app import *

dashboard = Blueprint("dashboard", __name__, template_folder="./templates/", static_folder="./static/", url_prefix='/admin')



@dashboard.route('/')
@auth_required
def admin():
    user = Lecturer.query.filter_by(email=session['username']).first()
    total_students = Students.query.filter_by(department_id= user.department_id)
    courses = Course.query.filter_by(lecturer_id=user.id)
    return render(
        'index-admin.html', 
        student_count = total_students.count(), 
        courses=courses.count()
        )	



@dashboard.route('/courses/', methods=['GET', 'POST'])
@auth_required
def courses():
    lecturer = Lecturer.query.filter_by(email=session['username']).first()
    if request.method == 'POST':
        fields = ['title', 'code']
        if list_contains(request.form, fields):
            course_title = request.form.get('title')
            course_code =  request.form.get('code')
            

            course = Course(
                title = course_title,
                code = course_code,
                lecturer_id = lecturer.id
            )
            db.session.add(course)
            db.session.commit()
            flash('Course Added Successfully')
            return "<span class='alert alert-success alert-dismissible'>Course Added Successfully</span>"
        else:
            return "<span class='alert alert-danger alert-dismissible'>Some Fields Are Empty!</span>"

    getCourses = Course.query.filter_by(lecturer_id=lecturer.id)
    return render('courses.html', courses=getCourses)
	
@dashboard.route('/courses/<int:id>/delete/')
@auth_required
def deleteCourse(id):
    course = db.get_or_404(Course, id)
    if course:
        flash(f'{course.title} deleted successfully')
        db.session.delete(course)
        db.session.commit()
    else:
        flash('could not find course')
        
    return redirect(url_for('dashboard.courses'))

@dashboard.route('/courses/set/<int:id>/')
@auth_required
def setCourse(id):
     course = db.get_or_404(Course, id)
     if course:
        return f"<script>document.cookie = 'courseID={course.id}'; </script>"


@dashboard.route('/courses/edit/<int:id>/', methods=['POST'])
@auth_required
def editCourse(id):
    course = db.get_or_404(Course, id)

    if request.method=='POST':
        if course:
            if request.form['title'] is not None and request.form['code'] is not None:
                course.title =  request.form['title']
                course.code =  request.form['code']
                print(request.form['title'], flush=True)
                print(request.form['code'], flush=True)
                db.session.merge(course)
                db.session.flush()
                db.session.commit()
                return f"<span class='alert alert-success alert-dismissible'>Changed Successfully</span><script>document.cookie = 'courseID=;' </script>"
            else:
                return  f"<span class='alert alert-success alert-dismissible'>Error Failed To Change Course</span>"      
        else:
            flash('could not find course')
        
        return redirect(url_for('dashboard.courses'))


@dashboard.route("/take-attendance/", methods=['GET'])
@auth_required
def takeAttendance():
    return render('take-attendance.html')

@dashboard.route("/get-attendance/", methods=['GET','POST'])
@auth_required   
def getAttendances():
    lecturer_id = session['id']
    attendance = Attendance.query.filter_by(course_lecturer_id=lecturer_id)
    return render('./attendances.html', attendances=attendance)

@dashboard.route("/add-attendance/", methods=['POST'])
@auth_required   
def addAttendance():
    if request.method == 'POST':
        try:
            mat = request.form['mat_no']
            student = Students.query.filter_by(mat_no=mat).first()
            check_one = Attendance.query.one(student_id=student.id)

            if check_one:
                return "This student has scanned before!"

            else:
                attendance =  Attendance(
                    student_id = student.id,
                    course_id = 1,
                    course_lecture_id = session['id']
                )
                db.session.add(attendance)
                db.session.commit()
                return "Added Successfully!"
        except Exception as e:
                print(f'Error:{e}', flush=True)
    