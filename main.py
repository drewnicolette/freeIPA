import httplib2
import functions as f
import time
import os
from testFreeIPAUsers import freeIPAUsers
from testFreeIPAGroups import freeIPAGroups

def users():
  c = httplib2.HTTPConnectionWithTimeout('cdf-west-ipa.coop-west.local',timeout=5)
  c.request('HEAD',"")
  if c.getresponse().status != 404:
    print("Connected!\n")
  
  ipaObject = freeIPAUsers('cdf-west-ipa.coop-west.local','admin','3edc3edc4rfv')
  client = ipaObject.connect()
  path = './files/'
  archiveDir = 'prevUserArchiveDir/'
  prevFile = 'users_prev.json'
  currFile = 'users_curr.json'
 
  #Check if previous file exists and archive directory exists 
  f.checkPrevFileExists(path,prevFile)
  f.checkArchiveDirsExist(path,archiveDir)

  ipaObject.getAllLocalUserInfo(client,path,currFile)

  if f.checkSum(path,'*users*') == True:
    print("No change in User Information\n")
    f.RenameCurrtoPrev(path,currFile,prevFile)
    os._exit(0)

  if ipaObject.findRemovedUsers(client,prevFile,path,currFile):
    print("Removed Users")
    print(ipaObject.findRemovedUsers(client,prevFile,path,currFile))
    print("\n")
  if ipaObject.findNewUsers(client,prevFile,path,currFile):
    print("New Users")
    print(ipaObject.findNewUsers(client,prevFile,path,currFile))
    print("\n")
  if ipaObject.onlyUpdatedUsers(client,prevFile,path,currFile):
    print("Changed Users")
    print(ipaObject.onlyUpdatedUsers(client,prevFile,path,currFile))
    print("\n")

  f.movePrevFile(path,prevFile,archiveDir)
  time.sleep(1)
  f.RenameCurrtoPrev(path,currFile,prevFile)

def groups():
  c = httplib2.HTTPConnectionWithTimeout('cdf-west-ipa.coop-west.local',timeout=5)
  c.request('HEAD',"")
  if c.getresponse().status != 404:
    print("Connected!\n")

  ipaObject = freeIPAGroups('cdf-west-ipa.coop-west.local','admin','3edc3edc4rfv')
  client = ipaObject.connect()
  path = './files/'
  archiveDir = 'prevGroupArchiveDir/'
  prevFile = 'groups_prev.json'
  currFile = 'groups_curr.json'

  #Check if previous file exists and archive directory exists
  f.checkPrevFileExists(path,prevFile)
  f.checkArchiveDirsExist(path,archiveDir)

  ipaObject.getAllLocalGroupInfo(client,path,currFile)

  if f.checkSum(path,'*groups*') == True:
    print("No change in Group Information\n")
    f.RenameCurrtoPrev(path,currFile,prevFile)
    os._exit(0)

  if ipaObject.findRemovedGroups(client,prevFile,path,currFile):
    print("Removed Groups")
    print(ipaObject.findRemovedGroups(client,prevFile,path,currFile))
    print("\n")
  if ipaObject.findNewGroups(client,prevFile,path,currFile):
    print("New Groups")
    print(ipaObject.findNewGroups(client,prevFile,path,currFile))
    print("\n")
  if ipaObject.onlyUpdatedGroups(client,prevFile,path,currFile):
    print("Changed Groups")
    print(ipaObject.onlyUpdatedGroups(client,prevFile,path,currFile))
    print("\n")

  f.movePrevFile(path,prevFile,archiveDir)
  time.sleep(1)
  f.RenameCurrtoPrev(path,currFile,prevFile)

def main():
  users()
  groups()

if __name__=="__main__":
  main()
