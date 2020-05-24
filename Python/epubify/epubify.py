# import beautifulsoup4
import mkepub, re, json, dropbox, requests, urllib
from os import getcwd, path

from bs4 import BeautifulSoup

class Epubify(object):
    # TODO: replace all prints with logger
    def __init__(self, **kwargs):
        self.url = kwargs.get('URL')
        self.file_path = kwargs.get('filePath', None)
        self.title = kwargs.get('title')
        self.author = kwargs.get('author')

        if not self.file_path:
            print("No filePath provided, the name of the title will be used as file name "
                  "and the book will be saved in %s/%s.epub" % (getcwd(), self.title))

    def fetch_html_text(self):
        response = requests.get(self.url, verify=False)

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

    @staticmethod
    def system_import(sys):
        try:
            import_system = lambda class_name: getattr(
                __import__("systems.{}".format(class_name.lower()), locals(), globals(), [class_name]),
                class_name,
            )
        except ImportError as e:
            # Display error message
            print(e)

        return import_system(sys.capitalize())

    def create_book(self, book_text):
        book = mkepub.Book(title=self.title, author=self.author)

        book.add_page(self.title, book_text)
        # print(f"\n========== CONTENT =========== {final_content} \n============== END OF CONTENT =============\n")

        local_path = "{}/books/{}.epub".format(getcwd(), self.title)

        return book

    def save_book(self, to_system, book, mode='local'):
        if mode == 'local':
            # save on local machine
            try:
                book.save(self.file_path)
                print(">> Saved (locally) at: {}".format(self.file_path))

            except FileExistsError as err:
                print(">> A file with this name already exists at {}".format(self.file_path))


if __name__ == '__main__':
    settings = {
        "URL": 'someURL',
        "title": 'harrypotter',
        "author": 'j.k.rowling',
        "credsFileName": None
    }

    epubify = Epubify(**settings)
    system = Epubify.system_import('pocket')
    print(system.__dict__)
    system.set_username(username='ani')
    print(system.get_username())