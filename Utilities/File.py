import os

class File(object):
    directory = None

    def __init__(self):
        self.directory = os.path.abspath(os.path.join(__file__ ,"../.."))

    def openFile(self,filename):
        path = self.directory + "/Files/" + filename
        if not os.path.isfile(path):
            raise Exception("We were not able to located the file " + filename + " at the following path "+path)

        with open(path) as f:
            return f.readlines()

    def getSensitiveVector(self):
        return self.openFile('sensitive.txt')

    def getPassiveSQLInjectionVector(self):
        return self.openFile('passiveSQL.txt')

    def getActiveSQLInjection(self):
        return self.openFile('activeSQL.txt')

    def getPossibleUserPass(self):
        return self.openFile('userpass.txt')

    def getDirectoriesLinks(self):
        return self.openFile('directories.txt')

    def getFilesLinks(self):
        return self.openFile('filenames.txt')