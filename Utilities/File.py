import os


class File(object):
    directory = None

    def __init__(self):
        self.directory = os.path.split(os.path.abspath(__file__))[0]

    def openFile(self,filename):
        path = self.directory + "/"+filename
        if not os.path.isfile(path):
            raise Exception("We were not able to located the file " + filename + " at the following path "+path)

        with open(path) as f:
            return f.readline()

    def getSensitiveVector(self):
        return self.openFile('sensitive.txt')

    def getPassiveSQLInjectionVector(self):
        return self.openFile('passiveSQL.txt')

    def getActiveSQLInjection(self):
        return self.openFile('activeSQL.txt')