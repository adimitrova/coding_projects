import json
from sys import modules
# from .epubify import Epubify
from importlib import import_module

epubify = import_module(name="epubify", package="epubify")
ascii_art = import_module(name="ascii_art", package="epubify")


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

    settings = {
        "URL": "https://www.ranker.com/list/mummy-museum-guanajuato-mexico/genevieve-carlton",
        "title": 'Guanajuato_mummies',
        "author": 'article',
        "credsFileName": "api_keys.json",
        "mode": "local",
        "system": "dropbox",
        "filePath": "/home/adimitrova/DEVELOPMENT/Github/PERSONAL_REPOS/"
    }

    epub = epubify.Epubify(**settings)
    text = epub.fetch_html_text()
    book_content = epub.preprocess_text(text)
    ebook = epub.create_book(book_content)
    epub.save_book(book=ebook, mode='remote', sys='dropbox')

    print(ascii_art.llama_small)


if __name__ == '__main__':
    main()

    # https://stackoverflow.com/questions/1325581/how-do-i-check-if-im-running-on-windows-in-python
    # https://medium.com/dreamcatcher-its-blog/making-an-stand-alone-executable-from-a-python-script-using-pyinstaller-d1df9170e263
