"""
Main file

Create a tkinter window to show the pages of a pdf document

The pages are stored are .png in the imageFolder (re)created by the script

"""

from tkinter import *
from tkinter import filedialog
import os
import shutil
from PIL import ImageTk, Image
import pypdfium2 as pdfium

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
        self.name = 'Frame-%s'%str(parameters.frameNumber)
        self.pageName = None
        self.createFrame((80,60))

        # Update general parameters
        parameters.frameNumber += 1
    

    def createFrame(self, size):
        """ Create tkinter frame """
        self.fr = Frame(root)
        self.fr.configure(height=size[0],width=size[1])
        self.fr.grid_propagate(0)
        self.fr.grid(row=grid.row, column=grid.column, pady=20)
        
        return 


    def assignLabel(self, pageName):
        """ Assign the correct image label to frame """
        self.pageName = pageName
        # Update frame with page image
        original = Image.open('%s\%s'%(os.getcwd(),pageName))
        resized = original.resize((60, 80),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(resized)
        label = Label(self.fr, image = img)
        label.image=img
        
        label.bind("<Button-1>", self.printName)
        label.grid()

        return
    
    
    def printName(self, event):
        print(self.pageName[12:-4])
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


        # Create individual pages
        for pageNumber in range(self.numberOfPages):
            pageName = f"imageFolder\{self.name}_page-{pageNumber+1}.png"
            self.saveImage(pageNumber, pageName)
            fr = ImageFrame()
            fr.assignLabel(pageName)
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
        self.row = 1
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
    

# Create open button
Button(root, text='open', command=openFunction, width=60).grid(row=0, column=0, columnspan=3)


###
## RUN
###
createImageFolder()
grid = Grid()
parameters = Parameters()
root.mainloop()
