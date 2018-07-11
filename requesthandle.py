from bs4 import BeautifulSoup
import requests
import datetime
from PyQt5.QtCore import QThread

class CustomThread(QThread):
    def __init__(self, target, callback, prop, args=()):
        super().__init__()
        self.__target = target
        self.finished.connect(lambda: callback(self, prop))
        if type(args) is not tuple:
            self.__args = tuple([args])
        else:
            self.__args = args
    def run(self):
        self.__target(*self.__args)

class RequestHandle:
    def __init__(self, MainWindow):
        self.MainWindow = MainWindow
        self.threads = {"searchMine":{}, "delete":{}, "searchOthers":{}} 
    
    def threadFinished(self, thread, prop):
        if thread in self.threads[prop]:
            self.threads[prop].pop(thread)

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
    
    def extractBoards(self, response):
        result = {}
        soup = BeautifulSoup(response, 'html.parser')
        boards = soup.find("div", {"id":"submenu"}).findAll("a", class_=lambda x: x!="search")
        for board in boards:
            result[board.getText()] = board["href"].replace("/", "")
        return result
            

    def searchMyArticles(self, number, articleList, threadCount):
        mult = 0
        while True:
            result = self.searchArticle("myarticle", threadCount*mult + number)
            if len(result) == 0:
                break
            articleList.extend(result)
            mult = mult+1
        
    def searchCommentedArticles(self, number, commentedList, threadCount):
        mult = 0
        while True:
            result = self.searchArticle("mycommentarticle", threadCount*mult + number)
            if len(result) == 0:
                break
            commentedList.extend(result)
            mult = mult+1

    def searchMyComments(self, number, commentedList, commentList, threadCount):
        for index in range(number, len(commentedList), threadCount):
            result = self.searchComment(commentedList[index])
            commentList.extend(result)
    
    def searchComment(self, article, nickname=None):
        data = {"id":article["id"], "limit_num":-1, "moiminfo":True}
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
        header["Content-Length"] = str(len("id={}&limit_num=-1&moiminfo=true".format(article["id"])))
        response = self.MainWindow.req.post("https://www.everytime.kr/find/board/comment/list", data=data, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        if nickname is None:
            result = list(map(lambda comment:{"article":article, "comment":comment}, soup.findAll("comment", {"is_mine":"1"})))
        else:
            result = list(map(lambda comment:{"article":article, "comment":comment}, soup.findAll("comment", {"user_nickname":nickname})))
        if "board_id" in article:
            for comment in result:
                comment["board"] = article["board_id"]
        return result

    def searchArticle(self, _id, page):
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
        if _id == "myarticle" or _id == "mycommentarticle":
            return soup.findAll("article")
        else:
            return list(map(lambda article:{"board":_id, "article":article}, soup.findAll("article")))
    
    def getMineTarget(self, threadCount):
        def threadedSearchMyArticles(articles):
            number = 0
            threads = []
            while number < threadCount:
                thread = CustomThread(self.searchMyArticles, self.threadFinished, "searchMine", (number, articles, threadCount))
                threads.append(thread)
                self.threads["searchMine"][thread] = thread
                number = number+1
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.wait()
        def threadedSearchMyCommentedArticles(commentedArticles):
            number = 0
            threads = []
            while number < threadCount:
                thread = CustomThread(self.searchCommentedArticles, self.threadFinished, "searchMine", (number, commentedArticles, threadCount))
                threads.append(thread)
                self.threads["searchMine"][thread] = thread
                number = number+1
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.wait()
        def threadedSearchMyComments(commentedArticles, comments):
            number = 0
            threads = []
            while number < threadCount:
                thread = CustomThread(self.searchMyComments, self.threadFinished, "searchMine", (number, commentedArticles, comments, threadCount))
                threads.append(thread)
                self.threads["searchMine"][thread] = thread
                number = number+1
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.wait()
        articles = []
        commentedArticles = []
        comments = []
        threadedSearchMyArticles(articles)
        threadedSearchMyCommentedArticles(commentedArticles)
        threadedSearchMyComments(commentedArticles, comments)
        
        # sorted(articles, key=lambda article:article["id"], reverse=True)
        # sorted(comments, key=lambda comment:comment["id"], reverse=True)
        self.MainWindow.mine = {"article":articles, "comment":comments}
        self.MainWindow.Slot.searchMineEndSignal.emit()
    
    def getMine(self):
        thread = CustomThread(self.getMineTarget, self.threadFinished, "searchMine", (self.MainWindow.threadCount))
        self.threads["searchMine"][thread] = thread
        thread.start()
    
    def deleteMyArticles(self, articles):
        header = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.everytime.kr/",
            "Accept-Language": "ko-KR",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Host": "www.everytime.kr",
            "Connection": "Keep-Alive",
            "Cache-Control": "no-cache"
        }
        for item in articles:
            header["Content-Length"] = str(len("id={}".format(item["id"])))
            response = self.MainWindow.req.post("https://www.everytime.kr/remove/board/article", data={"id":item["id"]})
            soup = BeautifulSoup(response.text, 'html.parser')
            if int(soup.find("response").text) == 1:
                string = "[글삭제] "
            else: 
                string = "[글삭제 실패] "
            if self.MainWindow.printIdFlag:
                string = string + item["id"]
            if self.MainWindow.printTextFlag:
                string = string + " " + Util.omitString(item["title"])
            self.MainWindow.Slot.addProgressSignal.emit(string)

    def deleteMyComments(self, comments):
        header = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "*/*",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://www.everytime.kr/",
            "Accept-Language": "ko-KR",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Host": "www.everytime.kr",
            "Connection": "Keep-Alive",
            "Cache-Control": "no-cache"
        }
        for item in comments:
            header["Content-Length"] = str(len("id={}".format(item["comment"]["id"])))
            response = self.MainWindow.req.post("https://www.everytime.kr/remove/board/comment", data={"id":item["comment"]["id"]})
            soup = BeautifulSoup(response.text, 'html.parser')
            if int(soup.find("response").text) == 1:
                string = "[댓글삭제] "
            else: 
                string = "[댓글삭제 실패] "
            if self.MainWindow.printIdFlag:
                string = string + item["comment"]["id"]
            if self.MainWindow.printTextFlag:
                string = string + " " + Util.omitString(item["comment"]["text"])
            if self.MainWindow.printOriginFlag:
                string = string + "\n" + "https://www.everytime.kr/{}/v/{}".format(item["board"], item["article"]["id"])
            self.MainWindow.Slot.addProgressSignal.emit(string)
           
    def deleteMineTarget(self, threadCount, option):
        def threadedDeleteMyArticles(articles):
            number = 0
            threads = []
            while number < threadCount:
                thread = CustomThread(self.deleteMyArticles, self.threadFinished, "delete", (articles[number::threadCount]))
                threads.append(thread)
                self.threads["delete"][thread] = thread
                number = number+1
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.wait()
        def threadedDeleteMyComments(comments):
            number = 0
            threads = []
            while number < threadCount:
                thread = CustomThread(self.deleteMyComments, self.threadFinished, "delete", (comments[number::threadCount]))
                threads.append(thread)
                self.threads["delete"][thread] = thread
                number = number+1
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.wait()
        result = Util.filterMine(self.MainWindow.mine, option)
        if option["articleFlag"]:
            threadedDeleteMyArticles(result["article"])
        if option["commentFlag"]:
            threadedDeleteMyComments(result["comment"])
        self.MainWindow.Slot.deleteEndSignal.emit()

    def deleteMine(self, option):
        thread = CustomThread(self.deleteMineTarget, self.threadFinished, "delete", (self.MainWindow.threadCount, option))
        self.threads["delete"][thread] = thread
        thread.start()
    
    def abortDelete(self):
        if len(self.threads["delete"]) > 0:
            for thread in list(self.threads["delete"]):
                thread.terminate()
                self.threadFinished(thread, "delete")
            return True
        else:
            return False

    def searchOthersArticlesAndComments(self, boardId, number, others, threadCount, option):
        mult = 0
        while mult*threadCount + number < option["page"]:
            articles = self.searchArticle(boardId, mult*threadCount + number)
            if option["commentFlag"]:
                for article in articles:
                    comments = self.searchComment(article["article"], option["nickname"])
                    for comment in comments:
                        comment["board"] = boardId
                    others["comment"].extend(comments)
            articles = list(filter(lambda article:article["article"]["user_nickname"] == option["nickname"], articles))
            if option["articleFlag"]:
                others["article"].extend(articles)
            mult = mult+1

    def searchOthersTarget(self, threadCount, option):
        def threadedSearch(boardId, others):
            number = 0
            threads = []
            while number < threadCount:
                thread = CustomThread(self.searchOthersArticlesAndComments, self.threadFinished, "searchOthers", (boardId, number, others, threadCount, option))
                threads.append(thread)
                self.threads["searchOthers"][thread] = thread
                number = number+1
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.wait()
        if option["articleFlag"]:
            self.MainWindow.others["article"] = []
        if option["commentFlag"]:
            self.MainWindow.others["comment"] = []
        for board, boardId in option["boards"].items():
            threadedSearch(boardId, self.MainWindow.others)
            if self.MainWindow.printBoardSearchEndFlag:
                self.MainWindow.Slot.addProgressSignal.emit("[System] {} 검색 완료".format(board))
        self.MainWindow.Slot.searchOthersEndSignal.emit()

    def searchOthers(self, option):
        thread = CustomThread(self.searchOthersTarget, self.threadFinished, "searchOthers", (self.MainWindow.threadCount, option))
        self.threads["searchOthers"][thread] = thread
        thread.start()

    def abortSearch(self):
        if len(self.threads["searchOthers"]) > 0:
            for thread in list(self.threads["searchOthers"]):
                thread.terminate()
                self.threadFinished(thread, "searchOthers")
            return True
        else:
            return False

