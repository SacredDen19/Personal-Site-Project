from flask import Blueprint, Flask, render_template, session, request
from api.datab import load_loggedin
import re
from ..handlers.log_handler import error_parser

admin_panel = Blueprint('apanel', __name__)


@admin_panel.route('/admin', methods=['GET'])
def landing():
    if request.method == 'GET':
        usr = load_loggedin()
        
        with open("/var/www/public_html/logs/error.log") as log_file:
            logs = log_file.read()
        formatted_logs = error_parser(logs)

        return render_template('admin_dashboard.html', user=usr, line=formatted_logs)
