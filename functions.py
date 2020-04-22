import hashlib
import os
from pathlib import Path
import glob
from datetime import datetime

def checkPrevFileExists(path,filename):
    filesInDir = [file for file in os.listdir(path)]   
    if filename not in str(filesInDir):
        print("\nFile does not exist there")
        createFile = input("\nDo you want to create it? (yes/no): ")
        if createFile=='yes':
            createPrevFile = "".join([path,filename])
            Path(createPrevFile).touch()
            print("\nPrev File Created")

def checkSum(path,wildcardFiles):
    files = glob.glob("".join([path,wildcardFiles]))
    if len(files) < 2:
        print("\nPlease check both the curr and prev file exist!")
        os._exit(0)

    digests = []
    for filename in files:
        hasher = hashlib.md5()
        with open(filename, 'rb') as f:
            buf = f.read()
            hasher.update(buf)
            get_hash = hasher.hexdigest()
            digests.append(get_hash)

    if digests[0] == digests[1]:
        return True
    else:
        return False 

def checkArchiveDirsExist(path,archiveDir):
    prevDir = "".join([path,archiveDir])
    filesInDir = [file for file in os.listdir(path)]
    cleanArchiveDir = archiveDir.split('/')[0]

    if (cleanArchiveDir not in str(filesInDir)):
        print("\nThe archive directory does not exist")
        createThem = input("\nDo you want to create it? (yes/no): ")
        if createThem == 'yes':
            os.mkdir(prevDir)
        else:
            print("\nThis is needed for process to work... please create")
            os._exit(1)

def movePrevFile(path,file,archiveDir):
    full_path = "".join([path,file])
    fileSplit = os.path.splitext(file)[0]
    dateTime = datetime.now()
    dateTimeStr = dateTime.strftime("%m_%d_%Y_%H:%M:%S")
    filename = "".join([fileSplit,dateTimeStr,".json"])
    filenameAndPath = "".join([path,archiveDir,filename])
    os.rename(full_path,filenameAndPath)

def RenameCurrtoPrev(path,currFile,prevFile):
    fullCurrPath = "".join([path,currFile])
    fullPrevPath = "".join([path,prevFile])
    os.rename(fullCurrPath,fullPrevPath)
