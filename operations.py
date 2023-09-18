"""
Module containing all system and button functions
"""

# General imports
from tkinter import *
from tkinter import filedialog
import os
import shutil
import pypdfium2 as pdfium
from pypdf import PdfMerger
import datetime
from PIL import ImageDraw
from PIL import ImageFont

# Custom imports
import parameters
import rootWindow as rW


###
## System functions
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


def getOpenFileName():
    """Get the path of the selected pdf file"""
    fileName = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title='select pdf file',
                                          filetype = (('PDF File', '.pdf'),
                                                      ('PDF File', '.PDF'),
                                                      ('ALL file', '.txt')))

    # Update status bar
    if fileName: rW.updateStatusBar('Open file...')

    return fileName


def getSaveAsFileName():
    """Get the path and name of the new saved pdf file"""
    fileName = filedialog.asksaveasfile(initialfile='New file.pdf',
                                        defaultextension='.pdf',                                                                                                                      title='select pdf file',
                                        filetype = (('PDF File', '.pdf'),
                                                    ('PDF File', '.PDF')))
    
    # Update status bar
    if fileName: 
        saveTime = datetime.datetime.now().strftime('%H:%M')
        saveName = fileName.name
        rW.updateStatusBar('Saved at %s  --  %s'%(saveTime, saveName))

    return fileName


def saveImage(pdf, pageNumber, pageName, labelAll=False):
    """Save pdf page as image"""
    page = pdf.get_page(pageNumber)
    pil_image = page.render().to_pil()

    # Add Text to an image
    if labelAll:
        I1 = ImageDraw.Draw(pil_image)
        font = ImageFont.truetype("arial.ttf", 150)
        I1.text((10, 10), "A", fill=(255, 0, 0), font=font)

    pil_image.save((pageName))
    
    return


def updateRowsAndColumns():
    """ Update parameters row and columns """
    frameWidth = rW.imageFrame.winfo_width()
    imageWidth = parameters.dictImagesSizes[parameters.imagesSize][1]
    numberOfColumns = frameWidth // imageWidth
    parameters.numberOfColumns = numberOfColumns
    
    parameters.column = 0 if parameters.column==numberOfColumns-1 else parameters.column+1
    parameters.row = parameters.row+1 if parameters.column==0 else parameters.row

    return


def resizeGrid(skipColumnCheck=False):
    """ Resize the existing grid after imageFrame width change"""
    frameWidth = rW.imageFrame.winfo_width()
    imageWidth = parameters.dictImagesSizes[parameters.imagesSize][1]
    numberOfColumns = frameWidth // imageWidth
    
    if not skipColumnCheck:
        if numberOfColumns == parameters.numberOfColumns or numberOfColumns==0: 
            return

    parameters.numberOfColumns = numberOfColumns
    
    slaves = rW.imageFrame.grid_slaves()
    slaves.reverse()
    for i, slave in enumerate(slaves):
        slave.grid_forget()
        row = i//numberOfColumns
        column = i%numberOfColumns
        slave.grid(row=row, column=column)
    
    return


###
## Button functions
###

def openPDF():
    """Main function to open a pdf and show the pages as images in individual frames"""
    # Interupt any active functions
    rW.keyRelease(27)
    
    # UGLY WAY TO IMPORT FRAME INSTANCE
    import frameInstance
    
    # Open import gui
    fileName = getOpenFileName()
    if not fileName: return

    # Get new pdf featers
    pdfName = 'PDF-%s'%parameters.pdfNumber
    pdf = pdfium.PdfDocument(fileName)
    numberOfPages = len(pdf)

    # Update general parameters
    parameters.pdfNumber += 1
    parameters.pdfNames[pdfName] = fileName

    # Create individual pages
    for pageNumber in range(numberOfPages):
        # Save page as image
        pageName = 'imageFolder\%s_page-%s.png' %(pdfName, str(pageNumber+1))
        saveImage(pdf, pageNumber, pageName)
        # Create frame to visualize page image
        fr = frameInstance.ImageFrame()
        fr.createLabel(pageName)
        parameters.gridFrames[fr.name] = fr
        updateRowsAndColumns()
    
    resizeGrid(True)
    rW.updateStatusBar('Imported -- %s'%fileName.split('/')[-1])

    return


