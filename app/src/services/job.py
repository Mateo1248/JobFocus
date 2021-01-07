from app.src.models.models import Job


def get_employeer_contact(job_id):
    return Job.query.filter_by(id=job_id).first().employeer.email