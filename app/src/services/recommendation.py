from flask import render_template
from flask_login import current_user

from app.src.utils.ml_utils import RecommendationEngine
from app.src.services.user import get_user_by_id
from app.src.services.rating import exists_for_job_employee
from app.src.services.job import get_employeer_contact


def get_recommendation(emp_id, keywords):
    jobs = RecommendationEngine.get_recommendations(
        get_user_by_id(emp_id),
        keywords, 
        n=30
    )

    max_r = 1
    for job in jobs:
        if job['f_factor'] > max_r:
            max_r = job['f_factor']

    response = ""
    for job in jobs:
        if max_r > 1:
            job['f_factor'] /= max_r
        response += render_template('jobEnity.html', 
            job=job, 
            contact=get_employeer_contact(job['id']),
            rating=exists_for_job_employee(emp_id, job['id'])
        )

    return response