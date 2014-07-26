'''
Created on Jul 24, 2014

@author: gigemjt
'''

__all__ = ["RequestHandler"]

import SimpleHTTPServer

import posixpath
import urllib
import os
from src.projectManagment import ProjectManagment

HOST_NAME = 'localhost' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 9000 # Maybe set this to 9000.


class RequestHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):

    currentWebPath = None
    CONST_PROJECT_START_PATH = "/project"
    CONST_WEB_START_PATH = "/web"
    CONST_WEB_FOLDER = "website"
    CONST_SERVER_FOLDER = "Server"

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
    def doGet(self):
        pass
    #def do_GET(self):
        """Respond to a GET request."""
        """
        if self.path == '/path' :
            super(MyHandler,self).do_Get(self)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("<html><head><title>Title goes here.</title></head>")
        self.wfile.write("<body><p>This is a test.</p>")
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        self.wfile.write("<p>You accessed path: %s</p>" % self.path)
        self.wfile.write("</body></html>")
        """

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        ABOVE FROM PARENT

        This looks at two extra constants to move where it searches for files, one is dynamic and the other is hard coded
        """
        if path.startswith(self.CONST_PROJECT_START_PATH) :
            path = self.parserProjectPath(path)
            return path

        if path.startswith(self.CONST_WEB_START_PATH) :
            if self.currentWebPath is None:
                self.SetWebLocation()
            path = self.currentWebPath + path[len(self.CONST_WEB_START_PATH):]
            print 'printing custom: ' + path
            return path
            
        # abandon query parameters
        path = path.split('?',1)[0]
        path = path.split('#',1)[0]
        path = posixpath.normpath(urllib.unquote(path))
        words = path.split('/')
        words = filter(None, words)
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir): continue
            path = os.path.join(path, word)
        return path

    def parserProjectPath(self, path):
        path = path[len(self.CONST_PROJECT_START_PATH):]
        if path.startswith('/'): # this means that there is no project so we go to default project
            path = path[1:] # cut off the slash
            projectPath = self.translate_path('/')
            totalPath = projectPath[:projectPath.find(self.CONST_SERVER_FOLDER)] + path
            return totalPath

        if not path.startswith('-'): # all others must be a project path
            raise Exception('Invalid project')
        project = path[1:path.find("/")]
        print project
        projectPath = None

        projectP = ProjectManagment.getInstance().getProject(project)
        print projectP
        projectPath = projectP.getProjectDirectory()
        # do proejct look up
        path = projectPath + path[len(project) + 1:]
        print 'printing custom: ' + path
        return path

    def SetWebLocation(self):
        self.currentWebPath = self.translate_path("/")
        self.currentWebPath = self.currentWebPath[:self.currentWebPath.find(self.CONST_SERVER_FOLDER)]
        self.currentWebPath += self.CONST_WEB_FOLDER