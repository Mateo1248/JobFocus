from typing import Dict, Union

from app.src.models.models import Employee, Employeer, EmployeeExperience, EmployeeInterest, Job
from app.src.models import db_add, db_delete, db
from app.src.utils.geo import GeoParser
from app.src.utils.ml_utils import TxtParser


User = Union[Employee, Employeer]


def user_exists(email: str) -> User:
    return Employee.query.filter_by(email=email).first() or Employeer.query.filter_by(email=email).first()


def get_user_by_id(user_id: int) -> User:
    return Employee.query.filter_by(id=user_id).first() or Employeer.query.filter_by(id=user_id).first()


def add_user(email: str, password: str, firstname: str=None, surname: str=None, sex: int=None, birth_date: str=None, city: str=None) -> Dict[str, any]:
    user = None
    # check user type
    if firstname:
        user = Employee(
            firstname,
            surname,
            f"{birth_date}-01-01",
            email,
            city,
            sex,
            password
        )
    else:
        user = Employeer(
            email,
            password
        )

    # add user to db
    db_add(user)

    return user


def delete_user(user_id):
    user = get_user_by_id(user_id)
    db_delete(user)


def update_user(user_id: int, email: str, firstname: str=None, surname: str=None, birth_date: str=None, city: str=None):
    user = get_user_by_id(user_id)
    if firstname:
        user.email = email
        user.firstname = firstname
        user.surname = surname
        user.birth_date = birth_date
        if user.city != city:
            user.city = city
            coords = GeoParser.get_geo_coordinates(city)
            if not coords:
                return False
            user.latitude, user.longitude = coords
    else:
        user.email = email
    db.session.commit()

    return True


def add_advert():
    pass


def add_update_experience(position, city, description, employee_id, exp_id=None):

    coords = GeoParser.get_geo_coordinates(city)
    if not coords:
        return False

    if exp_id:
        exp = get_exp_by_id(exp_id)
        exp.position = TxtParser.raw_txt(position)
        exp.description = TxtParser.raw_txt(description)
        exp.city = city
        db.session.commit()
        return True
    else:
        exp = EmployeeExperience(
            position,
            city,
            description,
            employee_id
        )
        db_add(exp)
        return True


def add_update_interest(interest, employee_id, inter_id=None):
    if inter_id:
        inter = get_int_by_id(inter_id)
        inter.interest = TxtParser.raw_txt(interest)
        db.session.commit()
    else:
        inter = EmployeeInterest(
            interest,
            employee_id
        )
        db_add(inter)


def get_int_by_id(int_id):
    return EmployeeInterest.query.filter_by(id=int_id).first()


def get_exp_by_id(exp_id):
    return EmployeeExperience.query.filter_by(id=exp_id).first()


def add_update_joboffer(position, company, city, description, edu_r, emp_t, employeer_id, joffer_id=None):
    if joffer_id:
        joboff = get_job_by_id(joffer_id)
        joboff.position = position
        joboff.company = company
        joboff.description = description
        joboff.pos_raw = TxtParser.raw_txt(position)
        joboff.desc_raw = TxtParser.raw_txt(description)
        joboff.education_required = edu_r
        joboff.employment_type = emp_t

        if joboff.city != city:
            joboff.city = city
            coords = GeoParser.get_geo_coordinates(city)
            if not coords:
                return False
            joboff.latitude, joboff.longitude = coords
        db.session.commit()
    else:
        joboff = Job(
            position,
            company,
            city,
            description,
            edu_r,
            emp_t,
            employeer_id
        )
        db_add(joboff)
    return True


def get_job_by_id(j_id):
    return Job.query.filter_by(id=j_id).first()


def get_experience(user_id):
    user = get_user_by_id(user_id)
    if user.is_employee():
        return user.experience
    return False

def get_interest(user_id):
    user = get_user_by_id(user_id)
    if user.is_employee():
        return user.interest
    return False


def get_joboffers(user_id):
    user = get_user_by_id(user_id)
    if not user.is_employee():
        return user.job
    return False