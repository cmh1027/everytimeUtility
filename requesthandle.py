from bs4 import BeautifulSoup
import requests
from PyQt5.QtCore import QThread
class CustomThread(QThread):
    def __init__(self, target, args=()):
        super().__init__()
        self.__target = target
        self.__args = args
    
    def run(self):
        self.__target(*self.__args)

class RequestHandle:
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow

    def login(self, _id, password):
        data = {"redirect":"/"}
        data["userid"] = _id
        data["password"] = password
        header = {
            "Accept": "text/html, application/xhtml+xml, image/jxr, */*",
            "Referer": "https://www.everytime.kr/",
            "Accept-Language": "ko-KR",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "www.everytime.kr",
            "Connection": "Keep-Alive",
            "Cache-Control": "no-cache"
        }
        header["Content-Length"] = str(len("userid={}&password={}&redirect=%2F".format(data["userid"], data["password"])))
        response = self.MainWindow.req.post("https://www.everytime.kr/user/login", data=data, headers=header, verify=False)
        if response.text.find('<p class="nickname">') == -1:
            return False
        else:
            return response.text
        
    def searchMyArticles(self, number, articleList):
        mult = 0
        while True:
            result = self.search("myarticle", self.MainWindow.threadCount*mult + number)
            if len(result) == 0:
                break
            articleList.extend(result)
            mult = mult+1
        
    
    def searchMyComments(self, number, commentList):
        mult = 0
        while True:
            result = self.search("mycommentarticle", self.MainWindow.threadCount*mult + number)
            if len(result) == 0:
                break
            commentList.extend(result)
            mult = mult+1
    
    def search(self, _id, page):
        data = {"id":_id, "limit_num":20, "start_num":page*20}
        header = {
            "Accept": "text/html, application/xhtml+xml, image/jxr, */*",
            "Referer": "https://www.everytime.kr/",
            "Accept-Language": "ko-KR",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Content-Type": "application/x-www-form-urlencoded",
            "Host": "www.everytime.kr",
            "Connection": "Keep-Alive",
            "Cache-Control": "no-cache"
        }
        header["Content-Length"] = str(len("id={}&limit_num=20&start_num={}".format(_id, page*20)))
        response = self.MainWindow.req.post("https://www.everytime.kr/find/board/article/list", data=data, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.findAll("article")
    
    def getMineTarget(self):
        number = 0
        threads = []
        articles = []
        comments = []
        while number < self.MainWindow.threadCount:
            thread = CustomThread(self.searchMyArticles, (number, articles))
            threads.append(thread)
            thread = CustomThread(self.searchMyComments, (number, comments))
            threads.append(thread)
            number = number+1
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.wait()
        # sorted(articles, key=lambda article:article["id"], reverse=True)
        # sorted(comments, key=lambda comment:comment["id"], reverse=True)
        self.MainWindow.mine = {"article":articles, "comment":comments}
        self.MainWindow.Slot.searchEndSignal.emit()
    
    def getMine(self):
        self.thread = CustomThread(self.getMineTarget)
        self.thread.start()