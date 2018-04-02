import os

class File(object):
    directory = None

    """
        The file object that open and return specific requested files
    """

    def __init__(self):
        self.directory = os.path.abspath(os.path.join(__file__ ,"../.."))

    def openFile(self,filename):
        """
        Opens the file and return the content of the file
        :param filename: file name
        :return: content inside file
        """
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

    def getXSSScripts(self):
        return self.openFile('XSSAttacks.txt')
