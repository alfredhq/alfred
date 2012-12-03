from flask import Blueprint, request, current_app, jsonify, abort
from flask_login import login_required, current_user

from ..helpers import send_to_amqp


tasks = Blueprint('tasks', __name__)


@tasks.route('/sync/')
@login_required
def sync():
    send_to_amqp(
        tasks=[{'user_id': current_user.get_id()}],
        queue_name=current_app.config['AMQP']['sync_queue_name'],
    )
    return jsonify(status='ok')


@tasks.route('/sync/status/')
@login_required
def sync_status():
    return jsonify(is_syncing=current_user.is_syncing)
