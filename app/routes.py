from flask import Blueprint, jsonify, request, current_app
from functools import wraps
from .models import AirRaidAlertMessageParser

bp = Blueprint('main', __name__)

def authenticate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_key = request.args.get('auth_key')
        if auth_key in current_app.config['AUTH_KEYS']:
            return f(*args, **kwargs)
        else:
            return jsonify({'error': 'Invalid auth_key'}), 401
    return decorated_function

def get_all_region_statuses(country, is_alert_param=None):
    region_statuses = {}

    for region in country.regions:
        is_alert = region.is_alert
        message = AirRaidAlertMessageParser.ALERT_MESSAGE if is_alert else AirRaidAlertMessageParser.END_MESSAGE
        timestamp = region.last_change_at.isoformat() if region.last_change_at else None
        # Find the region name using the region id in a more readable way
        region_name = get_region_name(region.id)

        if is_alert_param is None or is_alert == is_alert_param:
            region_statuses[region.id] = {
                'is_alert': is_alert,
                'message': message,
                'timestamp': timestamp,
                'name': region_name
            }
    return region_statuses

def get_region_name(region_id):
    for name, id in AirRaidAlertMessageParser.REGION_MAP.items():
        if id == region_id:
            return name.replace('_', ' ')
    return "Unknown Region"

@bp.route('/alerts')
@authenticate
def alerts():
    is_alert_param_str = request.args.get('is_alert', '').lower()
    is_alert_param = None

    if is_alert_param_str in ['true', 'false']:
        is_alert_param = is_alert_param_str == 'true'

    country = current_app.country
    return jsonify(get_all_region_statuses(country, is_alert_param))

@bp.route('/ping')
@authenticate
def ping():
    return jsonify({'message': 'pong'})




