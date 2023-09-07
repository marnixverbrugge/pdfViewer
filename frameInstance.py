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
        self.createFrame()

        # Update general parameters
        parameters.frameNumber += 1
    

    def createFrame(self):
        """ Create tkinter frame """
        h, w = parameters.dictImagesSizes[parameters.imagesSize]
        if parameters.showPageDetails: h+=25
        self.fr = Frame(rW.imageFrame, background='white')
        self.fr.configure(height=h, width=w)
        self.fr.grid_propagate(0)
        self.fr.grid(row=self.row, column=self.column, padx=(10,0), pady=20)
        
        return 


    def createLabel(self, pageName):
        """ Create the initial image label to frame """
        self.pageName = pageName
        # Update frame with page image
        original = Image.open('%s\%s'%(os.getcwd(),pageName))
        h, w = parameters.dictImagesSizes[parameters.imagesSize]
        resized = original.resize((w-8, h-8),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(resized)
        self.label = Label(self.fr, image = img)
        self.label.image=img
        
        self.label.bind("<Button-1>", self.onClick)
        self.label.grid(padx=2, pady=2)

        # Check for details label
        if parameters.showPageDetails: self.addDetailLabel()

        return

    def addDetailLabel(self):
        """ Add pdf and page number to the frame """
        splitName = self.pageName[16:].split('_')
        referencePDFName = splitName[0]
        pageNumber = int(splitName[1][5:-4])
        self.detailLabel = Label(self.fr, text='%s_p %s'%(referencePDFName, pageNumber), bg='white').grid(row=1,padx=2, pady=2)
        return

    def updatePageDetails(self):
        """ Update frame and label """
        self.updateFrameSize()
        if parameters.showPageDetails: self.addDetailLabel()
        return

    def updateFrameSize(self):
        """ Update frame size """
        self.size = parameters.imagesSize
        h, w = parameters.dictImagesSizes[parameters.imagesSize]
        if parameters.showPageDetails: h+=25
        self.fr.configure(height=h, width=w)
        self.updateLabel(self.pageName)
        
        return

    def updateLabel(self, pageName):
        """ Update the existing label by the new pageName"""
        self.pageName = pageName
        # Update frame with page image
        original = Image.open('%s\%s'%(os.getcwd(),pageName))
        h, w = parameters.dictImagesSizes[parameters.imagesSize]
        resized = original.resize((w-8, h-8),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(resized)
        self.label.configure(image=img)
        self.label.image=img
        if parameters.showPageDetails: self.addDetailLabel()
        return
    

    def onClick(self, event):
        """ Operate when user clicks on pdf page / frame """

        # Check if selection is required
        if parameters.currentAction == None: return

        # Check if selection process is done
        print('action')
        if parameters.selectionDone == False:
            if parameters.shiftPressed and self.name not in parameters.currentSelection:
                parameters.currentSelection.add(self.name)
                self.highlight()
            
            elif parameters.shiftPressed and self.name in parameters.currentSelection:
                parameters.currentSelection.remove(self.name)
                self.unhighlight()

            elif parameters.shiftPressed == False and self.name in parameters.currentSelection:
                self.unhighlightAll()
                parameters.currentSelection = set([])

            else:
                self.unhighlightAll()
                parameters.currentSelection = set([self.name])
                self.highlight()
            

        # Go to function after selection
        else:
            if parameters.currentAction == 'swap':
                rW.updateStatusBar('Swap finished')
            if parameters.currentAction == 'insert':
                rW.updateStatusBar('Selected pages are inserted at new location')

            self.unhighlightAll()
            parameters.currentAction = None
            parameters.currentSelection = set([])
            parameters.selectionDone = False


        # # Switch positions
        # if parameters.frameHighlighted != None:
        #     self.changePosition()

        # # Highlight
        # else:
        #     self.highlight()

        return


    def highlight(self):
        """ Highlight frame with red color """
        self.fr.configure(background='red')
        self.selectHighlight = True
        parameters.frameHighlighted = self.name

        return
    
    
    def unhighlight(self):
        """ Unhighlight frame """
        self.fr.configure(background='white')
        self.selectHighlight = False
        parameters.frameHighlighted = None
        return

    def unhighlightAll(self):
        """ Unhighlight all frames """
        for fr in parameters.currentSelection:
            parameters.gridFrames[fr].unhighlight()
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

        