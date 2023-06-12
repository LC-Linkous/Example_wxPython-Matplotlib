##--------------------------------------------------------------------\
#   matplotlib wxpython example
#   'GFrame.py'
#   Class for GUI layout and basic functionality for drawing on 3D plot
#   Author(s): Lauren Linkous (LINKOUSLC@vcu.edu)
#   Frbruary 2, 2023
##--------------------------------------------------------------------\

# python lib imports
import datetime
import wx #pip install wxpython
import wx.aui
import matplotlib #pip install matplotlib
from matplotlib.figure import Figure
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import NavigationToolbar2Wx

# project file imports
from node import Node

# default frame/panel sizes
WIDTH = 500
HEIGHT = 500
PANEL_HEIGHT = 450
PANEL_WIDTH = 450

class GFrame(wx.Frame):
    """create window frame and handle close events"""
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent=parent, title=title, size=(WIDTH, HEIGHT))
        

        self.panel_mainUI = MainPanel(self)
        self.mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        self.mainSizer.Add(self.panel_mainUI, -1, wx.EXPAND)
        self.SetSizer(self.mainSizer)

    def onClose(self, event):
        self.Destroy()
    
class MainPanel(wx.Panel):
    """Main object for drawing the base element in the frame"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.parent = parent

        self.panel_design = MainPage(self)
        self.panel_design.Show()

        self.mainUIpanelSizer = wx.BoxSizer(wx.VERTICAL)
        self.mainUIpanelSizer.Add(self.panel_design, 1, wx.EXPAND)
        self.SetSizer(self.mainUIpanelSizer)
  
        self.parent.Layout()  # may need to refresh on some systems


class MainPage(wx.Panel):
    """class of specific elements drawn into panel"""
    def __init__(self, parent):
        wx.Panel.__init__(self, parent=parent)
        self.parent = parent
        self.SetBackgroundColour('MEDIUM AQUAMARINE')

        #static vars for cosmetic features
        INPUT_BOX_WIDTH = 100

        #for UI interaction
        self.runBool = False #true when 'run' is clicked
        self.numNodes = 2
        self.nodeList = [] # each row is a node object
        self.pathType = None
        
        #could be prompted for in the UI, but isn't
        self.minRange = -100
        self.maxRange = 100

        # Left size UI box
        self.boxSelect = wx.StaticBox(self, label='User Inputs')
        self.lblPathType = wx.StaticText(self.boxSelect, label="Type of Path:")
        pathTypes = ['Connected Paths', 'Unconnected Dots', 'Single Dot']
        self.pathDropDown = wx.ComboBox(self.boxSelect, choices=pathTypes)
        self.pathDropDown.SetValue(pathTypes[0])

        self.lblnumNodes = wx.StaticText(self.boxSelect, label="Number of Nodes:")
        self.fieldNumNodes = wx.TextCtrl(self.boxSelect, value="", size=(INPUT_BOX_WIDTH, 20))
        self.fieldNumNodes.SetValue("2")

        self.runBtn = wx.Button(self.boxSelect, label="Run", size=(90, 20))
        self.runBtn.Bind(wx.EVT_BUTTON, self.btnRunClicked)
        self.stopBtn = wx.Button(self.boxSelect, label="Stop", size=(90, 20))
        self.stopBtn.Bind(wx.EVT_BUTTON, self.btnStopClicked)

        #Right side box
        self.boxSummary = wx.StaticBox(self, label='Node Location Summary')
        self.summaryText = wx.StaticText(self.boxSummary, style=wx.ALIGN_LEFT)
        self.updateSummaryBox()

        self.setupCanvas()

        self.layoutPageElements()

    def layoutPageElements(self):
        """put elements into spacers to organize layout"""

        dropSizer = wx.BoxSizer(wx.HORIZONTAL)
        dropSizer.Add(self.lblPathType, 0, wx.ALL, border=7)
        dropSizer.Add(self.pathDropDown, 0, wx.ALL, border=5)

        txtSizer = wx.BoxSizer(wx.HORIZONTAL)
        txtSizer.Add(self.lblnumNodes, 0, wx.ALL, border=5)
        txtSizer.Add(self.fieldNumNodes, 0, wx.ALL, border=5)

        btnSizer = wx.BoxSizer(wx.HORIZONTAL)
        btnSizer.Add(self.runBtn, 0, wx.ALL, border=5)
        btnSizer.Add(self.stopBtn, 0, wx.ALL, border=5)

        IOSizer = wx.BoxSizer(wx.VERTICAL)
        IOSizer.AddSpacer(5) #so input box doesnt overlap with top text
        IOSizer.Add(dropSizer, 0, wx.ALL|wx.EXPAND, border=5)
        IOSizer.Add(txtSizer, 0, wx.ALL|wx.EXPAND, border=5)
        IOSizer.Add(btnSizer, 1, wx.ALL|wx.EXPAND, border=5)
        self.boxSelect.SetSizer(IOSizer)

        summarySizer = wx.BoxSizer(wx.VERTICAL) #used to stop the text field from overwriting the title of the static box
        summarySizer.Add(self.summaryText, 0, wx.ALL|wx.EXPAND, border=15)
        self.boxSummary.SetSizer(summarySizer)
        

        topRowSizer = wx.BoxSizer(wx.HORIZONTAL)
        topRowSizer.Add(self.boxSelect, 1, wx.ALL|wx.EXPAND, border=5)
        topRowSizer.Add(self.boxSummary, 1, wx.ALL|wx.EXPAND, border=5 )

        #main sizer
        pageSizer = wx.BoxSizer(wx.VERTICAL)
        pageSizer.Add(topRowSizer, 1, wx.ALL|wx.LEFT, border=5)
        pageSizer.Add(self.canvas, 3, wx.CENTER)  #the 3d graph
        pageSizer.Add(self.navToolbar, 0,  wx.CENTER)
        self.SetSizer(pageSizer)
       

    def btnRunClicked(self, evt):
        """event triggered either by run btn click or function call. Sets running params."""     
        self.runBool = True
        self.pathType = self.pathDropDown.GetValue()
        numNodes = int(self.fieldNumNodes.GetValue())
        self.createNodes(numNodes)
        self.numNodes = numNodes
        self.step()

    def btnStopClicked(self, evt):
        """event triggered either by stop btn click or function call."""
        self.runBool = False
        
    def setupCanvas(self):
        """"set up the matplotlib figure, canvas, and axes"""
        self.figure = matplotlib.figure.Figure(figsize=(5,3), tight_layout=True)
        self.axes = self.figure.add_subplot(111, projection="3d")
        self.axes.set_xlim(self.minRange, self.maxRange)
        self.axes.set_ylim(self.minRange, self.maxRange)
        self.axes.set_zlim(self.minRange, self.maxRange)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.navToolbar = NavigationToolbar2Wx(self.canvas)
    
    def drawOnCanvas(self):
        """clear old graphed values and redraw updated node locations"""
        self.axes.clear()
        self.axes.set_xlim(self.minRange, self.maxRange)
        self.axes.set_ylim(self.minRange, self.maxRange)
        self.axes.set_zlim(self.minRange, self.maxRange)
        for a in self.nodeList:
            l = a.getPastLocs()
            x,y,z = zip(*l)
            if self.pathType == 'Connected Paths':                
                self.axes.plot3D(x,y,z)
                        
            elif self.pathType == 'Unconnected Dots':
                self.axes.scatter3D(x,y,z)
            
            else: #'Single Dot'
                self.axes.scatter3D(x[-1],y[-1],z[-1])

        self.canvas.draw()
        
    def updateSummaryBox(self):
        """update the textbox for the summary of node coordinate locations"""
        txt = ""
        ctr = 1
        for a in self.nodeList:
            l = a.getCurrentLoc()
            tmpTxt = "Node " + str(ctr) + ": " + str(l) +"\n"   
            txt = txt + tmpTxt
            ctr = ctr + 1

        self.summaryText.SetLabel(txt)

    def createNodes(self, numNodes):
        """create nodes that will populate the 3D plot"""
        self.nodeList = []
        for n in range(numNodes):
            a = Node(self.minRange, self.maxRange)
            self.nodeList.append(a)
  

    def step(self):
        """make each node take 1 step forward in their walk model if run button was hit"""
        if self.runBool == True:
            for a in self.nodeList:
                a.randomWalk()
            
            self.drawOnCanvas()
            self.updateSummaryBox()
            #if stop button hasn't been hit, then keep looping
            wx.CallLater(200, self.step) #call every 200ms
            #print(str(self.numNodes) + "," + str(datetime.datetime.now()))

