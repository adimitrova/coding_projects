# import beautifulsoup4
import mkepub, re, json, dropbox, requests, urllib
from os import getcwd, path

from bs4 import BeautifulSoup


class Epubify(object):
    def __init__(self, **kwargs):
        self.url = kwargs.get('URL')
        self.file_path = kwargs.get('filePath')

    def fetch_html_text(self, url):
        response = requests.get(URL, verify=False)

        soup = BeautifulSoup(response.content, features="html.parser")

        # kill all script and style elements
        for element in soup(["script", "style", "meta", "footer", "img", "li", "ul"]):
            element.extract()  # rip it out

        print(">> Getting the text..")
        text = soup.get_text().strip('\n')
        return text

    def preprocess_text(self, text):
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines() if len(line) > 3)

        reg_ex = re.compile('(\[[0-9]+\]|\[[a-z]+\]|\[редактиране \| редактиране на кода\])')
        print(">> Processing the text..")
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        new_chunks = ""
        for ch in chunks:
            # check if occurrence of the pattern is found in the chunk
            if re.search(reg_ex, ch):
                match_chunk = re.sub(reg_ex, '', ch)
                if len(match_chunk.split(" ")) < 4:
                    # Ignore lines with few words, they are likely unrelated
                    pass
                elif len(match_chunk.split(" ")) < 15:
                    # Keep small lines / sentences, could be related, but separate them from main text to make them more visible.
                    new_chunks += "\n" + match_chunk
                else:
                    # add the actual text to the new_chunks string.
                    new_chunks += " " + match_chunk
            else:
                if len(ch.split(" ")) < 4:
                    # Ignore lines with few words, they are likely unrelated
                    pass
                elif len(ch.split(" ")) < 15:
                    # Keep small lines / sentences, could be related, but separate them from main text to make them more visible.
                    new_chunks += "\n" + ch
                else:
                    # add the actual text to the new_chunks string.
                    new_chunks += " " + ch

        # reg_ex = re.compile(r'(\[[0-9]+\]|\[[a-z]+\]|\[редактиране \| редактиране на кода\])')
        final_content = new_chunks
        final_content = re.sub(reg_ex, '', final_content)
        return final_content
        # TODO: Add more cleansing logic

    def save_epub(self, system):
        exec("from {system} import {systemclass}".format(system=system,
                                                            systemclass=system.capitalize()))
        system = system.capitalize()
        print(system.__dict__)

def main(URL, fileName):
    settings = {
        "URL": URL,
        "filePath": fileName
    }
    epubify = Epubify(**settings)
    # text = epubify.fetch_html_text(URL)
    # final_content = epubify.preprocess_text(text)
    epubify.save_epub('pocket')

    # ================================== prepare to save as epub ===============================

    # print(">> Done!")
    #
    # if file_name:
    #     title = file_name
    # else:
    #     raise AttributeError("You must enter the name for the file.")
    #
    # book = mkepub.Book(title=title, author='Article')
    #
    # book.add_page(title, final_content)
    # # print(f"\n========== CONTENT =========== {final_content} \n============== END OF CONTENT =============\n")
    #
    # if localPath:
    #     local_path = localPath + '/' + title + '.epub'
    # else:
    #     local_path = "{}/books/{}.epub".format(getcwd(), title)
    #
    # try:
    #     book.save(local_path)
    #     print(">> Saved (locally) at: {}".format(local_path))
    # except FileExistsError as err:
    #     print(">> A file with this name already exists at {}".format(local_path))

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
    main('https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell', 'test')
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
