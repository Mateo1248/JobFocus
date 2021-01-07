from flask import Blueprint, render_template, url_for, redirect
from flask_login import login_required, current_user

from app.src.utils.auth import employee_permission, employeer_permission
from app.src.services.user import get_experience, get_interest, get_joboffers


index_page = Blueprint('index', __name__)


@index_page.route("/", methods=['GET'])
@login_required
def index():
    return render_template('index.html', user=current_user)


@index_page.route("/browser/employee", methods=['GET'])
@login_required
@employee_permission.require(http_exception=403)
def browser():
    return render_template('browser.html', user=current_user)


@index_page.route("/additional", methods=['GET'])
@login_required
def addatt():
    experience_raw = get_experience(current_user.id)
    interest_raw = get_interest(current_user.id)
    joboffers_raw = get_joboffers(current_user.id)

    attCls = ""

    experience = ""
    if experience_raw:
        attCls = "experience"
        for e in experience_raw:
            experience += render_template("addattEnity.html", experience=e, attCls = attCls, id=e.id)
    interest = ""
    if interest_raw:
        attCls = "interest"
        for i in interest_raw:
            interest += render_template("addattEnity.html", interest=i, attCls = attCls, id=i.id)
    joboffers = ""
    if joboffers_raw:
        attCls = "joboffers"
        for j in joboffers_raw:
            joboffers += render_template("addattEnity.html", joboffer=j, attCls = attCls, id=j.id)


    return render_template(
        'addatt.html', 
        user=current_user,
        experience = experience,
        interest = interest,
        joboffers = joboffers
    )