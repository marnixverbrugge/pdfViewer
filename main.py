"""
Main file

Create a tkinter window to show the pages of a pdf document

The pages are stored are .png in the imageFolder (re)created by the script

Comment: incorrect startxref pointer(1) --> possible to solve?

"""

from tkinter import *
from tkinter import filedialog
import os
import shutil
from PIL import ImageTk, Image
import pypdfium2 as pdfium
from pypdf import PdfMerger

###
## CLASSES
###

class ImageFrame:
    """ Creates a frame to include tkinter label """
    def __init__(self):
        """Initial function of the ImageFrame isntance"""
        # General assignment
        self.row = grid.row
        self.column = grid.column
        self.name = parameters.frameNumber
        self.pageName = None
        self.selectHighlight = False
        self.createFrame((88, 68))

        # Update general parameters
        parameters.frameNumber += 1
    

    def createFrame(self, size):
        """ Create tkinter frame """
        self.fr = Frame(root)
        self.fr.configure(height=size[0],width=size[1])
        self.fr.grid_propagate(0)
        self.fr.grid(row=grid.row, column=grid.column, pady=20)
        
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
        self.fr.configure(background='#f0f0f0')
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

        

        


class ImportPDF:
    """main object"""

    def __init__(self, fileName):
        self.fileName = fileName
        self.name = self.getName()
        self.pdf = pdfium.PdfDocument(fileName)
        self.numberOfPages = len(self.pdf)
        
        # Update general parameters
        parameters.pdfNumber += 1
        parameters.pdfNames[self.name] = fileName


        # Create individual pages
        for pageNumber in range(self.numberOfPages):
            pageName = f"imageFolder\{self.name}_page-{pageNumber+1}.png"
            self.saveImage(pageNumber, pageName)
            fr = ImageFrame()
            fr.createLabel(pageName)
            parameters.gridFrames[fr.name] = fr
            grid.updateRowsAndColumns()

    def getName(self):
        return 'PDF-%s'%parameters.pdfNumber


    def saveImage(self, pageNumber, pageName):
        page = self.pdf.get_page(pageNumber)
        pil_image = page.render().to_pil()
        pil_image.save((pageName))
        
        return


class Grid:
    """Gird object for frame orientation"""
    
    def __init__(self):
        self.row = 2
        self.column = 0

    def updateRowsAndColumns(self):
        # Update row and columns
        self.column = 0 if self.column==2 else self.column+1
        self.row = self.row+1 if self.column==0 else self.row

        return

class Parameters:
    def __init__(self):
        self.pdfNumber = 1
        self.frameNumber = 0
        self.gridFrames = {}
        self.frameHighlighted = None
        self.pdfNames = {}


###
## FUNCTIONS
###

def createImageFolder():
    """Recreate the image folder"""
    path = os.getcwd()
    folderPath = '%s\imageFolder'%path

    isExist = os.path.exists(folderPath)
    if isExist:
        shutil.rmtree(folderPath)

    # Create folder
    os.makedirs(folderPath)

    return


def getFileName():
    """Get the path of the selected pdf file"""

    fileName = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title='select pdf file',
                                          filetype = (('PDF File', '.pdf'),
                                                      ('PDF File', '.PDF'),
                                                      ('ALL file', '.txt')))

    return fileName

def getNewFileName():
    fileName = filedialog.asksaveasfile(initialfile='New file.pdf',
                                        defaultextension='.pdf',                                                                                                                      title='select pdf file',
                                        filetype = (('PDF File', '.pdf'),
                                                    ('PDF File', '.PDF')))
    return fileName


###
## MAIN
###

# Create main window
root = Tk()
root.geometry('630x700+400+100')
root.title('PDF page viewer')


# Create open button
def openFunction():
    """Function to open a selected pdf file"""
    # Get file name
    fileName = getFileName()
    if not fileName: return

    # Import pdf pages into the image folder and show to user
    curPDF = ImportPDF(fileName)
    
    return
    
# Save pdf button
def savePDF():
    """Function to save the new created pdf"""
    newFileName = getNewFileName()
    sortedFrameNumbers = sorted(parameters.gridFrames.keys())
    
    newPDF = PdfMerger()
    for frameNumber in sortedFrameNumbers:
        fr = parameters.gridFrames[frameNumber]

        # Get pdf name and number
        splitName = fr.pageName[12:].split('_')
        referencePDFName = splitName[0]
        pageNumber = int(splitName[1][5:-4])
        pdfName = parameters.pdfNames[referencePDFName]
        newPDF.append(pdfName, pages=(pageNumber-1, pageNumber))

    newPDF.write(newFileName.name)
    newPDF.close()
    
    return

# Create open button
Button(root, text='open', command=openFunction, width=60).grid(row=0, column=0, columnspan=3)


# Create save button
Button(root, text='save', command=savePDF, width=60).grid(row=1, column=0, columnspan=3)


###
## RUN
###
createImageFolder()
grid = Grid()
parameters = Parameters()
root.mainloop()
