import os
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect

dpx_apikey    = os.environ['DPX_APIKEY']
dpx_apisecret = os.environ['DPX_APISECRET']
dpx_tokenfile = "tokens/" + os.environ['DPX_TOKENFILE']

def gettoken():
    try:
        f = open(dpx_tokenfile, 'r')
        token = f.readline()
        if len(token) == 0:
            f.close()
            raise Exception()
        else:
            return token
    except:
        f = open(dpx_tokenfile, 'a')
        token = _interactive_phase()
        f.writelines(token)
        f.close()
        return token


def _interactive_phase():
    auth_flow = DropboxOAuth2FlowNoRedirect(dpx_apikey, dpx_apisecret)
    authorize_url = auth_flow.start()
    print("1. Go to: " + authorize_url)
    print("2. Click \"Allow\" (you might have to log in first).")
    print("3. Copy the authorization code.")
    auth_code = input("Enter the authorization code here: ").strip()
    oauth_result = auth_flow.finish(auth_code)
    return oauth_result.access_token