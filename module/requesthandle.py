from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib3
import requests
import datetime
from urllib import parse
import time
from PyQt5.QtCore import QObject, QThread, pyqtSignal
from model.config import Config
from model.data import Data

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

class RequestHandle(QObject):
    progress = pyqtSignal(str)
    searchMineEnd = pyqtSignal()
    deleteEnd = pyqtSignal()
    searchOthersEnd = pyqtSignal()
    plasterEnd = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.threads = {"searchMine":{}, "delete":{}, "searchOthers":{}, "plaster":{}}
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        with requests.Session() as self.req:
            retry = Retry(connect=4, backoff_factor=0.3)
            adapter = HTTPAdapter(max_retries=retry)
            self.req.mount('https://everytime.kr', adapter)
    
    def threadFinished(self, thread, prop):
        if thread in self.threads[prop]:
            self.threads[prop].pop(thread)

    def login(self, _id, password):
        data = {"redirect":"/"}
        data["userid"] = _id
        data["password"] = password
        header = {
            "Host": "everytime.kr",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Origin": "https://everytime.kr",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "Sec-Fetch-Mode": "cors",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Sec-Fetch-Site": "same-origin",
            "Referer": "https://everytime.kr/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        header["Content-Length"] = str(len("userid={}&password={}&redirect=%2F".format(data["userid"], data["password"])))
        response = self.req.post("https://everytime.kr/user/login", data=data, headers=header, verify=False)
        if response.text.find('<p class="nickname">') == -1:
            return False
        else:
            return response.text
    
    def logout(self):
        header = {
            "Host": "everytime.kr",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Origin": "https://everytime.kr",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "Sec-Fetch-Mode": "cors",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Sec-Fetch-Site": "same-origin",
            "Referer": "https://everytime.kr/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        self.req.get("https://everytime.kr/user/logout", headers=header)
    
    def extractBoards(self, response):
        result = {}
        soup = BeautifulSoup(response, 'html.parser')
        boards = soup.find("div", {"id":"submenu"}).findAll("a", class_=lambda x: x!="search")
        for board in boards:
            if board.has_attr("href"):
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
    
    def searchComment(self, article, option=None):
        data = {"id":article["id"], "limit_num":-1, "moiminfo":True}
        header = {
            "Host": "everytime.kr",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Origin": "https://everytime.kr",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "Sec-Fetch-Mode": "cors",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Sec-Fetch-Site": "same-origin",
            "Referer": "https://everytime.kr/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        header["Content-Length"] = str(len("id={}&limit_num=-1&moiminfo=true".format(article["id"])))
        response = self.req.post("https://everytime.kr/find/board/comment/list", data=data, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        if option is None:
            result = list(map(lambda comment:{"article":article, "comment":comment}, soup.findAll("comment", {"is_mine":"1"})))
        else:
            if option["all"]:
                result = list(map(lambda comment:{"article":article, "comment":comment}, soup.findAll(lambda tag:tag.name=="comment" and tag["id"] != "0")))
            else:
                result = list(map(lambda comment:{"article":article, "comment":comment}, soup.findAll("comment", {"user_nickname":option["nickname"]})))
            if option["commentKeywordFlag"]:
                result = list(filter(lambda comment:option["commentKeyword"] in comment["comment"]["text"], result))
        if "board_id" in article:
            for comment in result:
                comment["board"] = article["board_id"]
        return result

    def searchArticle(self, _id, page, option=None):
        data = {"id":_id, "limit_num":20, "start_num":page*20}
        header = {
            "Host": "everytime.kr",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Origin": "https://everytime.kr",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "Sec-Fetch-Mode": "cors",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Sec-Fetch-Site": "same-origin",
            "Referer": "https://everytime.kr/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        header["Content-Length"] = str(len("id={}&limit_num=20&start_num={}".format(_id, page*20)))
        response = self.req.post("https://everytime.kr/find/board/article/list", data=data, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        if option is None:
            return soup.findAll("article")
        else:
            if option["articleKeywordFlag"]:
                return list(map(lambda article:{"board":_id, "article":article}, soup.findAll("article")))
            else:
                return list(map(lambda article:{"board":_id, "article":article}, soup.findAll("article")))

    def postComment(self, article, string, isAnonym):
        header = {
            "Host": "everytime.kr",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Origin": "https://everytime.kr",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "Sec-Fetch-Mode": "cors",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Sec-Fetch-Site": "same-origin",
            "Referer": "https://everytime.kr/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        header["Content-Length"] = str(len("text={}&is_anonym={}&id={}".format(parse.quote(string.encode('utf-8')), int(isAnonym), article["id"]))) 
        data = {"text":string.encode('utf-8'), "is_anonym":"1", "id":article["id"]}
        response = self.req.post("https://everytime.kr/save/board/comment", data=data, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        return int(soup.find("response").text)

    def postSubcomment(self, comment, string, isAnonym):
        header = {
            "Host": "everytime.kr",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Origin": "https://everytime.kr",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "Sec-Fetch-Mode": "cors",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Sec-Fetch-Site": "same-origin",
            "Referer": "https://everytime.kr/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        header["Content-Length"] = str(len("text={}&is_anonym={}&comment_id={}".format(parse.quote(string.encode('utf-8')), int(isAnonym), comment["id"])))  
        data = {"text":string.encode('utf-8'), "is_anonym":"1", "comment_id": comment["id"]}
        response = self.req.post("https://everytime.kr/save/board/comment", data=data, headers=header)
        soup = BeautifulSoup(response.text, 'html.parser')
        return int(soup.find("response").text)

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
        Data.mine = {"article":articles, "comment":comments}
        self.progress.emit("[System] 검색 완료")
        self.searchMineEnd.emit()
    
    def getMine(self):
        thread = CustomThread(self.getMineTarget, self.threadFinished, "searchMine", (Config.All.threadCount))
        self.threads["searchMine"][thread] = thread
        thread.start()
    
    def deleteArticle(self, _id):
        header = {
            "Host": "everytime.kr",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Origin": "https://everytime.kr",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "Sec-Fetch-Mode": "cors",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Sec-Fetch-Site": "same-origin",
            "Referer": "https://everytime.kr/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        header["Content-Length"] = str(len("id={}".format(_id)))
        response = self.req.post("https://everytime.kr/remove/board/article", data={"id":_id})
        soup = BeautifulSoup(response.text, 'html.parser')
        if int(soup.find("response").text) == 1:
            return True
        else: 
            return False

    def deleteComment(self, _id):
        header = {
            "Host": "everytime.kr",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Origin": "https://everytime.kr",
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
            "Sec-Fetch-Mode": "cors",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Sec-Fetch-Site": "same-origin",
            "Referer": "https://everytime.kr/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
        }
        header["Content-Length"] = str(len("id={}".format(_id)))
        response = self.req.post("https://everytime.kr/remove/board/comment", data={"id":_id})
        soup = BeautifulSoup(response.text, 'html.parser')
        if int(soup.find("response").text) == 1:
            return True
        else: 
            return False

    def deleteMyArticles(self, articles, number, threadCount, articleLen):
        for index, item in enumerate(articles):
            response = self.deleteArticle(item["id"])
            if response:
                string = "[글삭제] "
            else: 
                string = "[글삭제 실패] "
            if Config.Delete.printIdFlag:
                string += item["id"]
            if Config.Delete.printTextFlag:
                string += " " + Util.omitString(item["title"])
            if Config.Delete.printOriginFlag:
                string += "\n" + "https://everytime.kr/{}/v/{} ".format(item["board_id"], item["id"])
            else:
                string += "\n"
            string += "{}/{}".format(number + threadCount * index + 1, articleLen)
            self.progress.emit(string)

    def deleteMyComments(self, comments, number, threadCount, commentLen):
        for index, item in enumerate(comments):
            response = self.deleteComment(item["comment"]["id"])
            if response == 1:
                string = "[댓글삭제] "
            else: 
                string = "[댓글삭제 실패] "
            if Config.Delete.printIdFlag:
                string += item["comment"]["id"]
            if Config.Delete.printTextFlag:
                string += " " + Util.omitString(item["comment"]["text"])
            if Config.Delete.printOriginFlag:
                string += "\n" + "https://everytime.kr/{}/v/{} ".format(item["article"]["board_id"], item["article"]["id"])
            else:
                string += "\n"
            string += "{}/{}".format(number + threadCount * index + 1, commentLen)
            self.progress.emit(string)
           
    def deleteMineTarget(self, threadCount, option):
        def threadedDeleteMyArticles(articles):
            number = 0
            threads = []
            while number < threadCount:
                thread = CustomThread(self.deleteMyArticles, self.threadFinished, "delete", (articles[number::threadCount], number, threadCount, len(articles)))
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
                thread = CustomThread(self.deleteMyComments, self.threadFinished, "delete", (comments[number::threadCount], number, threadCount, len(comments)))
                threads.append(thread)
                self.threads["delete"][thread] = thread
                number = number+1
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.wait()
        result = Util.filterMine(Data.mine, option)
        if option["articleFlag"]:
            threadedDeleteMyArticles(result["article"])
        if option["commentFlag"]:
            threadedDeleteMyComments(result["comment"])
        self.progress.emit("[System] 삭제 완료")
        self.deleteEnd.emit()
        

    def deleteMine(self, option):
        thread = CustomThread(self.deleteMineTarget, self.threadFinished, "delete", (Config.All.threadCount, option))
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
        page = option["page"] - 1 + mult*threadCount + number
        while page <= option["pageEnd"] - 1:
            articles = self.searchArticle(boardId, page, option)
            if option["commentFlag"]:
                for article in articles:
                    comments = self.searchComment(article["article"], option)
                    for comment in comments:
                        comment["board"] = boardId
                    others["comment"].extend(comments)
                
            if not option["all"]:
                articles = list(filter(lambda article:article["article"]["user_nickname"] == option["nickname"], articles))
            if option["articleKeywordFlag"]:
                articles = list(filter(lambda article:option["articleKeyword"] in article["article"]["title"] or \
                option["articleKeyword"] in article["article"]["text"], articles))
            if option["articleFlag"]:
                others["article"].extend(articles)
            if Config.Search.printBoardSearchEndFlag and (page) % 10 == 0 and (page) > 0 :
                self.progress.emit("[System] {} 페이지 검색 완료".format(page))
            mult = mult+1
            page = option["page"] - 1 + mult*threadCount + number

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
            Data.others["article"] = []
        if option["commentFlag"]:
            Data.others["comment"] = []
        for board, boardId in option["boards"].items():
            if Config.Search.printBoardSearchEndFlag:
                self.progress.emit("[System] {} 검색 시작".format(board))
            threadedSearch(boardId, Data.others)
            if Config.Search.printBoardSearchEndFlag:
                self.progress.emit("[System] {} 검색 완료".format(board))
        # if option["articleFlag"]:
        #    Data.others["article"] = sorted(Data.others["article"], key=Util.comparator(Util.articleDateCompare), reverse=True)
        #if option["commentFlag"]:
        #    Data.others["comment"] = sorted(Data.others["comment"], key=Util.comparator(Util.commentDateCompare), reverse=True)
        if option["saveFlag"]:
            with open(option["fileName"]+".txt", "w", encoding='UTF-8') as file:
                if option["commentFlag"]:
                    self.progress.emit("[System] {} 글 저장 중".format(board))
                    file.write("\n".join(list(map(lambda article:article["article"]["title"] + "\n" + article["article"]["text"], Data.others["article"]))))
                    self.progress.emit("[System] {} 글 저장 완료".format(board))
                if option["articleFlag"]:
                    self.progress.emit("[System] {} 댓글 저장 중".format(board))
                    file.write("\n".join(list(map(lambda comment:comment["comment"]["text"], Data.others["comment"]))))
                    self.progress.emit("[System] {} 댓글 저장 완료".format(board))
        self.progress.emit("[System] 검색 완료")
        self.searchOthersEnd.emit()

        

    def searchOthers(self, option):
        thread = CustomThread(self.searchOthersTarget, self.threadFinished, "searchOthers", (Config.All.threadCount, option))
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
    
    def articleCyclePlaster(self, option):
        iteration = 0
        wordIndex = 0
        deletedArticles = []
        deletedComments = []
        while iteration < option["iteration"]:
            deletedArticles.clear()
            deletedComments.clear()
            if option["articleFlag"]:
                for index, article in enumerate(option["article"]):
                    retry = 0
                    while True:
                        response = self.postComment(article["article"], option["plasterWord"][wordIndex], option["anonym"])
                        if response != 0 and response != -1:
                            if option["delete"]:
                                self.deleteComment(response)
                            if Config.Plaster.printPlasterFlag:
                                self.progress.emit("[System] https://everytime.kr/{}/v/{} 성공 {}/{}".format(\
                                article["board"], article["article"]["id"], index+1+iteration*len(option["article"]), len(option["article"])*option["iteration"]))
                            break
                        elif response == 0:
                            if Config.Plaster.printPlasterFlag:
                                self.progress.emit("[System] https://everytime.kr/{}/v/{} 삭제됨 {}/{}".format(\
                                article["board"], article["article"]["id"], index+1+iteration*len(option["article"]), len(option["article"])*option["iteration"]))  
                            deletedArticles.append(article)
                            break
                        elif response == -1:
                            if Config.Plaster.printPlasterFlag:
                                self.progress.emit("[System] https://everytime.kr/{}/v/{} 실패 {}/{}".format(\
                                article["board"], article["article"]["id"], index+1+iteration*len(option["article"]), len(option["article"])*option["iteration"]))
                            retry = retry + 1
                            if retry > option["retry"]:
                                break
                            time.sleep(option["interval"])
                    wordIndex = (wordIndex + 1) % len(option["plasterWord"])
                    time.sleep(option["interval"])
            if option["commentFlag"]:
                for index, comment in enumerate(option["comment"]):
                    retry = 0
                    while True:
                        response = self.postSubcomment(comment["comment"], option["plasterWord"][wordIndex], option["anonym"])
                        if response != 0 and response != -1:
                            if option["delete"]:
                                self.deleteComment(response)
                            if Config.Plaster.printPlasterFlag:
                                self.progress.emit("[System] https://everytime.kr/{}/v/{} 성공 {}/{}".format(\
                                comment["board"], comment["article"]["id"], index+1+iteration*len(option["article"]), len(option["comment"]*option["iteration"])))
                            break
                        elif response == 0:
                            if Config.Plaster.printPlasterFlag:
                                self.progress.emit("[System] https://everytime.kr/{}/v/{} 삭제됨 {}/{}".format(\
                                comment["board"], comment["article"]["id"], index+1+iteration*len(option["article"]), len(option["comment"]*option["iteration"])))
                            deletedComments.append(comment)
                            break
                        elif response == -1:
                            if Config.Plaster.printPlasterFlag:
                                self.progress.emit("[System] https://everytime.kr/{}/v/{} 실패 {}/{}".format(\
                                comment["board"], comment["article"]["id"], index+1+iteration*len(option["article"]), len(option["comment"]*option["iteration"])))
                            retry = retry + 1
                            if retry > option["retry"]:
                                break
                            time.sleep(option["interval"])
                    wordIndex = (wordIndex + 1) % len(option["plasterWord"])
                    time.sleep(option["interval"])
            if option["articleFlag"]:
                for article in deletedArticles:
                    option["article"].remove(article)
            if option["commentFlag"]:
                for comment in deletedComments:
                    option["comment"].remove(comment)
            iteration = iteration + 1
    
    def stringCyclePlaster(self, option):
        iteration = 0
        articleIndex = 0
        commentIndex = 0
        currentIndex = 0
        deletedArticles = []
        deletedComments = []
        while iteration < option["iteration"]:
            deletedArticles.clear()
            deletedComments.clear()
            if option["articleFlag"]:
                for index, word in enumerate(option["plasterWord"]):
                    if index < currentIndex:
                        continue
                    retry = 0
                    while True:
                        article = option["article"][articleIndex]
                        response = self.postComment(article["article"], word, option["anonym"])
                        if response != 0 and response != -1:
                            if option["delete"]:
                                self.deleteComment(response)
                            if Config.Plaster.printPlasterFlag:
                                self.progress.emit("[System] https://everytime.kr/{}/v/{} 성공 {}/{}".format(\
                                article["board"], article["article"]["id"], index+1+iteration*len(option["plasterWord"]), len(option["plasterWord"])*option["iteration"]))
                            break
                        elif response == 0:
                            if Config.Plaster.printPlasterFlag:
                                self.progress.emit("[System] https://everytime.kr/{}/v/{} 삭제됨 {}/{}".format(\
                                article["board"], article["article"]["id"], index+1+iteration*len(option["plasterWord"]), len(option["plasterWord"])*option["iteration"]))  
                            deletedArticles.append(article)
                            break
                        elif response == -1:
                            if Config.Plaster.printPlasterFlag:
                                self.progress.emit("[System] https://everytime.kr/{}/v/{} 실패 {}/{}".format(\
                                article["board"], article["article"]["id"], index+1+iteration*len(option["plasterWord"]), len(option["plasterWord"])*option["iteration"]))
                            retry = retry + 1
                            if retry > option["retry"]:
                                break
                            time.sleep(option["interval"])
                    articleIndex += 1
                    currentIndex = index + 1
                    time.sleep(option["interval"])
                    if articleIndex == len(option["article"]):
                        articleIndex = 0
                        break
            if option["commentFlag"]:
                for index, word in enumerate(option["plasterWord"]):
                    if index < currentIndex:
                        continue
                    retry = 0
                    while True:
                        comment = option["comment"][commentIndex]
                        response = self.postSubcomment(comment["comment"], word, option["anonym"])
                        if response != 0 and response != -1:
                            if option["delete"]:
                                self.deleteComment(response)
                            if Config.Plaster.printPlasterFlag:
                                self.progress.emit("[System] https://everytime.kr/{}/v/{} 성공 {}/{}".format(\
                                comment["board"], comment["article"]["id"], index+1+iteration*len(option["plasterWord"]), len(option["plasterWord"])*option["iteration"]))
                            break
                        elif response == 0:
                            if Config.Plaster.printPlasterFlag:
                                self.progress.emit("[System] https://everytime.kr/{}/v/{} 삭제됨 {}/{}".format(\
                                comment["board"], comment["article"]["id"], index+1+iteration*len(option["plasterWord"]), len(option["plasterWord"])*option["iteration"]))
                            deletedComments.append(comment)
                            break
                        elif response == -1:
                            if Config.Plaster.printPlasterFlag:
                                self.progress.emit("[System] https://everytime.kr/{}/v/{} 실패 {}/{}".format(\
                                comment["board"], comment["article"]["id"], index+1+iteration*len(option["plasterWord"]), len(option["plasterWord"])*option["iteration"]))
                            retry = retry + 1
                            if retry > option["retry"]:
                                break
                            time.sleep(option["interval"])
                    commentIndex += 1
                    currentIndex = index + 1
                    time.sleep(option["interval"])
                    if commentIndex == len(option["comment"]):
                        commentIndex = 0
                        break
            if option["articleFlag"]:
                for article in deletedArticles:
                    option["article"].remove(article)
                if len(option["article"]) == 0:
                    option["articleFlag"] = False
            if option["commentFlag"]:
                for comment in deletedComments:
                    option["comment"].remove(comment)
                if len(option["comment"]) == 0:
                    option["commentFlag"] = False
            if not option["articleFlag"] and not option["commentFlag"]:
                return
            if currentIndex == len(option["plasterWord"]):
                iteration += 1
                currentIndex = 0

    def plasterTarget(self, option):
        if option["articleCycle"] is True:
            self.articleCyclePlaster(option)
        else:
            self.stringCyclePlaster(option)
        self.progress.emit("[System] 도배 완료")
        self.plasterEnd.emit()

    def plaster(self, option):
        thread = CustomThread(self.plasterTarget, self.threadFinished, "plaster", (option))
        self.threads["plaster"][thread] = thread
        thread.start()
    
    def abortPlaster(self):
        if len(self.threads["plaster"]) > 0:
            for thread in list(self.threads["plaster"]):
                thread.terminate()
                self.threadFinished(thread, "plaster")
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
    def articleDateCompare(article1, article2):
        date1 = datetime.datetime.strptime(article1["article"]["created_at"], '%Y-%m-%d %H:%M:%S')
        date2 = datetime.datetime.strptime(article2["article"]["created_at"], '%Y-%m-%d %H:%M:%S')
        if date1 < date2:
            return -1
        elif date1 > date2:
            return 1
        else:
            return 0

    @staticmethod
    def commentDateCompare(comment1, comment2):
        date1 = datetime.datetime.strptime(comment1["comment"]["created_at"], '%Y-%m-%d %H:%M:%S')
        date2 = datetime.datetime.strptime(comment2["comment"]["created_at"], '%Y-%m-%d %H:%M:%S')
        if date1 < date2:
            return -1
        elif date1 > date2:
            return 1
        else:
            return 0

    
    @staticmethod
    def comparator(func):
        class K:
            def __init__(self, obj, *args):
                self.obj = obj
            def __lt__(self, other):
                return func(self.obj, other.obj) < 0
            def __gt__(self, other):
                return func(self.obj, other.obj) > 0
            def __eq__(self, other):
                return func(self.obj, other.obj) == 0
        return K

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