class Util:
    @staticmethod
    def filterMine(mine, option):
        def filterArticle(articles):
            if option["minlikeFlag"]:
                articles = list(filter(lambda article:article["posvote"] < option["minlike"], articles))
            if option["mincommentFlag"]:
                articles = list(filter(lambda article:article["comment"] < option["minlike"], articles))
            if option["excludeArticleFlag"]:
                articles = list(filter(lambda article:not Util.checkIfWordIn(article, option["excludeWord"]), articles))
            if option["scope"] == "1일 내":
                articles = list(filter(lambda article:Util.checkDate(now, article["created_at"], 1), articles))
            elif option["scope"] == "1주 내":
                articles = list(filter(lambda article:Util.checkDate(now, article["created_at"], 7), articles))
            elif option["scope"] == "1달 내":
                articles = list(filter(lambda article:Util.checkDate(now, article["created_at"], 31), articles))
            elif option["scope"] == "1년 내":
                articles = list(filter(lambda article:Util.checkDate(now, article["created_at"], 365), articles))
            return articles
        def filterComment(comments):
            if option["excludeCommentFlag"]:
                comments = list(filter(lambda item:not Util.checkIfWordIn(item["comment"], option["excludeWord"]), comments))
            if option["scope"] == "1일 내":
                comments = list(filter(lambda item:Util.checkDate(now, item["comment"]["created_at"], 1), comments))
            elif option["scope"] == "1주 내":
                comments = list(filter(lambda item:Util.checkDate(now, item["comment"]["created_at"], 7), comments))
            elif option["scope"] == "1달 내":
                comments = list(filter(lambda item:Util.checkDate(now, item["comment"]["created_at"], 31), comments))
            elif option["scope"] == "1년 내":
                comments = list(filter(lambda item:Util.checkDate(now, item["comment"]["created_at"], 365), comments))
            return comments
        articles = []
        articles.extend(mine["article"])
        comments = []
        comments.extend(mine["comment"])
        result = {}
        now = datetime.datetime.now()
        if option["articleFlag"]:
            result["article"] = filterArticle(articles)
        if option["commentFlag"]:
            result["comment"] = filterComment(comments)
        return result

    @staticmethod
    def checkDate(now, date, offset):
        past = now - datetime.timedelta(days=offset)
        date = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        if past <= date:
            return True
        else:
            return False

    @staticmethod
    def checkIfWordIn(tag, words):
        if tag.name == "article":
            for word in words:
                if tag["title"].find(word) != -1 or tag["text"].find(word) != -1:
                    return True
        elif tag.name == "comment":
            for word in words:
                if tag["text"].find(word) != -1:
                    return True
        return False
    
    @staticmethod
    def omitString(string):
        if len(string) < 25:
            return string
        else:
            return "{}...".format(string[0:23])