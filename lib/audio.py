import alsaaudio


class Audio:
    def __init__(self, startVolume=50):
        self.mixer = alsaaudio.Mixer('PCM')
        self.setVolume(startVolume)
        self.lastVolume = self.getVolume()
        self.isMute = False

    def setVolume(self, percent):
        self.mixer.setvolume(percent)

    def getVolume(self):
        return self.mixer.getvolume()[0]

    def unmute(self):
        self.setVolume(self.lastVolume)
        self.isMute = False

    def mute(self):
        self.lastVolume = self.getVolume()
        self.setVolume(0)
        self.isMute = True

    def volumeUp(self):
        if self.isMute:
            self.unmute()

        vol = self.mixer.getvolume()[0]
        vol += 10

        if vol >= 100:
            vol = 100

        self.setVolume(vol)

    def volumeDown(self):
        if self.isMute:
            self.unmute()

        vol = self.mixer.getvolume()[0]
        vol -= 10

        if vol <= 0:
            vol = 0

        self.setVolume(vol)
