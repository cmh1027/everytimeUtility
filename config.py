class Config:
    class All:
        threadCount = 4

        @staticmethod
        def initialize():
            Config.All.threadCount = 4

    class Delete:
        deleting = False
        printIdFlag = True
        printTextFlag = True
        printOriginFlag = True
        excludeWord = []
        excludeArticleFlag = False
        excludeCommentFlag = False

        @staticmethod
        def initialize():
            Config.Delete.deleting = False
            Config.Delete.printIdFlag = True
            Config.Delete.printTextFlag = True
            Config.Delete.printOriginFlag = True
            Config.Delete.excludeWord = []
            Config.Delete.excludeArticleFlag = False
            Config.Delete.excludeCommentFlag = False

    class Search:
        printBoardSearchEndFlag = True
        searchingMine = False
        searchingOthers = False
        selectedBoards = {}
        searchNickname = ""
        searchAllFlag = False

        @staticmethod
        def initialize():
            Config.Search.printBoardSearchEndFlag = True
            Config.Search.searchingMine = False
            Config.Search.searchingOthers = False
            Config.Search.selectedBoards = {}
            Config.Search.searchNickname = ""
            Config.Search.searchAllFlag = False            

    class Plaster:
        plasterInterval = 4
        printPlasterFlag = True
        plastering = False
        plasterBoards = {}
        plasterWord = []

        @staticmethod
        def initialize():
            Config.Plaster.plasterInterval = 4
            Config.Plaster.printPlasterFlag = True
            Config.Plaster.plastering = False
            Config.Plaster.plasterBoards = {}
            Config.Plaster.plasterWord = []
            
    @staticmethod
    def initialize():
        Config.All.initialize()
        Config.Delete.initialize()
        Config.Search.initialize()
        Config.Plaster.initialize()
