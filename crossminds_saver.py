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
        # 使用标题和pdfurl来判断冗余
        if (col.find_one({"_id": paperInfo["_id"]}) != None):
            return
        if (col.find_one({"title": paperInfo["title"]}) != None):
            return
        if (col.find_one({"pdfUrl": paperInfo["pdfUrl"]})!= None and paperInfo["pdfUrl"]!=''):
            return
        col.insert_one(paperInfo)

        

