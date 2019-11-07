# Xylophone Class

##### TO DEBUG.
## NEED TO GO TO IF RECORDING AND MAKE AN IF ELSE STATEMENT.
## IF TIME = INIT TIME, DONT COUNT IT, IT IS THE BUG

import RPi.GPIO as GPIO
from time import sleep, time
import pygame
from array import array
from math import sin, pi
from final_pi_song_class import *

# CONSTANTS
MIXER_FREQ = 44100
MIXER_SIZE = -16
MIXER_CHANS = 1
MIXER_BUFF = 1024

# a class that contains notes
# a note has a pin number, a light, and a sound
class Note(pygame.mixer.Sound):

    def __init__(self, input, output, f, vol, string):
        self.inPin = input
        self.outPin = output
        self.frequency = f
        self.name = string
        # initialize the note using an array of samples
        pygame.mixer.Sound.__init__(self, buffer=self.build_samples())
        self.set_volume(vol)

    # builds an array of samples for the current note
    def build_samples(self):
        # calculate the period and amplitude of the note's wave
        period = int(round(MIXER_FREQ / self.frequency))
        amplitude = 2 ** (abs(MIXER_SIZE) - 1) - 1
        # initialize the note's samples (using an array of
        # signed 16-bit "shorts")
        samples = array("h", [0] * period)
        # generate the note's samples
        for t in range(period):
            samples[t] = int(amplitude * sin((float(2* pi) / period) * t)) 
        return samples

    # accessor methods
    
    @property
    def inPin(self):
        return self._inPin

    @property
    def outPin(self):
        return self._outPin

    @property
    def frequency(self):
        return self._frequency

    @property
    def name(self):
        return self._name

    # mutator methods

    @inPin.setter
    def inPin(self, pin):
        self._inPin = pin

    @outPin.setter
    def outPin(self, pin):
        self._outPin = pin

    @frequency.setter
    def frequency(self, value):
        self._frequency = value

    @name.setter
    def name(self, string):
        self._name = string
        
    def __str__(self):
        return self.name
    

