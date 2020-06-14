import json
from sys import modules
# from .epubify import Epubify
from importlib import import_module

epubify = import_module(name="epubify", package="epubify")


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
        print(">> Questions, marked with \'*\' are required.")
        print(">> *Enter URL for the page to convert to epub, surrounded by quotes: ")
        url = input()

        print(">> Enter the name for the new book file: e.g. \'Harry Potter and the order of the phoenix\'")
        output_file_name = input()

        print(">> *Enter credentials file name, after placing it into the system/vault/ dir.")
        creds_path = input()

        print(">> Enter book author: ")
        author = input()

        print(">> *Enter book title: ")
        title = input()

        print(">> Enter \'local\' mode to save on the machine, or \'remote\' mode to save in a cloud system like dropbox: push ENTER to skip.. ")
        mode = input()

        print(">> Enter system (\'dropbox\' and \'pocket\' are currently supported): push ENTER to skip.. ")
        system = input()

        config_settings = {
            "URL": url,
            "title": title,
            "author": author,
            "credsFileName": creds_path,
            "mode": mode,
            "system": system,
            "filePath": output_file_name
        }

        return config_settings
    else:
        raise ValueError("Invalid choice. Please enter 1 or 2.")


def main():
    # settings = input_prompt()
    # TODO: Implement subdictionaries or list of items in order to have multiple books processed at once

    # settings = {
    #     "URL": "https://en.wikipedia.org/wiki/Chicxulub_crater",
    #     "title": 'Chicxulub_crater',
    #     "author": 'wikipedia',
    #     "credsFileName": "api_keys.json",
    #     "mode": "local",
    #     "filePath": "/home/adimitrova/DEVELOPMENT/Github/PERSONAL_REPOS"              # local file path
    # }

    settings = {
        "URL": "https://en.wikipedia.org/wiki/Chicxulub_crater",
        "title": 'Chicxulub_crater',
        "author": 'wikipedia',
        "credsFileName": "api_keys.json",
        "mode": "remote",
        "save_mode": "overwrite",      # not required, default - it won't override and will show a notification about it
        "system": "dropbox",                # only if mode is remote
        "filePath": "/home/adimitrova/DEVELOPMENT/Github/PERSONAL_REPOS"        # remote file path, if omitted - save to root
    }

    epub = epubify.Epubify(**settings)
    # Note: Cascading/Chaining method calls - SO COOOOOL BRO!!!!!!!!!
    ebook = epub.fetch_html_text().preprocess_text().create_book()
    epub.save_book(book=ebook, mode='remote', sys='dropbox')


if __name__ == '__main__':
    # TODo: CREATE AN EXECUTABLE with pyinstaller
    # https://realpython.com/pyinstaller-python/#preparing-your-project
    main()

    # https://stackoverflow.com/questions/1325581/how-do-i-check-if-im-running-on-windows-in-python
    # https://medium.com/dreamcatcher-its-blog/making-an-stand-alone-executable-from-a-python-script-using-pyinstaller-d1df9170e263
