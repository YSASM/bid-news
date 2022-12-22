# 导入库
import time
import pdfkit
import fitz
import os
import re
from PyPDF2 import PdfReader,PdfWriter
'''将字符串生成pdf文件'''
path_wkthmltopdf = r'base\wkhtmltopdf\bin\wkhtmltoimage.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
options = {
	    'encoding': "utf-8",
		'page-size': 'A6',
	    'margin-top': '0mm',
	    'margin-right': '0mm',
	    'margin-bottom': '0mm',
	    'margin-left': '0mm'
	}
def del_width(htmlpath):
	f = open(htmlpath,'r',encoding='utf-8')
	html = f.read()
	pat = re.compile("width[ ]?[:=][ ]?[\"]?[0-9a-z%]+[\"]?[ ]?[;]?")
	match = pat.findall(html)
	for i in match:
		html = html.replace(i,'width="50%"') if '=' in i else html.replace(i,' ')
	f.close()
	f = open(htmlpath,'w',encoding='utf-8')
	f.write(html)
def del_repeat(path):
    sor = path              # 需要压缩的PDF文件
    obj = "new" + sor
    doc = fitz.open(sor) 
    totaling = doc.pageCount
    zoom = 200                     # 清晰度调节，缩放比率
    pdfz(sor, obj, zoom, totaling, doc)
    os.removedirs('.pdf')

def covert2pic(zoom, totaling, doc):
    if os.path.exists('.pdf'):       # 临时文件，需为空
         os.removedirs('.pdf')
    os.mkdir('.pdf')
    for pg in range(totaling):
        page = doc[pg]
        zoom = int(zoom)            #值越大，分辨率越高，文件越清晰
        rotate = int(0)
        print(page)
        trans = fitz.Matrix(zoom / 100.0, zoom / 100.0).preRotate(rotate)
        pm = page.getPixmap(matrix=trans, alpha=False)
      
        lurl='.pdf/%s.jpg' % str(pg+1)
        pm.writePNG(lurl)
    doc.close()

def pic2pdf(obj, totaling):
    doc = fitz.open()
    for pg in range(totaling):
        img = '.pdf/%s.jpg' % str(pg+1)
        imgdoc = fitz.open(img)                 # 打开图片
        pdfbytes = imgdoc.convertToPDF()        # 使用图片创建单页的 PDF
        os.remove(img)  
        imgpdf = fitz.open("pdf", pdfbytes)
        doc.insertPDF(imgpdf)                   # 将当前页插入文档
    if os.path.exists(obj):         # 若文件存在先删除
        os.remove(obj)
    doc.save(obj)                   # 保存pdf文件
    doc.close()


def pdfz(sor, obj, zoom, totaling, doc):    
    covert2pic(zoom, totaling, doc)
    pic2pdf(obj, totaling)
def str_to_pdf(string, to_file):
	# 生成pdf文件，to_file为文件路径
	pdfkit.from_file(string, to_file, configuration=config, options=options)
# pdf 转html
def wkhtmltopdf(input_path, html_path):
    doc = fitz.Document(input_path)
    html_content = "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\"><title>Title</title></head><body style=\"display: flex;justify-content: center;flex-direction: column;background: #0e0e0e;align-items: center;\">"
    for page in doc:
        html_content += page.getText("html")
    html_content += "</body></html>"
    with open(html_path, "w", encoding="utf8", newline="") as fp:
        fp.write(html_content)
start = time.time()
del_width('test.html')
str_to_pdf('test.html',u'1.pdf')
del_repeat('1.pdf')
print(time.time()-start,end='')
print('s')
wkhtmltopdf('out.pdf','out2.html')
# os.remove('out.pdf')
# import imgkit
 
# path_wk = r'base\wkhtmltopdf\bin\wkhtmltoimage.exe'  # 工具路径
# # cfg = imgkit.config(wkhtmltoimage=path_wkimg)
# # 1、将html文件转为图片
# # imgkit.from_file(r'test.html', 'out.jpg', config=cfg)
# # # 2、从url获取html，再转为图片
# # imgkit.from_url('https://httpbin.org/ip', 'ip.jpg', config=cfg)
# # # 3、将字符串转为图片
# # f = open('test.html','r',encoding='utf-8').read()
# # imgkit.from_string(f,'hello.jpg', config=cfg)
# config = imgkit.config(wkhtmltoimage=path_wk)
# options = {
#     'encoding': 'UTF-8',
# }
# #转换HTML文件为图片
# html1 = imgkit.from_file(filename="test.html",  config=config, options=options, output_path="out.jpg")
# #转换HTML网址为图片
# # html2 = imgkit.from_url(url="https://www.baidu.com",config=config,output_path="out2.png")