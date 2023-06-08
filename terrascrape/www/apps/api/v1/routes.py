from flask import jsonify

from terrascrape.www.apps.api.v1 import blueprint


@blueprint.route('/health', methods=['GET'])
def health():
    return jsonify(dict(status='OK'))
