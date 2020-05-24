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
    }

    epub = epubify.Epubify(**settings)
    # text = epub.fetch_html_text()
    # book_content = epub.preprocess_text(text)
    # source_system = epub.system_import('pocket')
    # target_system = epub.system_import('dropbox')
    # epub.create_book(book_content)
    # target_system.save()


if __name__ == '__main__':
    main()

    # https://stackoverflow.com/questions/1325581/how-do-i-check-if-im-running-on-windows-in-python
    # https://medium.com/dreamcatcher-its-blog/making-an-stand-alone-executable-from-a-python-script-using-pyinstaller-d1df9170e263