# will create an xylophone with 8 notes and 8 lights
# will pass in two lists that have the pin locations for the lights and leds
class Xylophone(object):

    GPIO.setmode(GPIO.BCM)
    pygame.mixer.pre_init(MIXER_FREQ, MIXER_SIZE, MIXER_CHANS, MIXER_BUFF)
    pygame.init()

    # CLASS VARIABLES
    # variable that says if the xylophone is in free play or not
    freePlayVar = True

    # variable that says if it is recording or not
    isRecording = False
    
    # a dictionary that contains all recordings
    masterRecordings = {}

    # a dictionary that contains all the songs we have
    masterSongs = {}

    # a debugging boolean
    DEBUG = False

    # variable that says if the xylophone is in learning mode or not

    def __init__(self, noteList, songList):
        # if the list has 8 keys in it, then assign the pins to the notes,
        # lowest notes to highest
        if(len(noteList) == 8):
            self.c_low = noteList[0]
            self.d = noteList[1]
            self.e = noteList[2]
            self.f = noteList[3]
            self.g = noteList[4]
            self.a = noteList[5]
            self.b = noteList[6]
            self.c_high = noteList[7]

        # a for loop add each song to the master song dictionary
        for x in range(len(songList)):
            # access the song. which is a list of a name (str)
            # make a key-value pair of the name of the song and the actual song
            Xylophone.masterSongs[songList[x].name] = songList[x].song

        # create a recording variable to store the songs made
        self.recording = []

    # accessor methods
    
    @property
    def c_low(self):
        return self._c_low

    @property
    def d(self):
        return self._d

    @property
    def e(self):
        return self._e

    @property
    def f(self):
        return self._f

    @property
    def g(self):
        return self._g

    @property
    def a(self):
        return self._a

    @property
    def b(self):
        return self._b

    @property
    def c_high(self):
        return self._c_high

    @property
    def recording(self):
        return self._recording

    # mutator methods

    @c_low.setter
    def c_low(self, note):
        self._c_low = note

    @d.setter
    def d(self, note):
        self._d = note

    @e.setter
    def e(self, note):
        self._e = note

    @f.setter
    def f(self, note):
        self._f = note

    @g.setter
    def g(self, note):
        self._g = note

    @a.setter
    def a(self, note):
        self._a = note

    @b.setter
    def b(self, note):
        self._b = note

    @c_high.setter
    def c_high(self, note):
        self._c_high = note

    @recording.setter
    def recording(self, newRec):
        self._recording = newRec

    # function to set up GPIO input pins (the notes)
    def inputSetUp(self):
        GPIO.setup(self.c_low.inPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.d.inPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.e.inPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.f.inPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.g.inPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.a.inPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.b.inPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.c_high.inPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        
    # function to set up the GPIO output pins (the lights)
    def outputSetUp(self):
        GPIO.setup(self.c_low.outPin, GPIO.OUT)
        GPIO.setup(self.d.outPin, GPIO.OUT)
        GPIO.setup(self.e.outPin, GPIO.OUT)
        GPIO.setup(self.f.outPin, GPIO.OUT)
        GPIO.setup(self.g.outPin, GPIO.OUT)
        GPIO.setup(self.a.outPin, GPIO.OUT)
        GPIO.setup(self.b.outPin, GPIO.OUT)
        GPIO.setup(self.c_high.outPin, GPIO.OUT)

    # function to set up the Xylophone
    def setUpXylophone(self):
        self.inputSetUp()
        self.outputSetUp()

    # function that prepares the recording
    # i.e. cuts out any silence in the beginning, and finds time inbetween each note
    def prepRecording(self, rec):
        # a temporary variable
        temp = 0
        # a for loop the length of the recording
        for note in range(len(rec)):
            # get the note and time list from the recording
            # we will call this the instance (of the note)
            instance = rec[note]

            # checks to see if it note is the first in the recording
            if(note == 0):
                temp = instance[1]
                instance[1] = 0
                rec[note] = instance
                
            else:
                # the time of the previous instance
                previous_time = temp
                # now we will go to the time of the instance
                time = instance[1]
                # set that time to the temp variable
                temp = time
                # now subtract the previous instance's time from the time of the note
                # this allows us to know what time a note was played
                    # after the previous note
                time = time - previous_time
                # make this the new time of the note
                instance[1] = time
                rec[note] = instance
        # return the recording
        return rec

    # function that plays back the recording
    def playBack(self, rec):
        # a small quirk needed to make the instance[0].outPin work
        # without the following lines, you get 'RuntimeError: Please
            # set pin numbering mode using GPIO.setmode(GPIO.BOARD)
            # or GPIO.setmode(GPIO.BCM)'
        GPIO.setmode(GPIO.BCM)
        self.setUpXylophone()

        # a for loop the length of the recording
        for note in range(len(rec)):
            # instance is the list of the note and time 
            instance = rec[note]
            # wait until it is time to play the note
            sleep(instance[1])
            # play the instance's note
            instance[0].play(-1)
            # light up its respective light
            GPIO.output(instance[0].outPin, GPIO.HIGH)
            # wait before turning it all off
            sleep(0.07)
            # turn off sound
            instance[0].stop()
            # turn off light
            GPIO.output(instance[0].outPin, GPIO.LOW)

        # clean up the GPIO
        GPIO.cleanup()
            
    
    # function that has the user just play on the piano for fun (no learning)
    def freePlay(self):
        # if they are recording the free play, start a timer
        if(Xylophone.isRecording):
            # a list to record lists of every note played and when it was played
            self.recording = []
        
        # as long as free play is true
        while(Xylophone.freePlayVar):
            GPIO.setmode(GPIO.BCM)
            self.setUpXylophone()
            
            # The lights will only play if the note is hit
            if(GPIO.input(self.c_low.inPin)==GPIO.HIGH):
                GPIO.output(self.c_low.outPin, GPIO.HIGH)
                # play the note
                c_low.play(-1)
                sleep(0.1)
                c_low.stop()
                # if the song is being recorded
                if(Xylophone.isRecording):
                    # a list containing the note and time will be appended to the recording list
                    noteInstance = [self.c_low, time()]
                    # add it to the recording list
                    self.recording.append(noteInstance)
            # turn off the LED
            GPIO.output(self.c_low.outPin, GPIO.LOW)
            

            if(GPIO.input(self.d.inPin)==GPIO.HIGH):
                GPIO.output(self.d.outPin, GPIO.HIGH)
                # play the note
                d.play(-1)
                sleep(0.1)
                d.stop()
                if(Xylophone.isRecording):
                    # a list containing the note and time will be appended to the recording list
                    noteInstance = [self.d, time()]
                    # add it to the recording list
                    self.recording.append(noteInstance)
            # turn off the LED
            GPIO.output(self.d.outPin, GPIO.LOW)

            if(GPIO.input(self.e.inPin)==GPIO.HIGH):
                GPIO.output(self.e.outPin, GPIO.HIGH)
                # play the note
                e.play(-1)
                sleep(0.1)
                e.stop()
                if(Xylophone.isRecording):
                    # a list containing the note and time will be appended to the recording list
                    noteInstance = [self.e, time()]
                    # add it to the recording list
                    self.recording.append(noteInstance)
            # turn off the LED
            GPIO.output(self.e.outPin, GPIO.LOW)

            if(GPIO.input(self.f.inPin)==GPIO.HIGH):
                GPIO.output(self.f.outPin, GPIO.HIGH)
                # play the note
                f.play(-1)
                sleep(0.1)
                f.stop()
                if(Xylophone.isRecording):
                    # a list containing the note and time will be appended to the recording list
                    noteInstance = [self.f, time()]
                    # add it to the recording list
                    self.recording.append(noteInstance)
            # turn off the LED
            GPIO.output(self.f.outPin, GPIO.LOW)

            if(GPIO.input(self.g.inPin)==GPIO.HIGH):
                GPIO.output(self.g.outPin, GPIO.HIGH)
                # play the note
                g.play(-1)
                sleep(0.1)
                g.stop()
                if(Xylophone.isRecording):
                    # a list containing the note and time will be appended to the recording list
                    noteInstance = [self.g, time()]
                    # add it to the recording list
                    self.recording.append(noteInstance)
            # turn off the LED
            GPIO.output(self.g.outPin, GPIO.LOW)

            if(GPIO.input(self.a.inPin)==GPIO.HIGH):
                GPIO.output(self.a.outPin, GPIO.HIGH)
                # play the note
                a.play(-1)
                sleep(0.1)
                a.stop()
                if(Xylophone.isRecording):
                    # a list containing the note and time will be appended to the recording list
                    noteInstance = [self.a, time()]
                    # add it to the recording list
                    self.recording.append(noteInstance)
            # turn off the LED
            GPIO.output(self.a.outPin, GPIO.LOW)

            if(GPIO.input(self.b.inPin)==GPIO.HIGH):
                GPIO.output(self.b.outPin, GPIO.HIGH)
                # play the note
                b.play(-1)
                sleep(0.1)
                b.stop()
                if(Xylophone.isRecording):
                    # a list containing the note and time will be appended to the recording list
                    noteInstance = [self.b, time()]
                    # add it to the recording list
                    self.recording.append(noteInstance)
            # turn off the LED
            GPIO.output(self.b.outPin, GPIO.LOW)

            if(GPIO.input(self.c_high.inPin)==GPIO.HIGH):
                GPIO.output(self.c_high.outPin, GPIO.HIGH)
                # play the note
                c_high.play(-1)
                sleep(0.1)
                c_high.stop()
                if(Xylophone.isRecording):
                    # a list containing the note and time will be appended to the recording list
                    noteInstance = [self.c_high, time()]
                    # add it to the recording list
                    self.recording.append(noteInstance)
            # turn off the LED
            GPIO.output(self.c_high.outPin, GPIO.LOW) 

        
        GPIO.cleanup()

        # add the recording to the master recording dictionary
        if(Xylophone.isRecording and (len(self.recording) > 0)):
            rec = self.prepRecording(self.recording)
            self.recording = rec
            Xylophone.masterRecordings["Recording " + str(len(Xylophone.masterRecordings) + 1)] = self.recording
        if(Xylophone.DEBUG):
            print("Finished Freeplay")
            #print(self.recording)
            #print(Xylophone.masterRecordings)
            self.playBack(Xylophone.masterRecordings["Recording "+str(len(Xylophone.masterRecordings))])

    # function that plays a song to you
    # it is essentially the playback function
    def playSong(self, comp):
        # get the song aspect of the "song instance"
        song = comp.song
        # this song variable is essentially the rec variable for playback
        self.playBack(song)
        

    # function that teaches you a song
    def learnSong(self, comp):
        # a small quirk needed to make the instance[0].outPin work
        # without the following lines, you get 'RuntimeError: Please
            # set pin numbering mode using GPIO.setmode(GPIO.BOARD)
            # or GPIO.setmode(GPIO.BCM)'
        GPIO.setmode(GPIO.BCM)
        self.setUpXylophone()

        # if they are recording the learning session, start a timer
        if(Xylophone.isRecording):
            # a list to record lists of every note played and when it was played
            self.recording = []

        # get the song aspect of the "song instance"
        song = comp.song
        for x in range(len(song)):
            # the note instance is the list of the note and time
            noteInstance = song[x]
            # sleep until the note needs to be played
            sleep(noteInstance[1])
            # turn on the note's respective LED
            GPIO.output(noteInstance[0].outPin, GPIO.HIGH)
            # do nothing until the key is hit
            while(True):
                if(GPIO.input(noteInstance[0].inPin)==GPIO.HIGH):
                    break
            # play the note
            noteInstance[0].play(-1)
            sleep(0.1)
            noteInstance[0].stop()
            # if the song is being recorded
            if(Xylophone.isRecording):
                # a list containing the note and time will be appended to the recording list
                instance = [noteInstance[0], time()]
                # add it to the recording list
                self.recording.append(instance)
            # turn off the light
            GPIO.output(noteInstance[0].outPin, GPIO.LOW)
        # prep the recording and add it to the master list of recordings
        if(Xylophone.isRecording):
            rec = self.prepRecording(self.recording)
            self.recording = rec
            Xylophone.masterRecordings["Recording " + str(len(Xylophone.masterRecordings) + 1)] = self.recording
            
        if(Xylophone.DEBUG):
            print("DONE!")
            self.playBack(Xylophone.masterRecordings["Recording "+str(len(Xylophone.masterRecordings))])

        # clean up the GPIO
        #GPIO.cleanup()
            

# create Notes
c_low = Note(27, 25, 261.63, 1, "Low C")
d = Note(4, 24, 293.67, 1, "D")
e = Note(5, 23, 329.63, 1, "E")
f = Note(6, 22, 349.23, 1, "F")
g = Note(12, 21, 391.99, .8, "G")
a = Note(13, 20, 440, .7,"A")
b = Note(16, 19, 493.88, .5, "B")
c_high = Note(17, 18, 523.25, .4, "High C")

# create note list
noteList = [c_low, d, e, f, g, a, b, c_high]
# create songs
hcb = Song(noteList)
hcb.HotCrossBuns()
twinkle = Song(noteList)
twinkle.Twinkle_Twinkle()
bbyShrk = Song(noteList)
bbyShrk.Baby_Shark()
# create a song list
songList = [hcb, twinkle, bbyShrk]
#initialize the Xylophone
xy = Xylophone(noteList, songList)
xy.setUpXylophone()
#xy.freePlay()
#xy.learnSong(hcb)
#xy.playSong(hcb)
#sleep(1)
#xy.playSong(twinkle)
#sleep(1)
#xy.playSong(bbyShrk)
