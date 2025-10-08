from flask import Blueprint, Flask, render_template, session, request
from api.datab import load_loggedin

admin_panel = Blueprint('apanel', __name__)


@admin_panel.route('/admin', methods=['GET'])
def landing():
    if request.method == 'GET':
        usr = load_loggedin()
        return render_template('admin_dashboard.html', user=usr)
