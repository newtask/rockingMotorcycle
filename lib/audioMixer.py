import threading
import time

import pygame


class SoundQueueItem:
    def __init__(self):
        self.id = None
        self.loop = False


class AudioMixer(threading.Thread):
    def __init__(self):
        super().__init__()
        pygame.mixer.init()

        self.sounds = {}
        self.channels = []

        self.numChannels = 2
        self.curChannelId = 0

        self.listener = None

        self.queuedSounds = []

        for i in range(0, self.numChannels):
            channel = pygame.mixer.Channel(i)
            self.channels.append(channel)

        self.running = True
        self.start()

    def stop(self):
        self.running = False

        for channel in self.channels:
            channel.stop()

    def setListener(self, listener):
        self.listener = listener

    def run(self):
        while self.running:
            if len(self.queuedSounds) > 0:

                isBusy = False

                for channel in self.channels:
                    if channel.get_busy() == 1:
                        isBusy = True

                # print("Is busy: {}".format(isBusy))
                if isBusy is False:
                    item = self.queuedSounds.pop(0)
                    self.playSound(item.id, item.loop)

            time.sleep(0.1)

    def addSound(self, id, path):
        self.sounds[id] = pygame.mixer.Sound(path)

    def getNextChannel(self):
        nextChannelId = self.getNextChannelId()
        return self.channels[nextChannelId]

    def playSound(self, id, loop=False, fadeTime=1000):
        print("Play sound: {}, loop: {}, fadeTime: {}".format(id, loop, fadeTime))

        nextChannelId = self.getNextChannelId()

        curChannel = self.channels[self.curChannelId]
        nextChannel = self.channels[nextChannelId]

        if curChannel.get_busy():
            curChannel.fadeout(fadeTime)

        nextChannel.play(self.sounds[id], -1 if loop else 0)

        if self.listener is not None:
            self.listener(id)

        self.curChannelId = nextChannelId

    def queue(self, id, loop):
        item = SoundQueueItem()
        item.id = id
        item.loop = loop

        self.queuedSounds.append(item)

    def clearQueue(self):
        while len(self.queuedSounds) > 0:
            self.queuedSounds.pop()

    def stopSound(self):
        curChannel = self.channels[self.curChannelId]
        curChannel.stop()
        nextChannel = self.channels[self.getNextChannelId()]
        nextChannel.stop()

    def getNextChannelId(self):
        nextChannelId = self.curChannelId + 1

        if nextChannelId >= self.numChannels:
            nextChannelId = 0

        return nextChannelId
