# import all of tkinter for the gui to run
from Tkinter import*
# import Xylophone Class
from Xylophone import *
# import threading class
import threading

# The main screen class that initalizes each menu/ screen with a name and image
class Screen(object):
    def __init__(self, name, image):
        self.name = name
        self.image = image

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

# Menu class the inherits from frame that displays images and buttons for each
# that the user interacts with
class Menu(Frame):
    # constructor inherits from parent within tkinter
    def __init__(self, parent):
    # call the constructor in the superclass
        Frame.__init__(self, parent)

    # This function creatues the 4 Menu Screens that each have a name and a file
    # name that will be used later
    def createMenus(self):
        # Create the menus that the Menu/ simulator will have.
        # This number can be changed later for accomidations.
        global m1
        m1 = Screen('Menu 1', 'main.gif')
        global m2
        m2 = Screen('Menu 2', 'menu.gif')
        global m3
        m3 = Screen('Menu 3', 'freeplay.gif')
        global m4
        m4 = Screen('Menu 4', 'recording.gif')
        # by default the first menu is set to m1
        Menu.currentScreen = m1

    def setupGUI(self):
            # organize the GUI
        self.pack(fill=BOTH, expand=1)
            # the widget is a Tkinter Label
        img = None
        Menu.image = Label(self,image=img)
        Menu.image.image = img
        Menu.image.pack(fill = X and Y)#side = BOTH, fill=Y)
        Menu.image.pack_propagate(False)

    # this takes the current screen and haas the correct photo display as the background
    def setMenuImage(self):
        Menu.img = PhotoImage(file = Menu.currentScreen.image)
        Menu.image.config(image=Menu.img)
        Menu.image.image = Menu.img

    # This is the fuction of the "PLAY" button that is displayed on the first Menu
    def playButton(self):
        # changes the current Screen to m2 (the next menu)
        Menu.currentScreen = m2
        # It also creates the backbutton that is used to go back to previous Menus.
        # The back button is defined later but referenced here to display it.
        self.create_backButton()
        # calls the setMenuImage function once again to refresh the change made
        # otherwise the menu picture would not be changed.
        self.setMenuImage()
        # Calls a function that is made later.
        # It displays the buttons for the m2 Menu.
        self.selectionScreenButtons()
        # This function, which is implimented later, removes the play button.
        self.removePlayButton()

    # a function to begin threading the freePlay function
    def start_freePlay_thread(self, event):
        global freePlay_thread 
        freePlay_thread = threading.Thread(target=self.freeplayButton)
        freePlay_thread.daemon = True
        freePlay_thread.start()
        window.after(10, self.check_freePlay_thread)

    # a function to check freePlay function
    def check_freePlay_thread(self):
        if(freePlay_thread.is_alive()):
            window.after(1000, self.check_freePlay_thread)
        
    def freeplayButton(self):
        # Same type of operation as above
        Menu.currentScreen = m3
        self.setMenuImage()
        # These two functions remove the buttons from the selection screen
        # which is also known as m3.
        self.removeFreeplayButton()
        self.removeSongButton()
        # Calls a fuction that displays the buttons for the next screen
        self.recordButtons()
        Xylophone.freePlayVar = True
        xylophone.freePlay()

    def songLearningButton(self):
        Menu.currentScreen = m4
        #self.backButton()
        self.userSongs()
        self.setMenuImage()
        self.removeFreeplayButton()
        self.removeSongButton()
        self.recordButtons()

    def hotcrossbuns(self):
        xylophone.learnSong(hcb)

    def babyshark(self):
        xylophone.learnSong(bbyShrk)

    def twinkle_Twinkle(self):
        xylophone.learnSong(twinkle)

    # This is the function that is triggered when the back button is clicked
    def backButtonFunction(self):
        # if the current screen is m2 its changed to m1 etc.
        if Menu.currentScreen == m2:
            Menu.currentScreen = m1
        # only thing that is different here is that, the fuction of the first button
        # (the 'PLAY' button) is triggered, so the process basically repeats itself
        # however, we remove the start and stop recording buttons.
        # We also remove the back button, otherwise two buttons would be displayed
        elif Menu.currentScreen == m3:
            Menu.currentScreen = m2
            self.playButton()
            self.removeStartButton()
            self.removeStopButton()
            back.pack_forget()
            # set Free Play to false
            Xylophone.freePlayVar = False
        # same idea here
        elif Menu.currentScreen == m4:
            Menu.currentScreen = m2
            self.playButton()
            self.removeStartButton()
            self.removeStopButton()
            hotcross.pack_forget()
            shark.pack_forget()
            twink.pack_forget()
            back.pack_forget()

    # This creates the button on the title screen (m1)
    # and when its pressed the command calls the playButton function which was
    # mentioned earlier
    def firstButton(self):
        global playbutton
        playbutton = Button(window, text = 'PLAY', command = self.playButton)
        playbutton.pack()

    # Also a remove fuction that removes the button for the next screen
    def removePlayButton(self):
        playbutton.pack_forget()

    # creates the buttons for the selection screen or 'm2'
    def selectionScreenButtons(self):
        # freeplayButton takes the user to the freeplay screen 'm3'
        global freeplaybutton
        freeplaybutton = Button(window, text = 'Freeplay', command = lambda:self.start_freePlay_thread(None))
        freeplaybutton.pack(side = LEFT)
        # the songLearningButton takes the user to the songLearning screen 'm4'
        global songbutton
        songbutton = Button(window, text = 'Song Learning', command = self.songLearningButton)
        songbutton.pack(side = RIGHT)

    # Removes the freeplay and song button once the user leaves selection screen
    # page
    def removeFreeplayButton(self):
        freeplaybutton.pack_forget()

    def removeSongButton(self):
        songbutton.pack_forget()

    # buttons that trigger the recording fuctions within the Xylophone code
    def recordButtons(self):
        global start
        start = Button(window, text = 'Start Recording', command = self.startrecording)
        start.pack(side = LEFT)
        global stop
        stop = Button(window, text = 'Stop Recording', command = self.stoprecording)
        stop.pack(side = RIGHT)

    # creates the back button which helps the user navigate the menus
    def create_backButton(self):
        global back
        back = Button(window, text = 'Go Back', command = self.backButtonFunction)
        if Menu.currentScreen != m1:
            back.pack(side = BOTTOM)

    def userSongs(self):
        global hotcross
        hotcross = Button(window, text = 'Hot Cross Buns', command = self.hotcrossbuns)
        hotcross.pack()
        global shark
        shark = Button(window, text = 'Baby Shark', command = self.babyshark)
        shark.pack()
        global twink
        twink = Button(window, text = 'Twinkle, Twinkle', command = self.twinkle_Twinkle)
        twink.pack()
        
    # start the recording
    def startrecording(self):
        Xylophone.isRecording = True        

    # stop the recording
    def stoprecording(self):
        Xylophone.isRecording = False

    def removeStartButton(self):
        start.pack_forget()

    def removeStopButton(self):
        stop.pack_forget()
    
    # play the Menu
    def play(self):
        self.createMenus()
        self.setupGUI()
        self.firstButton()
        self.setMenuImage()

# a function to make everything needed for the Xylophone instance
def makeXylophone():
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

    # initialize the Xylophone
    xy = Xylophone(noteList, songList)
    xy.setUpXylophone()

    # return the xylophone
    return xy

GPIO.setwarnings(False)         

# make a global xylophone
global xylophone
xylophone = makeXylophone()

# set up the GUI
WIDTH = 900
HEIGHT = 900
window = Tk()
window.title("Xylophone Simulator")
s = Menu(window)
# play the Menu
s.play()
window.mainloop()

