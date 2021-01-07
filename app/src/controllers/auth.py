from flask import Blueprint, render_template, redirect, url_for, request, session, flash, current_app
from flask_login import login_user, logout_user, login_required, current_user
from flask_principal import identity_changed, AnonymousIdentity, Identity

from app.src.services.user import user_exists, add_user
from app.src.utils.geo import GeoParser


auth_bp = Blueprint('auth', __name__)


@auth_bp.route("/auth", methods = ['GET'])
def auth():
    if current_user.is_authenticated:
        return redirect(url_for('index.index'))
    return render_template('auth.html')


@auth_bp.route('/auth/logout')
@login_required
def logout():
    logout_user()

    for key in ('identity.name', 'identity.auth_type'):
        session.pop(key, None)
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())

    return redirect(url_for('auth.auth'))


@auth_bp.route("/auth/login", methods = ['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    remember_user = True if request.form.get('remember_me') else False

    user = user_exists(email)

    print(user)

    if not user or not user.valid_password(password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.auth'))

    login_user(user, remember=remember_user)

    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

    return redirect(url_for('index.index'))


@auth_bp.route("/auth/register", methods = ['POST'])
def register():
    user = None
    email = request.form.get('email')
    password = request.form.get('password')

    # check user exists
    if user_exists(email):
        flash("User already exists!")
        return redirect(url_for('auth.auth'))
 
    # check user type
    if request.form.get('user') == "employee":
        city = request.form.get('city')

        # check city exists
        if GeoParser.get_geo_coordinates(city):
            firstname = request.form.get('firstname')
            surname = request.form.get('surname')
            sex = 1 if request.form.get('sex') == "male" else 0
            birth_date = request.form.get('birth_year')
            city = request.form.get('city')

            # add employee to db
            user = add_user(email, password, firstname, surname, sex, birth_date, city)
        else:
            flash("City don't exists!")
            return redirect(url_for('auth.auth'))
    else:
        # add employeer to db
        user = add_user(email, password)

    login_user(user)

    identity_changed.send(current_app._get_current_object(), identity=Identity(user.id))

    return redirect(url_for('index.index'))


