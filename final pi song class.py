from time import time

#song class that the songs inhearet from
class Song(object):
    def __init__(self, noteList):
        #takes song list and sets key to note
        if (len(noteList) == 8):
            self.c_low = noteList[0]
            self.d = noteList[1]
            self.e = noteList[2]
            self.f = noteList[3]
            self.g = noteList[4]
            self.a = noteList[5]
            self.b = noteList[6]
            self.c_high = noteList[8]
        self.name = ""
    #song hot cross buns
    def HotCrossBuns():
        self.name = "hCB"
        song = [[self.b, 0.0], [self.a, 0.5], [self.g, o.5], [self.b, 0.75], [self.a, 0.5], [self.g, 0.5], [self.g, 0.75], [self.g, 0.25], [self.g, 0.25], [self.g, 0.25], [self.a, 0.25], [self.a, 0.25], [self.a, 0.25], [self.a, 0.25], [self.b, 0.5], [self.a, 0.5], [self.g, 0.5]]
        return [self.name, song]

    def song2():
        self.name = "song2"
        song = []
        
