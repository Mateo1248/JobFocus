from flask import Blueprint, request
from flask_login import login_required, current_user

from app.src.utils.auth import employee_permission
from app.src.services.recommendation import get_recommendation


recommendation_ep = Blueprint('recommendation', __name__)


@recommendation_ep.route("/recommendation/employee", methods=['GET'])
@login_required
@employee_permission.require(http_exception=403)
def get_recommendations():
    return get_recommendation(
        current_user.id,
        request.values['keywords']
    )
