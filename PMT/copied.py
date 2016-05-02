#!/usr/bin/env python
# Parameter 1:  the folder contains the original images.
# Parameter 2:  the folder to save new images. 


from PIL import Image
import os, sys
import os.path
import random

def getdistpath(str, distdir):
    date = str.split(' ')[0].split(':')
    dirs = distdir + os.sep + os.sep.join(date)
    if not os.path.exists(dirs):
        os.makedirs(dirs)
    dirs = dirs + os.sep + ''.join(str.split(' ')[1].split(':'))
    return dirs
    
def getCameraModel(str):
    model = str.replace(' ', '_')
    return model
         

def copyimage(srcdir, distdir):
    for path in [srcdir+os.sep+i for i in os.listdir(srcdir)]:
        if os.path.isdir(path):
            copyimage(path, distdir)
        else:
            writelog(path)
            ext = os.path.splitext(path)[1]            
            try:
                image = Image.open(path)                                
            except:
                logstr = 'file open error:' + path
                writelog(logstr)
            try:                
                #[306] is date and time
                #[272] is Camera model with space as splitter
                distpath = getdistpath(image._getexif()[306], distdir)   
                distpath = distpath + getCameraModel(image._getexif()[272])
                
                logstr = 'distpath:' + distpath
                writelog(logstr)
            except:                
                logstr = 'getextif error:' + path
                writelog(logstr)
            try:
                if not os.path.exists(distpath+ext):                    
                    distpath = distpath + ext
                    print(distpath)
                    image.save(distpath)                
                else:
                    print ("Same time stamp image found!")
                    rand = random.randint(1, 100)                    
                    distpath = distpath + '_' + str(rand) + ext
                    print(distpath)
                    image.save(distpath)
            except:
                logstr = 'file copy error:' + path
                writelog(logstr)

def writelog(str):
    global logfile
    logfile.write(str+'\n')    

def main():    
    if len(sys.argv) == 3:
        global logfile
        logfile = open('cilog.txt', 'w')
        copyimage(sys.argv[1], sys.argv[2])
        logfile.close()
    else:
        print('2 parameters required, first is folder for photos, second is target folder')
        print('e.g:', sys.argv[0],'e:\\photo f:\\goodphoto')


if __name__ == '__main__':
    main()
