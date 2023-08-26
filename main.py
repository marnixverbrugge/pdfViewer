"""
Main file

Create a tkinter window to show the pages of a pdf document

The pages are stored are .png in the imageFolder (re)created by the script
Multiple use is currently unavailable because the imageFolder and the tkinter
frames are not updated properly.
"""

from tkinter import *
from tkinter import filedialog
import os
import shutil
from PIL import ImageTk, Image
import pypdfium2 as pdfium

###
## FUNCTIONS
###

def createImageFolder():
    """Recreate the image folder"""
    print('image')
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

    if fileName:
        print(fileName)
    else:
        print('No file selected')
    
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
    fileName = getFileName()

    # Open pdf, save as images and show in frame
    row = 1
    column = 0

    pdfNew = pdfium.PdfDocument(fileName)
    n_pages = len(pdfNew)

    for page_number in range(n_pages):
        # Save page a png
        pageName = f"imageFolder\image_{page_number+1}.png"
        page = pdfNew.get_page(page_number)
        pil_image = page.render().to_pil()
        pil_image.save((pageName))
        
        # Create tkinter frame
        fr = Frame(root)
        fr.configure(height=80,width=60)
        fr.grid_propagate(0)
        fr.grid(row=row, column=column, pady=20)
        
        # Update frame with page image
        original = Image.open('%s\%s'%(os.getcwd(),pageName))
        resized = original.resize((60, 80),Image.ANTIALIAS)
        img = ImageTk.PhotoImage(resized)
        label = Label(fr, image = img)
        label.image=img
        label.grid()

        # Update row and columns
        column = 0 if column==2 else column+1
        row = row+1 if column==0 else row
    

# Create open button
Button(root, text='open', command=openFunction, width=60).grid(row=0, column=0, columnspan=3)


###
## RUN
###
createImageFolder()
root.mainloop()