def openPDFasOne():
    """Main function to open a pdf and show the first pages as image"""
    # Interupt any active functions
    rW.keyRelease(27)
    
    # UGLY WAY TO IMPORT FRAME INSTANCE
    import frameInstance
    
    # Open import gui
    fileName = getOpenFileName()
    if not fileName: return

    # Get new pdf featers
    pdfName = 'PDF-%s'%parameters.pdfNumber
    pdf = pdfium.PdfDocument(fileName)
    numberOfPages = len(pdf)

    # Update general parameters
    parameters.pdfNumber += 1
    parameters.pdfNames[pdfName] = fileName

    # Create page
    pageName = 'imageFolder\%s_All.png' %(pdfName)
    saveImage(pdf, 0, pageName, True)

    # Create frame to visualize page image
    fr = frameInstance.ImageFrame(labelAll=True)
    fr.createLabel(pageName)
    parameters.gridFrames[fr.name] = fr
    updateRowsAndColumns()
    
    # Update grid and statusbar
    resizeGrid(True)
    rW.updateStatusBar('Imported as one -- %s'%fileName.split('/')[-1])

    return

    
# Save pdf 
def saveAs():
    """Function to save the new created pdf"""
    newFileName = getSaveAsFileName()
    sortedFrameNumbers = sorted(parameters.gridFrames.keys())
    
    newPDF = PdfMerger()
    for frameNumber in sortedFrameNumbers:
        fr = parameters.gridFrames[frameNumber]

        splitName = fr.pageName[12:].split('_')
        referencePDFName = splitName[0]
        pdfName = parameters.pdfNames[referencePDFName]
        
        # Get pdf name and number
        if fr.labelAll:
            newPDF.append(pdfName)
        else:
            pageNumber = int(splitName[1][5:-4])
            newPDF.append(pdfName, pages=(pageNumber-1, pageNumber))

    newPDF.write(newFileName.name)
    newPDF.close()
    
    return

# Page size
def updatePageSize(currentSize='normal'):
    """Function to update the page size"""
    parameters.imagesSize = currentSize
    for fr in parameters.gridFrames.values():
        fr.updateFrameSize()
    resizeGrid()
    return


# Page details
def updatePageDetails(showPageDetails):
    """Function to update the page size"""
    parameters.showPageDetails = showPageDetails
    for fr in parameters.gridFrames.values():
        fr.updatePageDetails()
    return




###
## PAGE OPERATIONS
###

def insertPages():
    """ Function to change the page order"""
    currentPageOrder = [fr.pageName for fr in parameters.gridFrames.values()]
    currentSelection = sorted(list(parameters.currentSelection))
    updatedOrder = [i for i in range(len(parameters.gridFrames.keys())) if i not in currentSelection]

    # Get index second page
    insert = parameters.secondPageSelection
    if updatedOrder[0] > insert:
        indexNumber = 0
    elif updatedOrder[-1]<insert:
        indexNumber = len(updatedOrder)
    else:
        for i, n  in enumerate(updatedOrder):
            if n == insert:
                indexNumber = i
            elif i>0 and updatedOrder[i-1]<insert and n>insert:
                indexNumber = i
    
    # Update order
    for i in reversed(currentSelection):
        updatedOrder.insert(indexNumber,i)

    # Update all pages
    for i, n in enumerate(updatedOrder):
        parameters.gridFrames[i].updateLabel(currentPageOrder[n])
    
    return

def deletePages():
    """ Function to delete the selected pages """
    numberOfDeletes = len(parameters.currentSelection)
    currentPageOrder = [fr.pageName for fr in parameters.gridFrames.values()]
    currentSelection = sorted(list(parameters.currentSelection))
    updatedOrder = [i for i in range(len(parameters.gridFrames.keys())) if i not in currentSelection]

    # Unhighlight selected
    for fr in parameters.currentSelection:
        parameters.gridFrames[fr].unhighlight()
        parameters.currentSelection = set([])

    # Remove redunted frames
    newTotalFrames = len(parameters.gridFrames.keys())-numberOfDeletes
    deleteList = [i for i in parameters.gridFrames.keys() if i > newTotalFrames-1]
    parameters.frameNumber = newTotalFrames
    for i in deleteList:
        parameters.gridFrames[i].deleteSelf()
        del parameters.gridFrames[i]

    # Update all pages
    for i, n in enumerate(updatedOrder):
        parameters.gridFrames[i].updateLabel(currentPageOrder[n])

    resizeGrid(True)
    return