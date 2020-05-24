import dropbox
import json


class Dropbox(object):
    def __init__(self, **kwargs):
        self.cred_filename = 'systems/vault/' + kwargs.get('credsFileName', "api_keys.json")
        self.token = self._fetch_token_from_cred_file(self.cred_filename)
        self.dropbox_client = dropbox.Dropbox(oauth2_access_token=self.token)
        self.output_file_path = kwargs.get('filePath', '')      # if no filePath, save to root

    def _fetch_token_from_cred_file(self, cred_filename):
        with open(cred_filename, 'r') as file:
            creds = json.load(file).get('dropbox')

        return creds['access_token']

    def save(self):
        # ================================== Save to dropbox ===============================

        dbx = dropbox.Dropbox(self.token)

        try:
            with open(local_path, "rb") as file:
                print(">> Uploading file: [{}] to Dropbox at: [{}]".format(local_path, self.output_file_path))
                dbx.files_upload(file.read(), self.output_file_path, mute=True)
        except TypeError:
            print(">> Expecting bytes data as input for the upload on dropbox.")

        # TODO: Custom saving location
        # TODO: Save to dropbox..
