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
root.geometry('630x700+400+100')
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
        return

    v1 = pdf.ShowPdf()
    v2 = v1.pdf_view(root, pdf_location=open(fileName, 'r'), width=77, height=100)
    v2.pack(pady=(0,0))

Button(root, text='open', command=openFile, width=60).pack()

# Run
root.mainloop()
