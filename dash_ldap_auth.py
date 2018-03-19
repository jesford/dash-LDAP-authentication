from dash_auth.auth import Auth
import base64
import flask
import ldap


class LDAPAuth(Auth):
    def __init__(self, app):
        Auth.__init__(self, app)

    def _credentials_are_valid(self, username, password):
        """Verifies credentials for username and password.
        Returns True on success or False on failure.
        """
        LDAP_SERVER = 'ldap://xxx.xxx.xxx'         # EDIT THIS
        LDAP_USERNAME = '%s@xxx.com' % username    # EDIT THIS
        LDAP_PASSWORD = password

        try:
            # build a client
            ldap_client = ldap.initialize(LDAP_SERVER)
            # perform a synchronous bind
            ldap_client.set_option(ldap.OPT_REFERRALS, 0)
            ldap_client.simple_bind_s(LDAP_USERNAME, LDAP_PASSWORD)
        except ldap.INVALID_CREDENTIALS:
            ldap_client.unbind()
            # Wrong username or password
            return False
        except ldap.SERVER_DOWN:
            # AD server not available
            return False
        # all is well
        ldap_client.unbind()
        # Login successful
        return True

    def is_authorized(self):
        header = flask.request.headers.get('Authorization', None)
        if not header:
            return False
        username_password = base64.b64decode(header.split('Basic ')[1])
        username_password_utf8 = username_password.decode('utf-8')
        username, password = username_password_utf8.split(':')

        is_valid = self._credentials_are_valid(username, password)
        return is_valid

    def login_request(self):
        return flask.Response(
            'Login Required',
            headers={'WWW-Authenticate': 'Basic realm="User Visible Realm"'},
            status=401)

    def auth_wrapper(self, f):
        def wrap(*args, **kwargs):
            if not self.is_authorized():
                return flask.Response(status=403)

            response = f(*args, **kwargs)
            return response
        return wrap
