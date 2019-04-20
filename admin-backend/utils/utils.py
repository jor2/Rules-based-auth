from flask import request
from functools import wraps
from time import gmtime, strftime
from jose import jwt


# Format error response and append status code
def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get("Authorization", None)
    if not auth:
        return "authorization_header_missing"

    parts = auth.split()

    if parts[0].lower() != "bearer":
        return "invalid_header"
    elif len(parts) == 1:
        return "invalid_header"
    elif len(parts) > 2:
        return "invalid_header"

    token = parts[1]
    return token


def get_current_hour_gmt():
    return strftime("%H", gmtime())


def requires_auth(f):
    """Determines if the Access Token is valid"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if requires_scope("Doctor"):
            current_hour = int(get_current_hour_gmt())
            if current_hour >= 9 and current_hour < 17:
                return f(*args, **kwargs)
            else:
                return "current hour {} is outside of range".format(current_hour)
        return f(*args, **kwargs)
    return decorated


def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    token = get_token_auth_header()
    unverified_claims = jwt.get_unverified_claims(token)
    if unverified_claims.get("scope"):
            token_scopes = unverified_claims["scope"].split()
            for token_scope in token_scopes:
                if token_scope == required_scope:
                    return True
    return False
