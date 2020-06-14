# import beautifulsoup4
import mkepub, re, json, dropbox, requests, urllib
from os import getcwd, path
from bs4 import BeautifulSoup
import urllib3
from importlib import import_module

ascii_art = import_module(name="ascii_art", package="epubify")


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Epubify(object):
    # TODO: replace all prints with logger
    def __init__(self, **kwargs):
        self.settings = kwargs
        self.url = kwargs.get('URL').strip("\"").strip("\'")
        self.title = kwargs.get('title')
        self.author = kwargs.get('author')
        self.system = kwargs.get("system")
        self.mode = kwargs.get("mode", None)
        self.file_path = kwargs.get('filePath', None)
        self.book_content = ""      # initial state of the text is empty, gets replaces in fetch_html_text()

        if not self.mode and not self.file_path:
            # set local filepath
            self.file_path = kwargs.get('filePath', '%s/books/%s.epub' % (getcwd(), self.title))
        elif self.mode == "remote" and not self.file_path:
            self.file_path = None
        elif self.mode == "remote" and self.file_path:
            assert not str(self.file_path).endswith('.epub')
            self.file_path = kwargs.get('filePath') + '%s.epub' % self.title
        elif self.file_path is not None and self.mode == 'local':
            from os import mkdir
            try:
                mkdir(self.file_path + '/books/')
            except FileExistsError:
                pass
            self.file_path = self.file_path + '/books/%s.epub' % self.title

        # update filePath to the dict which will be passed onto the save_book method
        self.settings['filePath'] = self.file_path

        print(">> The book will be saved at: \n[%s] " % self.file_path)

    def fetch_html_text(self):
        response = requests.get(self.url, verify=False)

        soup = BeautifulSoup(response.content, features="html.parser")

        # kill all script and style elements
        # TODO: Add a check for text in the "meta" element and fetch the text
        for element in soup(["script", "style", "meta", "footer", "img", "li", "ul"]):
            element.extract()  # rip it out

        print(">> Getting the HTML content..")
        text = soup.get_text().strip('\n')
        print(">> HTML content fetched and stored safely.")
        self.book_content = text
        return self     # Note: Enables chaining of another method after this one. (called cascading)

    def preprocess_text(self):
        # TODO: Add more cleansing logic
        # TODO: break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in self.book_content.splitlines() if len(line) > 3)

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
        print(">> HTML content processed and saved.")
        self.book_content = final_content
        return self

    @staticmethod
    def system_import(sys, **kwargs):
        module_name = 'drop_box' if sys == 'dropbox' else sys.lower()
        try:
            from importlib import import_module
            class_ = getattr(import_module("systems.%s" % module_name), sys.capitalize())
            system_instance = class_(**kwargs)
        except ImportError as e:
            print(e)

        return system_instance

    def create_book(self):
        book = mkepub.Book(title=self.title, author=self.author)
        book.add_page(self.title, self.book_content)
        return book

    def save_book(self, book, mode='local', sys=None):
        if self.mode == 'local':
            # save on local machine
            try:
                book.save(self.file_path)
                print(">> Saved (locally) at: {}".format(self.file_path))

            except FileExistsError as err:
                print(">> A file with this name already exists at [{}]. \nOVERRIDE? (y/n)".format(self.file_path))
                override = input()
                if override == 'y':
                    print(">> Overriding the book")
                    from os import remove
                    remove(self.file_path)
                    book.save(self.file_path)
                else:
                    print(">> Skip saving the book..")
                    pass
        elif self.mode == 'remote':
            # TODO: save to system (pocket, dropbox etc)
            print(">> Saving to system %s" % sys)
            target_system = self.system_import(sys, **self.settings)
            target_system.save_book(book)
        print(">> Done!")
        print(ascii_art.llama_small)
