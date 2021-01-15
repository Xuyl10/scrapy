# scrapy

## 目录结构
│  README.md   
│--crossminds  
│     crossminds_config.py  参数设置  
│     crossminds_parser.py  解析对应的论文的各个字段  
│     crossminds_scrapy.py  按会议类别取论文  
│     crossminds_saver.py   存数据库、重复判断  
│     downloader.py         负责视频和PDF文件的下载  
│     main.py               运行程序的入口  
│


## 环境 
- python3

运行必须要安装的包
```
pip install requests
pip install beautifulsoup4
pip install lxml
pip install pymongo
pip install pytube
```

## 整体流程
1、首先通过 https://api.crossminds.io/web/node/interest-list?offset=0&limit=10 接口获得crossminds中按Knowledge Area分的十个类别

2、通过 https://api.crossminds.io/web/node/video/name/{category}?limit=1500&offset=0 从各个类别中获取相应的论文的json数据，category为第1步中获取到的类别（由于在网站中可以直接看到每个类别的item数量，最大为1471，所以这里的limit先设置为了1500）

3、解析每个论文的json数据  
着重说明以下几个字段的解析
- pdfurl字段
```
由于crossminds给到的paperurl并不统一，有些是用paperlink做了链接，而有些直接写在了一篇paper对应的description中，所以这里采用两种方式解析：
- 每片paper对应的json文件中都有对应的_id，而它所对应的展示页面对应于https://crossminds.ai/video/_id，通过使用beautifulsoup可以解析对应的页面中的paperlink
- 如果页面中没有paperlink链接，则去相应的description中使用正则表达式找到pdf的地址，并做相应的替换，便于后续下载pdf使用
```
- abstract字段
```
- crossminds中paper的description部分包含abstract，有些会明确指出有abstract，对于这种我们用正则表达式提取出abstract部分
- 如果没有且之前爬到了对应的pdfurl，比如arxiv网站的url，则用beautifulsoup解析arxiv中论文主页的摘要
```
- authors字段
```
- crossminds中paper的json数据中有authors字段，但很多的上传者都是“computor vision”此类，对于没有pdfurl的paper，我们直接使用该字段
- 对于爬到了pdfurl的paper，比如arxiv网站的url，则用beautifulsoup解析arxiv中论文主页的作者
```
4、数据的存储，使用pymongo存储到了mongodb数据库中  
5、视频和PDF的下载。将视频和PDF文件下载到本地，将存储路径存到mongoDB数据库中。

- 视频下载。CrossMinds网站中的视频主要来自于CrossMinds、Youtube 和 Vimeo三个网站，根据其存储视频文件不同采用不同的下载方式。

  1、来自CrossMinds网站的视频URL例如：https://stream.crossminds.ai/5fa9d52a8a1378120d965136-1604965683584/hls-5fa9d52a8a1378120d965136.m3u8 ，视频为m3u8格式，m3u8文件主要以文件列表的形式存在，根据其中记录的索引可以找到多个分段的ts格式的音视频文件，将这些分段的音视频文件下载下来，最后合并成一个完整的ts格式的视频。  
  2、来自Vimeo网站的视频URL例如：https://vimeo.com/423554135 ，对此url的内容进行解析，得到视频的相关信息包括文件名，分辨率，实际的下载地址等信息，选择最低分辨率对应的视频文件进行下载。  
  3、来自Youtube网站的视频URL例如：https://www.youtube.com/embed/mo079YBVTzE ，使用第三方工具pytube可以直接对此类URL进行下载。  

    视频下载可以在爬取到一篇论文的基本信息之后就进行，也可以在基本信息都爬完之后，从数据库中获取所有包含视频URL的论文信息，视频文件默认存储在```./data/videos/```路径下

- PDF文件下载。PDF文件和视频的文件名在存储时都需要都标题进行处理，去掉文件名非法字符。PDF文件默认存储在```./data/PDFs/```路径下



