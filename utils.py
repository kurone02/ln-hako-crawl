from time import sleep
import requests
from bs4 import BeautifulSoup, ResultSet
import urllib
import wget


class Chapter():
    
    def __init__(self, title, link) -> None:
        self.title = title
        self.link = link

    def __str__(self) -> str:
        return f"Title = {self.title}\nLink = {self.link}"


class Utils():
    
    def __init__(self) -> None:
        self.ROOT_WEBSITE = "https://ln.hako.re"
        self.list_of_all_chapters = []
        page = requests.get(f"{self.ROOT_WEBSITE}/truyen/12096-ore-no-kurasu-ni-wakagaetta-motoyome-ga-iru")
        soup = BeautifulSoup(page.content, 'html.parser')
        chapters = soup.find_all(["div"], class_ = "chapter-name")
        for chapter in chapters:
            chapter_details = chapter.find("a")
            self.list_of_all_chapters.append(
                Chapter(
                    title = chapter_details.contents[0],
                    link = chapter_details["href"]
                )
            )

    def get_number_of_chapters(self) -> int:
        return len(self.list_of_all_chapters)

    def get_all_chapters(self) -> list:
        return self.list_of_all_chapters
    
    def get_title_chapter(self, chapter_id) -> str:
        return self.list_of_all_chapters[chapter_id].title

    def get_content_chapter(self, chapter_id) -> ResultSet:
        chapter_link = self.list_of_all_chapters[chapter_id].link
        page = requests.get(f"{self.ROOT_WEBSITE}{chapter_link}")
        soup = BeautifulSoup(page.content, 'html.parser')
        content = soup.find("div", id = "chapter-content")
        return content.find_all(["p"])
    
    def get_note_chapter(self, chapter_id) -> ResultSet:
        chapter_link = self.list_of_all_chapters[chapter_id].link
        page = requests.get(f"{self.ROOT_WEBSITE}{chapter_link}")
        soup = BeautifulSoup(page.content, 'html.parser')
        content = soup.find("div", id = "chapter-content")
        return content.find_all(["p"])

    def down_load_img(self, url, name):

        opener = urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Linux x86_64)')]
        urllib.request.install_opener(opener)
        print(url)
        urllib.request.urlretrieve(url = url, filename = f"{name}.jpg")
