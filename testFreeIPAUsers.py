from python_freeipa import ClientMeta
from deepdiff import DeepDiff
import json

class freeIPAUsers:
  def __init__(self,ipaInstance,username,password):
    self.ipaInstance = ipaInstance
    self.username = username
    self.password = password

  def connect(self):
    client = ClientMeta(self.ipaInstance,verify_ssl=False)
    client.login(self.username,self.password)
    return client

  def getAllLocalUserInfo(self,client,path,currFile):
    allUsers = json.dumps(client.user_find())
    users = json.loads(allUsers)['result']
    filepath = "".join([path,currFile])
    with open(filepath,'w') as outfile:
      json.dump(users,outfile)
    return users
  
  def getPrevUsernames(self,prevFile,path):
    oldUsers = []
    filepath = "".join([path,prevFile])
    with open(filepath) as json_file:
      data = json.load(json_file)
      for user in data:
        uid = str(user['uid'])[2:-2]
        oldUsers.append(uid)
    return oldUsers 

  def getCurrUsernames(self,client,path,currFile):
    usernames = []
    for user in self.getAllLocalUserInfo(client,path,currFile):
      uid = str(user['uid'])[2:-2]
      usernames.append(uid)
    return usernames

  def findNewUsers(self,client,prevFile,path,currFile):
    newUsers = []
    oldUsers = self.getPrevUsernames(prevFile,path)
    for user in self.getAllLocalUserInfo(client,path,currFile):
      uid = str(user['uid'])[2:-2]
      if uid not in oldUsers:
        newUsers.append(user)
    return newUsers
 
  def findRemovedUsers(self,client,prevFile,path,currFile):
    removedUsers = []
    currUsers = self.getCurrUsernames(client,path,currFile)
    filepath = "".join([path,prevFile])
    with open(filepath) as json_file:
      data = json.load(json_file)
      for user in data:
        uid = str(user['uid'])[2:-2]
        if uid not in currUsers:
          removedUsers.append(user)
    return removedUsers

  def addUsers(self,client,primeJsonFile):
    newUsers = self.findNewUsers(client,primeJsonFile,path,currFile)
    language = 'EN'
    for user in newUsers:
      uid = str(user['uid'])[2:-2]
      firstname = str(user['uid'])[2:-2]
      lastname = str(user['sn'])[2:-2]
      client.user_add(uid,firstname,lastname,"{0} {1}".format(firstname,lastname),o_preferredlanguage=language)

  @staticmethod
  def getUpdatedUsers(path,currFile,prevFile):
    currFilepath = "".join([path,currFile])
    prevFilepath = "".join([path,prevFile])
    with open(currFilepath) as c:
      curr = json.load(c)
    with open(prevFilepath) as p:
      prev = json.load(p)
    ddiff = DeepDiff(prev,curr,ignore_order=True)
    return ddiff

  @staticmethod
  def sendUpdatedUsers(path,currFile,prevFile):
    changes = freeIPAUsers.getUpdatedUsers(path,currFile,prevFile)
    currFilepath = "".join([path,currFile])
    with open(currFilepath) as c:
      curr = json.load(c)
    changedIndicies = []
    updatedUsers = []
    if 'iterable_item_added' not in changes.keys():
      return updatedUsers
    valueChanged = changes['iterable_item_added']

    for key in valueChanged:
      parse = int(key.find('['))
      parseEnding = int(key.find(']'))
      changedIndicies.append(int(key[parse + 1:parseEnding]))

    for index,value in enumerate(curr):
      if index in changedIndicies:
        updatedUsers.append(value)
    return updatedUsers

  def onlyUpdatedUsers(self,client,primeJsonFile,path,currFile):
    newUsers = self.findNewUsers(client,primeJsonFile,path,currFile)
    updatedUsers = freeIPAUsers.sendUpdatedUsers(path,currFile,primeJsonFile)
    listOfNewUsers = []
    listOfUpdatedUsers = []
    for user in newUsers:
      uid = str(user['uid'])[2:-2]
      listOfNewUsers.append(uid)
    for user in updatedUsers:
      uid = str(user['uid'])[2:-2]
      if uid not in listOfNewUsers:
        listOfUpdatedUsers.append(user)
    return listOfUpdatedUsers
