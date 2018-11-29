##########################
#  Import Modules
##########################

import webbrowser
import urllib2
import json
from urllib import urlencode
from urlparse import parse_qsl, urlparse
import random

# JOBADDER DETAILS
PROVIDER = 'jobadder'  
CLIENT_KEY = 'your_app_key'
CLIENT_SECRET = 'your_app_secret'
CALLBACK_URL = "http://rrhosterer.com:8000/complete/google-oauth2/"  ## Update

AUTHORIZE_URL = 'https://id.jobadder.com/connect/authorize' 
ACCESS_TOKEN_URL = 'https://id.jobadder.com/connect/token' 
API_RESOURCE_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'   ## Update

##########################
# STEP 1: user cofirmation
##########################


auth_params = {
    'response_type': 'code required',
    'client_id': CLIENT_KEY,
    'scope': 'permission to request',
    'redirect_uri': CALLBACK_URL,
    'state': str(random.getrandbits(64)),  # 'unique string to be passed back optional'
} 


url = "?".join([AUTHORIZE_URL, urlencode(auth_params)])
print(url)
webbrowser.open_new_tab(url)
redirected_url = raw_input("Paste here url you were redirected:\n")
redirect_params = dict(parse_qsl(urlparse(redirected_url).query))
assert redirect_params['state'] == auth_params['state']  # protect CSRF
auth_code = redirect_params['code']
print "auth_code", auth_code

######################
# STEP 2: access token
######################
access_token_params = {
    "client_id": CLIENT_KEY,
    "redirect_uri": CALLBACK_URL,
    "client_secret": CLIENT_SECRET,
    "code": auth_code,
}

resp = urllib2.urlopen(ACCESS_TOKEN_URL, data=urlencode(access_token_params))
assert resp.code == 200
resp_content = json.loads(resp.read())
access_token = resp_content['access_token']
print "access_token", access_token