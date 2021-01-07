import pymongo
from crossminds_config import crossminds_config

class crossminds_saver:
    def __init__(self):
        super().__init__()
        self.connection = pymongo.MongoClient(host = crossminds_config.host,port = crossminds_config.port)
        self.database = crossminds_config.db
        self.collection = "basicInfo"

    def savePaperInfo(self, paperInfo):
        db =self.connection[self.database]
        col = db[self.collection]
        # 检查标题重复
        if (col.find_one({"title": paperInfo["title"]}) != None):
            return
        col.insert_one(paperInfo)

        

