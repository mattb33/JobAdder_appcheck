"""
Example of OAuth 2.0 process with web server.
API of facebook is used: https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow
"""

import webbrowser
import urllib2
import json
from urllib import urlencode
from urlparse import parse_qsl, urlparse
import random

PROVIDER = 'jobadder'


if PROVIDER == 'jobadder':
    # JOBADDER
    CLIENT_KEY = 'your_app_key'
    CLIENT_SECRET = 'your_app_secret'
    CALLBACK_URL = "http://rrhosterer.com:8000/complete/google-oauth2/"

    AUTHORIZE_URL = 'https://id.jobadder.com/connect/authorize' 
    ACCESS_TOKEN_URL = 'https://id.jobadder.com/connect/token' 
    API_RESOURCE_URL = 'https://www.googleapis.com/oauth2/v1/userinfo'

##########################
# STEP 1: user cofirmation
##########################

auth_params = {
    "client_id": CLIENT_KEY,
    "state": str(random.getrandbits(64)),  # to protect from CSRF
    "redirect_uri": CALLBACK_URL,
    "scope": "email",  # we want to get access to email
    "response_type": "code",
}

url = "?".join([AUTHORIZE_URL, urlencode(auth_params)])
print url
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
if 'google' in ACCESS_TOKEN_URL:
    # google requires 'grant_type' param
    access_token_params['grant_type'] = 'authorization_code'
# send POST request. Facebook and VK also ok with GET, but google only POST
resp = urllib2.urlopen(ACCESS_TOKEN_URL, data=urlencode(access_token_params))
assert resp.code == 200
resp_content = json.loads(resp.read())
access_token = resp_content['access_token']
print "access_token", access_token

####################################
# STEP 3: request to server resource
####################################
api_params = {
    'access_token': access_token,
}
url = "?".join([API_RESOURCE_URL, urlencode(api_params)])
resp = urllib2.urlopen(url)
assert resp.code == 200
resp_content = json.loads(resp.read())
email = resp_content.get('email')
print "Email:", email
print "All params:", resp_content