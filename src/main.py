##--------------------------------------------------------------------\
#   matplotlib wxpython example
#   'main.py'
#   Main file for driving project. Creates GUI & adds to main loop
#   Author: Lauren Linkous (LINKOUSLC@vcu.edu)
#   February 2, 2023
##--------------------------------------------------------------------\

# python lib imports
import wx.lib.mixins.inspection as wit

# project file imports
from src.GFrame import GFrame 

def main():

    # GUI
    # create the wxpython based GUI window for displaying the plot and walk model
    app = wit.InspectableApp()
    GF = GFrame(None, title="matplotlib-wxpython-example")
    GF.Show()

    # adding to main loop keeps the gui window open and the program running
    # must be at the end because code after this will not execute while gui window is open
    app.MainLoop()


if __name__ == '__main__':
    main()
