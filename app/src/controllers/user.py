from flask import Blueprint, request, render_template, redirect, url_for, flash, Response
from flask_login import login_required, current_user, logout_user

from app.src.services.user import delete_user, update_user, add_update_experience, add_update_interest, add_update_joboffer, get_exp_by_id, get_int_by_id, get_job_by_id
from app.src.services.rating import add_update_rating
from app.src.utils.auth import employeer_permission, employee_permission
from app.src.models import db_delete

user_ep = Blueprint('user', __name__)


@user_ep.route("/user", methods=['POST', 'DELETE'])
@login_required
def manage_user():
    if request.method == 'POST':
        updated = update_user(
            user_id =current_user.id,
            email = request.form.get('email'),
            firstname = request.form.get('first_name'),
            surname = request.form.get('surname'),
            birth_date = request.form.get('birth_date'),
            city = request.form.get('city')
        )
        if not updated:
            flash("City does not exists!")
        flash("User succesfully updated!")
        return redirect(url_for('index.index'))

    elif request.method == 'DELETE':
        delete_user(current_user.id)
        logout_user()
        flash("User succesfully deleted!")
        return redirect(url_for('auth.auth'), code=303)

    else:
        flash("Method not allowed!")
        return render_template('index.html', user=current_user)



@user_ep.route("/user/employee/rating", methods=['POST'])
@login_required
@employee_permission.require(http_exception=403)
def rating():
    add_update_rating(
        current_user.id,
        request.values['job_id'],
        request.values['rate']
    )
    return Response(status=201)



@user_ep.route("/user/employee/experience", methods=['POST', 'GET'])
@login_required
@employee_permission.require(http_exception=403)
def experience():
    if "att_form_btn" in request.form:
        if request.form["att_form_btn"] == "UPDATE":
            added = add_update_experience(
                request.form['position'],
                request.form['city'],
                request.form['description'],
                current_user.id,
                request.form['attId']
            )
            if added:
                flash("Experience updated succesfully!")
            else:
                flash("Can't update experience, city does not exists!")
            return redirect(url_for("index.addatt"))

        elif request.form["att_form_btn"] == "DELETE":
            exp = get_exp_by_id(request.form['attId'])
            db_delete(exp)
            flash("Experience succesfully deleted!")
            return redirect(url_for("index.addatt"))
        else:
            return Response(status=406)
    else:
        added = add_update_experience(
            request.values['position'],
            request.values['city'],
            request.values['description'],
            current_user.id,
            request.values['experience_id'] if 'experience_id' in request.values else None
        )
        if added:
            return Response(status=201)
        return Response(status=404)



@user_ep.route("/user/employee/interest", methods=['GET', 'POST'])
@login_required
@employee_permission.require(http_exception=403)
def interest():
    if "att_form_btn" in request.form:
        if request.form["att_form_btn"] == "UPDATE":
            add_update_interest(
                request.values['interest'],
                current_user.id,
                request.values['attId'] 
            )
            flash("Interest updated succesfully!")
            return redirect(url_for("index.addatt"))

        elif request.form["att_form_btn"] == "DELETE":
            inter = get_int_by_id(request.form['attId'])
            db_delete(inter)
            flash("Interest succesfully deleted!")
            return redirect(url_for("index.addatt"))
        else:
            return Response(status=406)
    else:
        add_update_interest(
            request.values['interest'],
            current_user.id,
            request.values['interest_id'] if 'interest_id' in request.values else None
        )
        return Response(status=201)



@user_ep.route("/user/employeer/advert", methods=['GET', 'POST'])
@login_required
@employeer_permission.require(http_exception=403)
def advert():
    if "att_form_btn" in request.form:
        if request.form["att_form_btn"] == "UPDATE":
            added = add_update_joboffer(
                request.values['position'],
                request.values['company'],
                request.values['city'],
                request.values['description'],
                request.values['edu_r'],
                request.values['emp_t'],
                current_user.id,
                request.values['attId'] 
            )
            if added:
                flash("Job offer updated succesfully!")
            else:
                flash("Can't update job offer, city does not exists!")
            return redirect(url_for("index.addatt"))

        elif request.form["att_form_btn"] == "DELETE":
            job = get_job_by_id(request.form['attId'])
            db_delete(job)
            flash("Job offer succesfully deleted!")
            return redirect(url_for("index.addatt"))
        else:
            return Response(status=406)
    else:
        added = add_update_joboffer(
            request.values['position'],
            request.values['company'],
            request.values['city'],
            request.values['description'],
            request.values['edu_r'],
            request.values['emp_t'],
            current_user.id,
            request.values['joboffer_id'] if 'joboffer_id' in request.values else None
        )
        if added:
            return Response(status=201)
        return Response(status=404)
