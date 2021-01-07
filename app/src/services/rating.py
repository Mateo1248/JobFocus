from datetime import datetime

from app.src.models.models import JobRating
from app.src.models import db_add, db


def exists_for_job_employee(empid, jobid):
    return JobRating.query.filter_by(employee_id=empid, job_id=jobid).first()


def add_update_rating(employee_id, job_id, rating_val):
    rat = exists_for_job_employee(employee_id, job_id)
    if rat:
        rat.rating = rating_val
        rat.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        db.session.commit()
    else:
        db_add(
            JobRating(
                rating_val,
                employee_id,
                job_id
            )
        )
