import os

from cofigure_file import get_configuration_file_name
from flask import Flask, request, Response

app = Flask('yealink')


@app.route('/base_model_config.cfg')
def auto_provision():
    config_file = get_configuration_file_name(str(request.user_agent))

    with open(config_file, 'r', encoding='utf8') as f:
        return Response(f.read(), mimetype='text/plain')


if __name__ == '__main__':
    app.run(host='192.168.53.33', port=5000, debug=True)
