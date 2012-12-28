from ..interfaces.plexInterface import PlexInterface
from ..pyomx.pyomxplayer import OMXPlayer
from urlparse import urlparse
from ..pyplexlogger.logger import pyPlexLogger

class xbmcCommands:
    def __init__(self, omxArgs):
        self.l = pyPlexLogger("xbmcCommands").logger
        self.l.info('Initated xbmcCommands')
        self.media = None
        self.plex = PlexInterface()
        self.omx = None
        self.omxArgs = omxArgs
        self.shutDown = False

    def PlayMedia(self, fullpath, tag, unknown1, unknown2, unknown3):
        self.l.info("playing media from %s" % fullpath)
        global parsed_path
        global media_key
        global duration
        
        parsed_path = urlparse(fullpath)
        media_path = parsed_path.scheme + "://" + parsed_path.netloc + tag

        self.media = self.plex.getMedia(media_path)
        
        #print 'mediapath', mediapath
        if(self.omx):
            self.Stop()
        transcodeURL = self.media.getTranscodeURL()
        normalURL = self.media.fileURL
        print normalURL
        self.omx = OMXPlayer(normalURL, args=self.omxArgs, start_playback=True)

    def Pause(self, message):
        if(self.omx):
            self.omx.set_speed(1)
            self.omx.toggle_pause()

    def Play(self, message):
        if(self.omx):
            ret = self.omx.set_speed(1)
            if(ret == 0):
                self.omx.toggle_pause()

    def Stop(self, message=""):
        if(self.omx):
            self.omx.stop()
            self.omx = None

    def stopPyplex(self, message = None):
        self.shutDown = True

    def SkipNext(self, message = None):
        if(self.omx):
            self.omx.increase_speed()

    def SkipPrevious(self, message = None):
        if(self.omx):
            self.omx.decrease_speed()

    def StepForward(self, message = None):
        if(self.omx):
            self.omx.increase_speed()

    def StepBack(self, message = None):
        if(self.omx):
            self.omx.decrease_speed()

    def BigStepForward(self, message = None):
        if(self.omx):
            self.omx.jump_fwd_600()

    def BigStepBack(self, message = None):
        if(self.omx):
            self.omx.jump_rev_600()

    def getMilliseconds(self,s):
        hours, minutes, seconds = (["0", "0"] + ("%s" % s).split(":"))[-3:]
        hours = int(hours)
        minutes = int(minutes)
        seconds = float(seconds)
        miliseconds = int(3600000 * hours + 60000 * minutes + 1000 * seconds)
        return miliseconds

    def getPosMilli(self):
        return self.getMilliseconds(self.omx.position)
    
    def setPlayed(self):
        self.media.setPlayed()

    def isFinished(self):
        if(self.omx):
            finished = self.omx.finished
        else:
            finished = True
        return finished
    
    def isRunning(self):
        if(self.omx):
            return True
        return False

    def updatePosition(self):
        if self.isFinished():
            if (self.getPosMilli() > (self.media.duration * .95)):
                self.setPlayed()
            self.Stop()
        else:
            self.media.updatePosition(self.getPosMilli())

# test = xbmcCommands('')
# test.PlayMedia('http://192.168.1.201:32400/library/onDeck', '/library/metadata/1713', '+', ' ', ' ')
# self.stopPyplex()