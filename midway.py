import requests
from urllib.parse import urlparse
import logging
import http.cookiejar as cookielib
import re
import getpass
import os
 
logger=logging.getLogger()
 
MIDWAY_ENDPOINT = 'https://midway-auth.amazon.com'
USERNAME = getpass.getuser() 
COOKIE_FILE = os.path.expanduser("~") + '/.midway/cookie' 
 
def resp_info(response):
    return '{}:{}:{}:{}'.format(
        response.headers.get('x-host'),
        response.headers.get('x-request-id'),
        response.status_code,
        response.text)
 
def request_follow_redirects(session, url, headers, data, max_hops=10):
    if max_hops < 0:
        return False
    max_hops -= 1
    response = session.post(url, data=data, headers=headers , allow_redirects=False)
    if response.status_code == 302 or response.status_code == 307:
        return request_follow_redirects(session, response.headers['Location'], headers, data)
    else:
        return response
 
 
def test_isengard_hello(url):
    # If Sentry is used behind the service, you need to opt-in to Sentry to Midway flow,
    # This will add a cookie that will begin redirecting your subsequent authentication requests from Sentry to Midway.
    # https://w.amazon.com/index.php/Sentry/Regionalized%20Identity/Sentry%20To%20Midway     
    session = requests.Session()
    session.allow_redirects = False
    session.max_redirects = 5
    session.verify = "/etc/pki/tls/certs/ca-bundle.crt"
    response = session.post('https://sentry.amazon.com/sentry-braveheart?value=1')
    if not response.ok:
        print("sentry error")
        exit(0)         
    fd = open(COOKIE_FILE)
    for line in fd:
        elem = re.sub(r'^#HttpOnly_', '', line.rstrip()).split()
        if len(elem) == 7:
            cookie_obj = requests.cookies.create_cookie(domain=elem[0],name=elem[5],value=elem[6])
            session.cookies.set_cookie(cookie_obj)
    headers={'Accept': 'application/json',"Content-Type": "application/json; charset=UTF-8", "Content-Encoding": 'amz-1.0', "X-Amz-Target": "IsengardService.Hello"}
    return request_follow_redirects(session, url, headers=headers, data={})
   
 
response = test_isengard_hello("https://proxima-device-tracker.onrender.com/")
