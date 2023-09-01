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
    if fileName: rW.updateStatusBar('Imported -- %s'%fileName.split('/')[-1])

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


def saveImage(pdf, pageNumber, pageName):
    """Save pdf page as image"""
    page = pdf.get_page(pageNumber)
    pil_image = page.render().to_pil()
    pil_image.save((pageName))
    
    return


def updateRowsAndColumns():
    """ Update parameters row and columns """
    parameters.column = 0 if parameters.column==2 else parameters.column+1
    parameters.row = parameters.row+1 if parameters.column==0 else parameters.row

    return




###
## Button functions
###

def openPDF():
    """Main function to open a pdf and show the pages as images in individual frames"""
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
    
    return

    
# Save pdf 
def saveAs():
    """Function to save the new created pdf"""
    newFileName = getSaveAsFileName()
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

# Page size
def updatePageSize(currentSize='normal'):
    """Function to update the page size"""
    parameters.imagesSize = currentSize
    for fr in parameters.gridFrames.values():
        fr.updateFrameSize()
    return


# Page details
def updatePageDetails(showPageDetails):
    """Function to update the page size"""
    parameters.showPageDetails = showPageDetails
    for fr in parameters.gridFrames.values():
        fr.updatePageDetails()
    return
