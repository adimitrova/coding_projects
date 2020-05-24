from .epubify import Epubify
import json

def input_prompt():
    print(">> We will ask you for input. If you would rather have a config file, press 1, for manual input, press 2")
    mode = int(input())
    if mode == 1:
        print(">> Enter config file name, after placing it into system/vault/ dir.")
        config_file_name = input()
        with open(config_file_name, 'r') as file:
            config_settings = json.load(file)
        return config_settings
    elif mode == 2:
        print(">> Questions, marked with\'*\' are required.")
        print(">> *Enter URL for the page to convert to epub: ")
        url = input()

        print(">> *Enter the name for the new book file: e.g. \'Harry Potter and the order of the phoenix\'")
        output_file_name = input()

        print(">> *Enter credentials file name, after placing it into the system/vault/ dir.")
        creds_path = input()

        print(">> Enter book author: ")
        author = input()

        config_settings = {
            "url": url,
            "filePath": output_file_name,
            "credsFileName": creds_path,
            "author": author
        }
        return config_settings
    else:
        raise ValueError("Invalid choice. Please enter 1 or 2.")

def main():
    # input_prompt()

    settings = {
        "URL": 'someURL',
        "title": 'harry potter',
        "author": 'j.k.rowling',
        "credsFileName": None
    }

    epubify = Epubify(**settings)
    # text = epubify.fetch_html_text()
    # book_content = epubify.preprocess_text(text)
    # source_system = Epubify.system_import('pocket')
    # target_system = Epubify.system_import('dropbox')
    # epubify.create_book(book_content)


    # ================================== Save to dropbox ===============================

    # dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)
    #
    # if dropboxPath:
    #     dropbox_path = dropboxPath
    # else:
    #     dropbox_path = ''   # root folder
    #
    # try:
    #     with open(local_path, "rb") as file:
    #         print(">> Uploading file: [{}] to Dropbox at: [{}]".format(local_path, dropbox_path))
    #         dbx.files_upload(file.read(), dropbox_path, mute=True)
    # except TypeError:
    #     print("Expecting bytes data as input for the upload on dropbox.")

    # TODO: Custom saving location
    # TODO: Save to dropbox..


if __name__ == '__main__':
    # _authenticate()
    main()
    # while True:
    #     creds_file_path = path.abspath(path.join(__file__, "../../.."))+"/credentials.json"
    #
    #     # with open(creds_file_path) as creds_file:
    #     #     creds_content = json.load(creds_file)
    #     print("------------")
    #     url = input("URL of the article: ")
    #
    #     # url = "https://getpocket.com/redirect?url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FFinal_Solution&formCheck=bf15d6ab03876623dc234496a40b4ccb"
    #
    #     # dropbox_token = input("Create a dropbox app and paste the access token here: ")
    #     # dropbox_token = creds_content['epubify']['access_token']
    #
    #     # save_path = input("Enter linux-like path where the file will be saved: ")
    #     file_name = input("File name: ")
    #
    #     # epubify(url, file_name, dropbox_token, dropbox_path)
    #     epubify(url, file_name)

# https://stackoverflow.com/questions/1325581/how-do-i-check-if-im-running-on-windows-in-python
# https://medium.com/dreamcatcher-its-blog/making-an-stand-alone-executable-from-a-python-script-using-pyinstaller-d1df9170e263
