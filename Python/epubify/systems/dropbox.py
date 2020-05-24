import dropbox

class Dropbox(object):
    def __init__(self, **kwargs):
        self.cred_filename = kwargs.get('credentials_file', "vault/api_keys.json")
