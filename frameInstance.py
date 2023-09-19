"""
Module containing the ImageFrame class


The object creates tkinter frame and labels. Mouse functions are 
binded to the frame allowing selection and highlighting for the 
functions swap, insert and delete.

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
    def __init__(self, labelAll=False):
        """Initial function of the ImageFrame isntance"""
        # General assignment
        self.row = parameters.row
        self.column = parameters.column
        self.name = parameters.frameNumber
        self.pageName = None
        self.selectHighlight = False
        self.labelAll = labelAll
        self.createFrame()

        # Update general parameters
        parameters.frameNumber += 1
    

    def createFrame(self):
        """ Create tkinter frame """
        
        # Get image size
        h, w = parameters.dictImagesSizes[parameters.imagesSize]
        
        # Update frame hide to include page description
        if parameters.showPageDetails: 
            h+=25

        # Create and grid frame
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
        
        # Add mouse binding to frame
        self.label.bind("<Button-1>", self.onClick)
        self.label.grid(padx=2, pady=2)

        # Check if page description details are required
        if parameters.showPageDetails: 
            self.addDetailLabel()

        return


    def addDetailLabel(self):
        """ Add pdf and page number to the frame """
        splitName = self.pageName[16:].split('_')
        referencePDFName = splitName[0]

        # Create description label text
        if self.labelAll:
            self.detailLabel = Label(self.fr, text='%s_All'%(referencePDFName), bg='white').grid(row=1,padx=2, pady=2)
        else:
            pageNumber = int(splitName[1][5:-4])
            self.detailLabel = Label(self.fr, text='%s_p %s'%(referencePDFName, pageNumber), bg='white').grid(row=1,padx=2, pady=2)
       
        return


    def updatePageDetails(self):
        """ Update frame and label """
        self.updateFrameSize()
        
        if parameters.showPageDetails: 
            self.addDetailLabel()

        return


    def updateFrameSize(self):
        """ Update frame size """
        self.size = parameters.imagesSize
        h, w = parameters.dictImagesSizes[parameters.imagesSize]
        
        # Create label space
        if parameters.showPageDetails:
            h+=25
        
        self.fr.grid_propagate(0)
        self.fr.configure(height=h, width=w)
        self.updateLabel(self.pageName)
        
        return


    def updateLabel(self, pageName):
        """ Update the existing label by the new pageName"""
        self.pageName = pageName
        
        # Update labelAll
        if pageName[-8:] == '_All.png':
            self.labelAll = True
        else:
            self.labelAll = False

        # Update frame with page image
        original = Image.open('%s\%s'%(os.getcwd(),pageName))
        h, w = parameters.dictImagesSizes[parameters.imagesSize]
        resized = original.resize((w-8, h-8),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(resized)
        self.label.configure(image=img)
        self.label.image=img
        
        if parameters.showPageDetails: 
            self.addDetailLabel()
        
        return
    

    def onClick(self, event):
        """ Operate when user clicks on pdf page / frame """

        # Check if selection is required
        if parameters.currentAction == None: return

        # Swap function
        if parameters.currentAction == 'swap':
            self.swapPages()

        # Insert function
        elif parameters.currentAction == 'insert':
            self.insertPages()
           
        # Delete function
        elif parameters.currentAction == 'delete':
            self.deletePages()

        return


    def highlight(self, color='red'):
        """ Highlight frame with color """
        self.fr.configure(background=color)
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


    def swapPages(self):
        """ Swap pages function active """
        
        # Switch positions
        if parameters.frameHighlighted != None:
            self.changePosition()

        # Highlight
        else:
            self.highlight()

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


    def insertPages(self):
        """ Function to insert selected pages to new position """
        
        # Check if selection process is done
        if parameters.selectionDone == False: 
            self.multiSelect()
        
        else:
            # Select page to know insert location in green
            if parameters.secondPageSelection == None:
                parameters.secondPageSelection = self.name
            
            # Re-select insert page location
            else:
                if parameters.secondPageSelection in parameters.currentSelection:
                    parameters.gridFrames[parameters.secondPageSelection].highlight()
                    parameters.secondPageSelection = self.name
                else:
                    parameters.gridFrames[parameters.secondPageSelection].unhighlight()
                    parameters.secondPageSelection = self.name
            self.highlight('green')

        return
        

    def multiSelect(self):
        """ Function to select multiple pages """

        # Shift pressed and self not in currentSelection -> select
        if parameters.shiftPressed and self.name not in parameters.currentSelection:
            parameters.currentSelection.add(self.name)
            self.highlight()
        
        # Shift pressed and self in currentSelection -> unselect
        elif parameters.shiftPressed and self.name in parameters.currentSelection:
            parameters.currentSelection.remove(self.name)
            self.unhighlight()

        # Shift not pressed and self in currentSelection -> unselect
        elif parameters.shiftPressed == False and self.name in parameters.currentSelection:
            self.unhighlightAll()
            parameters.currentSelection = set([])

        # Shift not pressed and self not in currentSelection -> new select
        else:
            self.unhighlightAll()
            parameters.currentSelection = set([self.name])
            self.highlight()

        return


    def deletePages(self):
        """ Delete the selected pages """
        self.multiSelect()
        
        return


    def deleteSelf(self):
        """ Remove the frame from grid """
        for widgets in self.fr.winfo_children():
            widgets.destroy()
        self.fr.destroy()

        return
        