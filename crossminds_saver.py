import pymongo
from crossminds_config import crossminds_config


class crossminds_saver:
    def __init__(self):
        super().__init__()
        self.database = crossminds_config.db
        self.collection = "justfortest1"
        self.connection = pymongo.MongoClient(
            host=crossminds_config.host,
            port=crossminds_config.port,
            username=crossminds_config.username,
            password=crossminds_config.pwd,
            authSource=self.database)

    def save_paperinfo(self, paperinfo):
        db = self.connection[self.database]
        col = db[self.collection]
        # 使用标题和pdfurl来判断冗余
        if (col.find_one({"_id": paperinfo["_id"]}) is not None):
            return
        if (col.find_one({"title": paperinfo["title"]}) is not None):
            return
        if (col.find_one({"pdfUrl": paperinfo["pdfUrl"]}) is not None
                and paperinfo["pdfUrl"] != ''):
            return
        col.insert_one(paperinfo)
        print("save successfully!")
