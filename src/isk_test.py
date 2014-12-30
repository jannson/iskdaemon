import os
from os import listdir
import StringIO
import requests
from PIL import Image
from xmlrpclib import ServerProxy, Binary
from simdb import simpledb

server = ServerProxy("http://localhost:31128/RPC")
image_folder = "/home/janson/download/baidu-yun"

def thumbnail(infile, max_width):
    try:
        img = Image.open(infile)
        s = img.size;
        if s[0] > max_width:
            ratio = max_width/s[0];
            #print ratio, max_width
            size = (s[0]*ratio, s[1]*ratio)
            img.thumbnail(size, Image.ANTIALIAS)
        output = StringIO.StringIO()
        img.save(output, "JPEG")
        return output
    except IOError:
        print "cannot create thumbnail for '%s'" % infile

def upload(my_file, filename):
    api_url = 'http://127.0.0.1:4869/upload'
    r = None
    try:
        r = requests.post(api_url, files={filename.decode('utf-8'): my_file})
    except:
        print filename

    if not r:
        raise Exception(filename)

    if not 'MD5' in r.text:
        raise Exception(r.text)

    s = r.text
    return s[s.index('MD5:')+5:s.index('</h1>')]

max_cnt = 10000000
cnt = 1
server.createDb(2)

def index_image(folder, filename):
    global cnt
    #global image_folder
    #global server

    path = os.path.join(folder, filename)
    output = thumbnail(path, 800.0)
    output.seek(0)
    md5 =  upload(output, filename)

    path = path[len(image_folder)+1:]
    print 'uploaded',path, md5

    simpledb.save(md5, cnt, path.decode('utf-8'))

    output.seek(0)
    server.addImgBlob(2, cnt, Binary(output.getvalue()))
    output.close()

def index_image_folder(folder_path):
    global max_cnt
    global cnt
    if cnt > max_cnt:
        return

    for f in listdir(folder_path):
        path = os.path.join(folder_path, f)
        if os.path.isfile(path):
            is_image = any(path.endswith("." + ext) for ext in ['jpg', 'png', 'jpeg'])
            if is_image:  # check extension, only index images
                index_image(folder_path, f)
                cnt = cnt + 1
                if cnt > max_cnt:
                    return
        elif os.path.isdir(path):
            index_image_folder(path)

index_image_folder(image_folder)
server.saveAllDbs()

print server.queryImgID(2, 3)
