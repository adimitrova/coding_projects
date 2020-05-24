import json, requests

class Pocket(object):
    """
    Class to connect to the Pocket app, retrieve the user's article list,
    retrieve their original URLs
    in order for Epubify to convert the original URLs into epub files
    """
    def __init__(self, **kwargs):
        """
        The constructor receives a keyword argument list, which
        will be used to fetch information about the Pocket app,
        credential file path etc
        :param kwargs: keyword arguments
        """
        self.cred_filename = kwargs.get('credentials_file', "vault/api_keys.json")
        self.authenticated = self._authenticate(self.cred_filename)

    def get_article_list(self):
        if self._authenticate():
            pass

    def _authenticate(self, cred_filename):
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Accept': 'application/json'}

        with open(cred_filename, 'r') as file:
            creds = json.load(file)
        # auth_url = "https://readitlaterlist.com/v2/get?{params}"
        step_1_auth = "https://getpocket.com/v3/oauth/request?redirect_uri={redirect_uri}&consumer_key={consumer_key}"
        params = {
            "consumer_key": creds['pocket']['consumer_key'],
            "redirect_uri": creds['pocket']['redirect_uri']
        }
        auth_url = step_1_auth.format(consumer_key=params.get('consumer_key'), redirect_uri=params.get('redirect_uri'))
        response = requests.post(auth_url, verify=True)
        params['request_token'] = response.text.split('=')[1]

        step_2_auth = "https://getpocket.com/auth/authorize?request_token={token}&redirect_uri={redirect_uri}".format(
            redirect_uri=params.get('redirect_uri'),
            token=params['request_token']
        )
        resp = requests.get(step_2_auth, verify=True)

        print("code: {}".format(params['request_token']))

        step_3_auth = "https://getpocket.com/v3/oauth/authorize".format(
            redirect_uri=params.get('redirect_uri'),
            token=params['request_token']
        )
        resp = requests.get(step_3_auth, verify=True)
        print(resp)
        # print(creds)

        # https://getpocket.com/developer/docs/authentications

        return True
