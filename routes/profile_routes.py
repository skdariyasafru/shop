from flask import Blueprint, render_template
from flask_login import login_required, current_user

from models.models import User

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile")
@login_required
def profile():

    referred_name = "None"

    if current_user.referred_by:
        ref_user = User.query.get(current_user.referred_by)

        if ref_user:
            referred_name = ref_user.username

    network_count = User.query.filter_by(
        referred_by=current_user.id
    ).count()

    return render_template(
        "profile.html",
        user=current_user,
        referred_name=referred_name,
        network_count=network_count,
        wallet_balance=current_user.wallet_balance
    )
