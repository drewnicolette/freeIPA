from python_freeipa import ClientMeta
from deepdiff import DeepDiff
import json

class freeIPAGroups:
  def __init__(self,ipaInstance,username,password):
    self.ipaInstance = ipaInstance
    self.username = username
    self.password = password

  def connect(self):
    client = ClientMeta(self.ipaInstance,verify_ssl=False)
    client.login(self.username,self.password)
    return client
    
  def getAllLocalGroupInfo(self,client,path,currFile):
    allGroups = json.dumps(client.group_find())
    groups = json.loads(allGroups)['result']
    filepath = "".join([path,currFile])
    with open(filepath,'w') as outfile:
      json.dump(groups,outfile)
    return groups
 
  def getPrevGroups(self,prevFile,path):
    oldGroups = []
    filepath = "".join([path,prevFile])
    with open(filepath) as json_file:
      data = json.load(json_file)
      for group in data:
        cn = str(group['cn'])[2:-2]
        oldGroups.append(cn)
    return oldGroups

  def getCurrGroups(self,client,path,currFile):
    groups = []
    for user in self.getAllLocalGroupInfo(client,path,currFile):
      cn = str(user['cn'])[2:-2]
      groups.append(cn)
    return groups

  def findNewGroups(self,client,prevFile,path,currFile):
    newGroups = []
    oldGroups = self.getPrevGroups(prevFile,path)
    for group in self.getAllLocalGroupInfo(client,path,currFile):
      cn = str(group['cn'])[2:-2]
      if cn not in oldGroups:
        newGroups.append(group)
    return newGroups

  def findRemovedGroups(self,client,prevFile,path,currFile):
    removedGroups = []
    currGroups = self.getCurrGroups(client,path,currFile)
    filepath = "".join([path,prevFile])
    with open(filepath) as json_file:
      data = json.load(json_file)
      for group in data:
        cn = str(group['cn'])[2:-2]
        if cn not in currGroups:
          removedGroups.append(group)
    return removedGroups

  @staticmethod
  def getUpdatedGroups(path,currFile,prevFile):
    currFilepath = "".join([path,currFile])
    prevFilepath = "".join([path,prevFile])
    with open(currFilepath) as c:
      curr = json.load(c)
    with open(prevFilepath) as p:
      prev = json.load(p)
    ddiff = DeepDiff(prev,curr,ignore_order=True)
    return ddiff

  @staticmethod
  def sendUpdatedGroups(path,currFile,prevFile):
    changes = freeIPAGroups.getUpdatedGroups(path,currFile,prevFile)
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

  def onlyUpdatedGroups(self,client,primeJsonFile,path,currFile):
    newGroups = self.findNewGroups(client,primeJsonFile,path,currFile)
    updatedGroups = freeIPAGroups.sendUpdatedGroups(path,currFile,primeJsonFile)
    listOfNewGroups = []
    listOfUpdatedGroups = []
    for group in newGroups:
      cn = str(group['cn'])[2:-2]
      listOfNewGroups.append(cn)
    for group in updatedGroups:
      cn = str(group['cn'])[2:-2]
      if cn not in listOfNewGroups:
        listOfUpdatedGroups.append(group)
    return listOfUpdatedGroups
