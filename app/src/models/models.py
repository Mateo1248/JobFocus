from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

from app.src.models import db
from app.src.utils.geo import GeoParser
from app.src.utils.ml_utils import TxtParser




class RoleAbstract:

    @property
    def role(self):
        return self.__tablename__



class EmploymentType(db.Model):
    __tablename__ = "employment_type"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(200))

    job = db.relationship("Job", back_populates="type")

    @staticmethod
    def as_dict():
        return { k:v for k,v in EmploymentType.query.with_entities(EmploymentType.id, EmploymentType.type).all()}



class EducationDegree(db.Model):
    __tablename__ = "education_degree"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    degree = db.Column(db.String(200))

    job = db.relationship("Job", back_populates="education")

    @staticmethod
    def as_dict():
        return { k:v for k,v in EducationDegree.query.with_entities(EducationDegree.id, EducationDegree.degree).all()}


class EmployeeExperience(db.Model):
    __tablename__ = "employee_experience"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    position = db.Column(db.String(300))
    city = db.Column(db.String(200))
    description = db.Column(db.Text)
    desc_raw = db.Column(db.Text)
    pos_raw = db.Column(db.String(300))

    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    employee = db.relationship("Employee", back_populates="experience")


    def __init__(self, position, city, description, employee_id):
        self.position = position
        self.city = city
        self.description = description
        self.employee_id = employee_id
        self.desc_raw = TxtParser.raw_txt(description)
        self.pos_raw = TxtParser.raw_txt(position)



class EmployeeInterest(db.Model):
    __tablename__ = "employee_interest"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    interest = db.Column(db.String(200))
    inter_raw = db.Column(db.String(300))

    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    employee = db.relationship("Employee", back_populates="interest") 


    def __init__(self, interest, employee_id):
        self.interest = interest
        self.employee_id = employee_id
        self.inter_raw = TxtParser.raw_txt(interest)



class Job(db.Model):
    __tablename__ = "job"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    is_active = db.Column(db.Integer)
    position = db.Column(db.String(300))
    company = db.Column(db.String(200))
    city = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    desc_raw = db.Column(db.Text)
    pos_raw = db.Column(db.String(300))

    employment_type = db.Column(db.Integer, db.ForeignKey('employment_type.id'))
    type = db.relationship("EmploymentType", back_populates="job")

    education_required = db.Column(db.Integer, db.ForeignKey('education_degree.id'))
    education = db.relationship("EducationDegree", back_populates="job") 

    employeer_id = db.Column(db.Integer, db.ForeignKey('employeer.id'))
    employeer = db.relationship("Employeer", back_populates="job") 

    rating = db.relationship("JobRating", back_populates="job")


    def __init__(self, position, company, city, description, edu_r, emp_t, employeer_id):
        self.position = position
        self.company = company
        self.description = description
        self.employeer_id = employeer_id
        self.education_required = edu_r
        self.employment_type = emp_t
        self.employeer_id = employeer_id
        self.is_active = 1
        self.city = city
        self.latitude, self.longitude = GeoParser.get_geo_coordinates(city)
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.desc_raw = TxtParser.raw_txt(description)
        self.pos_raw = TxtParser.raw_txt(position)


class JobRating(db.Model):
    __tablename__ = "job_rating"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    rating = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)

    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    employee = db.relationship("Employee", back_populates="rating") 

    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    job = db.relationship("Job", back_populates="rating") 


    def __init__(self, rating, employee_id, job_id):
        self.rating = rating
        self.employee_id = employee_id
        self.job_id = job_id
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class UserAbstract:
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = generate_password_hash(value, method='sha256')

    def valid_password(self, value):
        return check_password_hash(self.password, value)

    def is_employee(self):
        return self.__tablename__ == "employee"


class Employeer(UserAbstract, RoleAbstract, UserMixin, db.Model):
    __tablename__ = "employeer"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(300), unique=True)
    registered_on = db.Column(db.DateTime)
    active = db.Column(db.Integer)
    _password = db.Column(db.String(400))

    job = db.relationship("Job", back_populates="employeer")

    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.registered_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.active = 1

    def safe(self):
        return {
            'email': self.email
        }.items()



class Employee(UserAbstract, RoleAbstract, UserMixin, db.Model):
    __tablename__ = "employee"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    surname = db.Column(db.String(200))
    first_name = db.Column(db.String(200))
    birth_date = db.Column(db.Date)
    email = db.Column(db.String(300), unique=True)
    city = db.Column(db.String(200))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    male = db.Column(db.Integer)
    registered_on = db.Column(db.DateTime)
    active = db.Column(db.Integer)
    _password = db.Column(db.String(400))

    experience = db.relationship("EmployeeExperience", back_populates="employee")
    interest = db.relationship("EmployeeInterest", back_populates="employee")
    rating = db.relationship("JobRating", back_populates="employee")

    def __init__(self, first_name, surname, birth_date, email, city, male, password):
        self.first_name = first_name
        self.surname = surname
        self.birth_date = birth_date
        self.email = email
        self.city = city
        self.male = male
        self.password = password
        self.active = 1
        self.registered_on = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.latitude, self.longitude = GeoParser.get_geo_coordinates(self.city)

    def safe(self):
        return {
            'first name': self.first_name,
            'surname': self.surname,
            'birth date': self.birth_date,
            'city': self.city,
            'email': self.email
        }.items()



class WordIdf(db.Model):
    __tablename__ = "word_idf"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.String(200))
    idf = db.Column(db.Float)

    def __init__(self, word, idf):
        self.word = word
        self.idf = idf

    @staticmethod
    def as_dict():
        return { k:v for k,v in WordIdf.query.with_entities(WordIdf.word, WordIdf.idf).all()}