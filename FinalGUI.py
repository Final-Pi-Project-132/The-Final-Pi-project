# import all of tkinter for the gui to run
from Tkinter import*

def m1Button(self):
    Menu.currentScreen == m2

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
    def __init__(self, parent):
    # call the constructor in the superclass
        Frame.__init__(self, parent)
    def createMenus(self):
        # Create the menus that the Menu/ simulator will have.
        # This number can be changed later for accomidations.
        global m1
        m1 = Screen('Menu 1', 'main.gif')
        global m2
        m2 = Screen('Menu 2', 'screen2.gif')
        global m3
        m3 = Screen('Menu 3', 'screen3.gif')
        global m4
        m4 = Screen('Menu 4', 'screen4.gif')
        Menu.currentScreen = m1

    def setupGUI(self):
            # organize the GUI
        self.pack(fill=BOTH, expand=1)
            # give it focus so the player doesn't have to click on it
            # setup the image to the left of the GUI
            # the widget is a Tkinter Label
            # don't let the image control the widget's size
        img = None
        Menu.image = Label(self,image=img)
        Menu.image.image = img
        Menu.image.pack(fill = X and Y)#side = BOTH, fill=Y)
        #Menu.image.pack_propagate(False)
            # setup the text to the right of the GUI
            # first, the frame in which the text will be placed

    def setMenuImage(self):
        Menu.img = PhotoImage(file = Menu.currentScreen.image)
        Menu.image.config(image=Menu.img)
        Menu.image.image = Menu.img


    def createButtons(self):
        if Menu.currentScreen == m1:
            button1 = PhotoImage(file = 'button1.gif')
            Button(window, text = 'PLAY', image = button1, command = m1Button).pack(side = TOP)

        # play the Menu
    def play(self):
        # add the rooms to the Menu
        self.createMenus()
        # configure the GUI
        self.setupGUI()
        # set the current room
        self.setMenuImage()
        self.createButtons()
        #self.callback()

WIDTH = 900
HEIGHT = 900
window = Tk()
window.title("Xylophone Simulator")
# create the GUI as a Tkinter canvas inside the window
#b1 = Button(master, text = 'PLAY')
# place can specify the button's coordinates
#b.place(w = 100, y = 100, relwidth = 50, relheight = 50, width = -50, height = -50, anchor = 'c')
#b.pack(fill = BOTH)#height = 10, width = 10)
s = Menu(window)
# play the Menu
s.play()
#s.btn.pack(side = 'top')
window.mainloop()
