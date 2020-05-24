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
        self.cred_filename = 'systems/vault/' + kwargs.get('credsFileName', "api_keys.json")
        self.authenticated = self._authenticate(self.cred_filename)
        self.user_name = ''

    def get_article_list(self):
        if self._authenticate():
            pass

    def _authenticate(self):
        self.code = ''
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Accept': 'application/json'}

        with open(self.cred_filename, 'r') as file:
            creds = json.load(file)
        # auth_url = "https://readitlaterlist.com/v2/get?{params}"
        print(">> Executing Pocket [Authentication] step 1 .. ")
        step_1_auth = "https://getpocket.com/v3/oauth/request?redirect_uri={redirect_uri}&consumer_key={consumer_key}"
        params = {
            "consumer_key": creds['pocket']['consumer_key'],
            "redirect_uri": creds['pocket']['redirect_uri']
        }
        auth_url = step_1_auth.format(consumer_key=params.get('consumer_key'), redirect_uri=params.get('redirect_uri'))
        response = requests.post(auth_url, verify=True)
        params['request_token'] = response.text.split('=')[1]
        print(">> [Authentication] step 1 done. ")

        print(">> Executing Pocket [Authentication] step 2 .. ")
        step_2_auth = "https://getpocket.com/auth/authorize?request_token={token}&redirect_uri={redirect_uri}".format(
            redirect_uri=params.get('redirect_uri'),
            token=params['request_token']
        )
        resp = requests.get(step_2_auth, verify=True)
        self.code = params['request_token']
        print(">> [Authentication] step 2 done. ")

        print(">> Executing Pocket [Authentication] step 3 .. ")
        step_3_auth = "https://getpocket.com/v3/oauth/authorize".format(
            redirect_uri=params.get('redirect_uri'),
            token=params['request_token']
        )
        resp = requests.get(step_3_auth, verify=True)
        response_code = resp.status_code

        if response_code not in [200, 201, 202, 204]:
            # print the actual error message
            resp.raise_for_status()

        print(">> [Authentication] step 3 done. ")
        # print(creds)

        # https://getpocket.com/developer/docs/authentications

        return True

    def is_authenticated(self):
        return self.authenticated

