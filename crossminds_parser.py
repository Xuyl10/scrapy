import json
from crossminds_config import crossminds_config
from tqdm import tqdm
from crossminds_saver import crossminds_saver

class crossminds_parser:

    def parse_title(self,item):
        raw_title = item["title"]
        # title = raw_title.split(']')[-1].strip()
        return raw_title

    def parse_author(self,item):
        #todo:
        # authors从description里找 没有的话再直接用json中的author字段

        return item["author"]["name"]

    def parse_publicationOrg(self,item):
        str = ' '
        publicationOrg = str.join(item["category"][0].split(' ')[0:-1])
        return publicationOrg

    def parse_url(self,item):
        #todo:从description中解析url

        pdfurl=''

        codeurl=''

        return pdfurl, codeurl
        


    def parser(self, items):
        json_results = []
        for i in range(len(items)):
            for j in range(crossminds_config.request_num):
                json_results.append(json.loads(items[i])["results"][j]) 
        for i in tqdm(range(len(json_results))):
            item = json_results[i]
            title = self.parse_title(item)
            videoUrl = item["video_url"]
            year = item["created_at"][0:4]
            publicationOrg = self.parse_publicationOrg(item)
            authors = self.parse_author(item)
            pdfurl,codeurl = self.parse_url(item)
            datasetUrl = ''
            videoPath = ''
            pdfPath = ''
            abstract = ''
            publicationUrl = ''
            _id = item["_id"]

            paperInfo = {
                "_id": _id,
                "title" : title,
                "authors": authors,
                "abstract": abstract,
                "publicationOrg": publicationOrg,
                "year": year,
                "pdfUrl": pdfurl,
                "pdfPath": "",
                "publicationUrl":publicationUrl,
                "codeUrl": codeurl,
                "datasetUrl": datasetUrl,
                "videoUrl": videoUrl,
                "videoPath": ""
            }


            print("id: ", _id)
            print("title: ", title)
            print("authors: ", authors)
            print("abstract: ", abstract)
            print("year: ", year)
            print("publicationOrg: ", publicationOrg)
            print("pdfurl: ", pdfurl)
            print("pdfPath: ", pdfPath)
            print("videoUrl: ", videoUrl)
            print("videoPath: ", videoPath)
            print("datasetUrl: ", datasetUrl)
            print("publicationUrl: ",publicationUrl)
            print("codeurl: ", codeurl)

            crossminds_saver().savePaperInfo(paperInfo)




