from dropbox import DropboxOAuth2FlowNoRedirect


class TokenProvider:

    def __init__(self, api_key, api_secret, token_filename):
        self.api_key = api_key
        self.api_secret = api_secret
        self.token_filename = token_filename

    def token(self):
        try:
            f = open(self.token_filename, 'r')
            token = f.readline()
            if len(token) == 0:
                f.close()
                raise Exception()
            else:
                return token
        except Exception:
            f = open(self.token_filename, 'a')
            token = self._interactive_phase()
            f.writelines(token)
            f.close()
            return token

    def _interactive_phase(self):
        auth_flow = DropboxOAuth2FlowNoRedirect(self.api_key, self.api_secret)
        authorize_url = auth_flow.start()
        print("1. Go to: " + authorize_url)
        print("2. Click \"Allow\" (you might have to log in first).")
        print("3. Copy the authorization code.")
        auth_code = input("Enter the authorization code here: ").strip()
        oauth_result = auth_flow.finish(auth_code)
        return oauth_result.access_token
