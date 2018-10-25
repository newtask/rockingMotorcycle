import pygame


class AudioMixer:
    def __init__(self):
        pygame.mixer.init()

        self.sounds = {}
        self.channels = []

        self.numChannels = 2
        self.curChannelId = 0

        for i in range(0, self.numChannels):
            self.channels.append(pygame.mixer.Channel(i))

    def addSound(self, id, path):
        self.sounds[id] = path

    def playSound(self, id, loop=False, fadeTime=1000, queueId=None, queueLoop=True):
        nextChannelId = self.curChannelId + 1

        if nextChannelId >= self.numChannels:
            nextChannelId = 0

        curChannel = self.channels[self.curChannelId]
        nextChannel = self.channels[nextChannelId]

        if curChannel.get_busy():
            curChannel.fadeout(fadeTime)
        nextChannel.play(self.sounds[id], -1 if loop else 0)

        if queueId is not None:
            nextChannel.queue(self.sounds[queueId], -1 if queueLoop else 0)

        self.curChannelId = nextChannelId

    def stopSound(self):
        curChannel = self.channels[self.curChannelId]
        curChannel.stop()
