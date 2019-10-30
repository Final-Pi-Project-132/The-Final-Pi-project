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
            self.c_high = noteList[7]
        self.name = ""
        self.song = []
        
    #song hot cross buns
    def HotCrossBuns():
        self.name = "hCB"
        #song notes along with their duration between notes
        self.song = [[self.b, 0.0], [self.a, 0.5], [self.g, o.5], [self.b, 0.75], [self.a, 0.5],\
                     [self.g, 0.5], [self.g, 0.75], [self.g, 0.25], [self.g, 0.25], [self.g, 0.25],\
                     [self.a, 0.25], [self.a, 0.25], [self.a, 0.25], [self.a, 0.25], [self.b, 0.5],\
                     [self.a, 0.5], [self.g, 0.5]]
        
    
    #song twinkle twinkle little star
    def Twinkle_Twinkle():
        self.name = "Twinkle Twinkle Little Star"
        song = [[self.c_low, 0.0], [self.c_low, 0.5], [self.g, 0.5], [self.g, 0.5], [self.a, 0.5], [self.a, 0.5],\
                [self.g, 0.5], [self.f, 0.75], [self.f, 0.5], [self.e, 0.5], [self.e, 0.5],\
                [self.d, 0.5], [self.d, 0.5], [self.c_low, 0.5]]

    #song baby shark
    def Baby_shark():
        self.name= "Baby Shark"
        song = [[self.c_low, 0.0], [self.d, 0.5], [self.f, 0.5], [self.f, 0.25], [self.f, 0.25], [self.f, 0.25], [self.f, 0.25], [self.f, 0.25], [self.f, 0.25],\
                [self.c_low, 0.5], [self.d, 0.5], [self.f, 0.5], [self.f, 0.25], [self.f, 0.25], [self.f, 0.25],\
                [self.f, 0.25], [self.f, 0.25], [self.f, 0.25]]
