"""
Main file


Create a tkinter window to show the first page of a pdf document
"""

from tkinter import *
from tkinter import filedialog
from tkPDFViewer import tkPDFViewer as pdf
import os

# Create main window
root = Tk()
root.geometry('400x400')
root.title('PDF page viewer')


# Create open button
def openFile():
    """Function to open a selected pdf file"""

    fileName = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title='select pdf file',
                                          filetype = (('PDF File', '.pdf'),
                                                      ('PDF File', '.PDF'),
                                                      ('ALL file', '.txt')))

    if fileName:
        print(fileName)
    else:
        print('No file selected')

Button(root, text='open', command=openFile, width=60).pack()

# Run
root.mainloop()
