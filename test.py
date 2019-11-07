import urllib2
import base64

class PreemptiveBasicAuthHandler(urllib2.HTTPBasicAuthHandler):


    '''Preemptive basic auth.

    Instead of waiting for a 403 to then retry with the credentials,
    send the credentials if the url is handled by the password manager.
    Note: please use realm=None when calling add_password.'''
    def http_request(self, req):
        url = req.get_full_url()
        realm = None
        # this is very similar to the code from retry_http_basic_auth()
        # but returns a request object.
        user, pw = self.passwd.find_user_password(realm, url)
        if pw:
            raw = "%s:%s" % (user, pw)
            auth = 'Basic %s' % base64.b64encode(raw).strip()
            req.add_unredirected_header(self.auth_header, auth)
        return req

    https_request = http_request


api_url = "http://api.foursquare.com/"
api_username = "johndoe"
api_password = "some-cryptic-value"

auth_handler = PreemptiveBasicAuthHandler()
auth_handler.add_password(
    realm=None, # default realm.
    uri=api_url,
    user=api_username,
    passwd=api_password)
opener = urllib2.build_opener(auth_handler)
urllib2.install_opener(opener)