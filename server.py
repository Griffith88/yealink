import os

from datetime import date
from logging import basicConfig
from werkzeug.exceptions import abort
from cofigure_file import Phone
from flask import Flask, Response, send_file, request

log_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logs', f'{date.today()}-log.log'))
basicConfig(filename=log_path)
app = Flask('yealink')


@app.route('/<mac>.cfg')
def configure_telephone(mac):
    if mac.startswith('y'):
        abort(404)
    user_agent = request.headers.get('User-Agent')
    app.logger.info(f'Пришел запрос на автоконфигурацию от устройства {user_agent}')
    phone = Phone(mac, user_agent)
    try:
        config_file = phone.get_configuration_file_name()
    except ValueError as val:
        config_file = None
        app.logger.warning(f'{val.args}')
        abort(404)

    with open(config_file, 'r', encoding='utf8') as f:
        return Response(f.read(), mimetype='text/plain')


@app.route('/firmware/<firmware_name>')
def update_firmware(firmware_name):
    file = os.path.normpath(os.path.join(os.path.dirname(__file__), 'firmware', firmware_name))
    return send_file(file, download_name=firmware_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True)
