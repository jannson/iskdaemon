import os
from os import listdir
import StringIO
import requests
from PIL import Image
from xmlrpclib import ServerProxy

server = ServerProxy("http://localhost:31128/RPC")
image_folder = "/home/janson/download/baidu-yun"

def thumbnail(infile, max_width):
    try:
        img = Image.open(infile)
        s = img.size;
        if s[0] > max_width:
            ratio = max_width/s[0];
            print ratio, max_width
            size = (s[0]*ratio, s[1]*ratio)
            img.thumbnail(size, Image.ANTIALIAS)
        output = StringIO.StringIO()
        img.save(output, "JPEG")
        return output
    except IOError:
        print "cannot create thumbnail for '%s'" % infile

def upload(my_file, filename):
    api_url = 'http://127.0.0.1:4869/upload'
    r = requests.post(api_url, files={filename: my_file})

    if not 'MD5' in r.text:
        raise Exception(r.text)

    return r.text

def index_image(folder, filename):
    path = os.path.join(folder, filename)
    output = thumbnail(path, 800.0)
    output.seek(0)
    print 'uploaded', path
    print 'uploaded', upload(output, filename)

max_cnt = 1
cnt = 0
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
#print server.createDb(2)

index_image_folder(image_folder)
