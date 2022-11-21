from database import db
from sqlalchemy.sql import func

class Admin(db.Model):
    __tablename__ = 'admins'
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Admin: %r>' % self.email


class School(db.Model):
    __tablename__ ="school"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    short_code = db.Column(db.String(3), unique=True, nullable=False)
    departments = db.relationship('Department', backref='school', lazy=True)
    
    def __repr__(self):
        return f'<School:  {self.name}>'

class Department(db.Model):
    __tablename__ = "department"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    school_id = db.Column(db.Integer, db.ForeignKey('school.id'), nullable=False)
    lecturers = db.relationship('Lecturer', backref='department', lazy=True)
    students  = db.relationship('Students', backref='department', lazy=True)

    def __repr__(self):
        return f'<Department:  {self.name}>'

class Lecturer(Admin):
    __tablename__ = "lecturer"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    courses =   db.relationship('Course', backref='lecturer', lazy="dynamic")
    attendances = db.relationship('Attendance', backref='lecturer', lazy="dynamic")

    def __repr__(self):
        return f'<Lecturer:  {self.firstname} {self.lastname}>'


class Course(db.Model):
    __tablename__ = "course"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    code = db.Column(db.String(6), unique=True, nullable=False)
    lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturer.id'), nullable=False)
    attendances = db.relationship('Attendance', backref='course', lazy=True)

    def __repr__(self):
        return f'<Course:  {self.title}>'

class Students(db.Model):
    __tablename__ = "student"

    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64), nullable=False)
    lastname = db.Column(db.String(64), nullable=False)
    mat_no = db.Column(db.String(20), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    department_id =  db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    attendances = db.relationship('Attendance', backref='student', lazy=True)

    qr_code = db.Column(db.BLOB())

    def __repr__(self):
            return f'<Student:  {self.firstname} {self.lastname}>'

class Attendance(db.Model):
    __tablename__ = "attendance_records"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String, db.ForeignKey('student.mat_no'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    course_lecturer_id = db.Column(db.Integer, db.ForeignKey('lecturer.id'), nullable=False)
    date = db.Column(db.DateTime(timezone=True),  server_default=func.now())

    def __repr__(self):
        return f'<Attendance Sheet:  {self.date}>'

    def __str__(self) -> str:
        return self.date

