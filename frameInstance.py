"""
Module containing the ImageFrame class
"""

# General imports
from tkinter import *
import os
from PIL import ImageTk, Image

# Custom imports
import parameters
import rootWindow as rW

###
## CLASSES
###

class ImageFrame:
    """ Creates a frame to include tkinter label """
    def __init__(self):
        """Initial function of the ImageFrame isntance"""
        # General assignment
        self.row = parameters.row
        self.column = parameters.column
        self.name = parameters.frameNumber
        self.pageName = None
        self.selectHighlight = False
        self.createFrame((88, 68))

        # Update general parameters
        parameters.frameNumber += 1
    

    def createFrame(self, size):
        """ Create tkinter frame """
        self.fr = Frame(rW.imageFrame, background='white')
        self.fr.configure(height=size[0],width=size[1])
        self.fr.grid_propagate(0)
        self.fr.grid(row=self.row, column=self.column, pady=20)
        
        return 


    def createLabel(self, pageName):
        """ Create the initial image label to frame """
        self.pageName = pageName
        # Update frame with page image
        original = Image.open('%s\%s'%(os.getcwd(),pageName))
        resized = original.resize((60, 80),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(resized)
        self.label = Label(self.fr, image = img)
        self.label.image=img
        
        self.label.bind("<Button-1>", self.onClick)
        self.label.grid(padx=2, pady=2)

        return
    

    def updateLabel(self, pageName):
        """ Update the existing label by the new pageName"""
        self.pageName = pageName
        # Update frame with page image
        original = Image.open('%s\%s'%(os.getcwd(),pageName))
        resized = original.resize((60, 80),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(resized)
        self.label.configure(image=img)
        self.label.image=img

        return
    

    def onClick(self, event):
        """ Operate when user clicks on pdf page / frame """
        # Switch positions
        if parameters.frameHighlighted != None:
            self.changePosition()

        # Highlight
        else:
            self.highlight()

        return


    def highlight(self):
        """ Highlight frame with red color """
        self.fr.configure(background='red')
        self.selectHighlight = True
        if parameters.frameHighlighted != None:
            parameters.gridFrames[parameters.frameHighlighted].unhighlight()
        parameters.frameHighlighted = self.name

        return
    
    
    def unhighlight(self):
        """ Unhighlight frame """
        self.fr.configure(background='white')
        self.selectHighlight = False
        parameters.frameHighlighted = None
        return

    def changePosition(self):
        """ Function to switch pdf pages """
        selectedFrameName = parameters.frameHighlighted
        selectedPageName = parameters.gridFrames[parameters.frameHighlighted].pageName

        # Update the previous selected frame
        parameters.gridFrames[selectedFrameName].updateLabel(str(self.pageName))
        parameters.gridFrames[selectedFrameName].unhighlight()

        # Update self
        self.updateLabel(str(selectedPageName))

        return

        