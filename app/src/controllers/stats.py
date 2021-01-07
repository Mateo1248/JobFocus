from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user

from app.src.services.user import delete_user, update_user
from app.src.utils.auth import employeer_permission
from app.src.services.stats import employeer_stats


stats_ep = Blueprint('stats', __name__)


@stats_ep.route("/statistics/employeer", methods=['GET'])
@login_required
@employeer_permission.require(http_exception=403)
def stats():
    return render_template(
        'stats.html', 
        user=current_user, 
        stats=employeer_stats(current_user.id),
        enumerate=enumerate
    )