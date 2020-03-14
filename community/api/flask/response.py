import simplejson as json
from flask import Response


def json_success(result, status=200, indent=None):
    payload = {
        'success': True,
        'result': result,
        'errorMessage': None
    }
    return Response(json.dumps(payload, indent=indent, for_json=True),
                    status=status,
                    mimetype="application/json")


def json_failure(msg, status=None, stacktrace=None):
    payload = {
        'success': False,
        'result': None,
        'errorMessage': str(msg)
    }
    if stacktrace:
        payload['stacktrace'] = stacktrace
    status = status if status else 500
    return Response(json.dumps(payload, for_json=True),
                    status=status,
                    mimetype="application/json")


