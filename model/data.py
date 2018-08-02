class Data:
    mine = None
    others = {}
    boards = {}

    @staticmethod
    def initialize():
        Data.mine = None
        Data.others = {}
        Data.boards = {}