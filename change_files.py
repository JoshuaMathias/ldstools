import os
from os import walk
import subprocess

path = "/home/joshuamonkey/Documentos/Church/Book of Mormon/Le Livre de Mormon - French"
files = []
if os.path.exists(path):
    for (dirpath, dirnames, filenames) in walk(path):
        files.extend(filenames)
        break

    for f in files:
        filename, file_extension = os.path.splitext(f)
        if file_extension == ".mp3":
            subprocess.call(['ffmpeg', '-i', path+'/'+f, '-filter:a', 'atempo=1.5', '-strict', '-2', '-q:a', '9', path+'/fast/'+filename+'_fast.mp3'])
else:
    print "path "+path+" not found"