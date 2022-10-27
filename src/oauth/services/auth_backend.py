from rest_framework import authentication, exceptions


class AuthBackend(authentication.BaseAuthentication):
    authentication_header_prefix = 'Token'

    def authenticate(self, request, token=None, **kwargs):
        auth_header = authentication.get_authorization_header(request).split()

        if not auth_header or auth_header[0].lower() != b'token':
            return None

        if len(auth_header) == 1:
            raise exceptions.AuthenticationFailed("Invalid token header. No credential provided")

        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed("Invalid token header. Token string should not contain spaces")

        try:
            token = auth_header[1].decode('utf-8')
        except UnicodeError:
            raise exceptions.AuthenticationFailed(
                ('Invalid token header. Token string should not cantain in')
            )