"""
Module containing the root window

The button operations are imported from operations.py

"""

# General imports
from tkinter import *
import ctypes

# Custom imports
import operations as ops


###
## ROOT
###

# Create main window
root = Tk()
root.state('zoomed')
root.minsize(height=400, width=600)
root.title('PDF page merger')


###
# Root Configuration
###
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=0)

root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=0)


###
# Menu bar
###
def pageSizeMenuClick(item, tabNumber):
    # Update GUI menu
    pageSizeSmall.set(0) 
    pageSizeMedium.set(0) 
    pageSizeLarge.set(0) 
    item.set(1)
    keepOpen('v', tabNumber)

    # Operate size function
    sizes = 'small', 'medium', 'large'
    ops.updatePageSize(sizes[tabNumber-1])

    return

def showPageDetailsClick():
    # Update GUI menu
    keepOpen('v')
    # Operate detail function
    details = showPageDetails.get()
    ops.updatePageDetails(details)
    return

def keepOpen(key='', subTab=None):
    keybd_event = ctypes.windll.user32.keybd_event
    alt_key = 0x12
    key_up = 0x0002

    ansi_key = ord(key.upper())
    #   press alt + key
    keybd_event(alt_key, 0, 0, 0)
    keybd_event(ansi_key, 0, 0, 0)

    #   release alt + key
    keybd_event(ansi_key, 0, key_up, 0)
    keybd_event(alt_key, 0, key_up, 0)

    if not subTab:
        keybd_event(40, 0, 0, 0)
    elif subTab:
        keybd_event(39, 0, 0, 0)
        for i in range(subTab-1): 
            keybd_event(40, 0, 0, 0)
            keybd_event(40, 0, key_up, 0)    
    return


menubar = Menu(root)

# File 
fileMenu = Menu(menubar, tearoff=0)
fileMenu.add_command(label='Open pdf', command=ops.openPDF)
fileMenu.add_command(label='Save as', command=ops.saveAs)
fileMenu.add_separator()
fileMenu.add_command(label='Quit', command=root.quit)
menubar.add_cascade(label='File', menu=fileMenu)

# View
viewMenu = Menu(menubar, tearoff=0)
pageSizeMenu = Menu(viewMenu, tearoff=0)
viewMenu.add_cascade(label='Page size', menu=pageSizeMenu)

pageSizeSmall = BooleanVar()
pageSizeMedium = BooleanVar()
pageSizeLarge = BooleanVar()
pageSizeMedium.set(1)
pageSizeMenu.add_checkbutton(label='Small', onvalue=1, offvalue=0, variable=pageSizeSmall, command=lambda: pageSizeMenuClick(pageSizeSmall, 1))
pageSizeMenu.add_checkbutton(label='Medium', onvalue=1, offvalue=0, variable=pageSizeMedium, command=lambda: pageSizeMenuClick(pageSizeMedium, 2))
pageSizeMenu.add_checkbutton(label='Large', onvalue=1, offvalue=0, variable=pageSizeLarge, command=lambda: pageSizeMenuClick(pageSizeLarge, 3))

showPageDetails = BooleanVar()
viewMenu.add_checkbutton(label='Show page details', onvalue=1, offvalue=0, variable=showPageDetails, command=showPageDetailsClick)
menubar.add_cascade(label='View', menu=viewMenu)


# Help
helpMenu = Menu(menubar, tearoff=0)
helpMenu.add_command(label='Manual', command=lambda: updateStatusBar('Help - Open manuel'))
menubar.add_cascade(label='Help', menu=helpMenu)

root.config(menu=menubar)


###
# Top functions
###
topFunctionsFrame = Frame(root, height=25)
topFunctionsFrame.grid(row=0, column=0, columnspan=2, sticky='nswe')

buttonOpen = Button(topFunctionsFrame, text='open', command=ops.openPDF)
buttonOpen.grid(row=0, column=0, padx=(3,0))
buttonSave = Button(topFunctionsFrame, text='save as', command=ops.saveAs)
buttonSave.grid(row=0, column=1, padx=(1,0))


###
# Center frame
###

def dragBarClick(event):
    event.widget.mouseX = event.x
    return


def dragBarRelease(event):
    event.widget.mouseX = 0
    return

def dragBarMotion(event):
    if event.widget.mouseX != 0:
        width = sideMenuFrame.winfo_width() + event.x - event.widget.mouseX
        centerFrame.grid_propagate(False)
        sideMenuFrame.configure(width=width)
    return


centerFrame = Frame(root)
centerFrame.grid(row=1, column=0, sticky='nswe')
centerFrame.grid_columnconfigure(0, weight=0)
centerFrame.grid_columnconfigure(1, weight=0)
centerFrame.grid_columnconfigure(2, weight=1)
centerFrame.grid_rowconfigure(0, weight=1)

# Side menu
sideMenuFrame = Frame(centerFrame, width=300, highlightbackground='black', highlightthickness=1)
sideMenuFrame.grid(row=0, column=0, sticky='nswe')

# Drag bar
dragBarFrame = Frame(centerFrame, bg='grey', width=7)
dragBarFrame.mouseX = 0
dragBarFrame.grid(row=0, column=1, sticky='nsw')

dragBarFrame.bind("<Motion>", dragBarMotion)
dragBarFrame.bind("<Button-1>", dragBarClick)
dragBarFrame.bind("<ButtonRelease-1>", dragBarRelease)

# Image frame
imageFrame = Frame(centerFrame, bg='white', highlightbackground='black', highlightthickness=1)
imageFrame.grid(row=0, column=2, sticky='nswe')


###
# Left functions
###
leftFunctionsFrame = Frame(root, width=25)
leftFunctionsFrame.grid(row=1, column=1, sticky='nswe')
leftFunctionsFrame.grid_columnconfigure(0, weight=0)


buttonFunction1 = Button(leftFunctionsFrame, text='1', width=2, command=lambda: updateStatusBar('Function 1 Button'))
buttonFunction1.grid(row=0, column=0, pady=(1,0), sticky='nswe')
buttonFunction2 = Button(leftFunctionsFrame, text='2', width=2, command=lambda: updateStatusBar('Function 2 Button'))
buttonFunction2.grid(row=1, column=0, pady=(1,0), sticky='nswe')


###
# Statusbar
###
statusBarFrame = Frame(root, height=25)
statusBarFrame.grid(row=2, column=0, columnspan=2, pady=1, padx=1, sticky='nswe')
statusBarFrame.grid_columnconfigure(0, weight=1)
statusLabel = Label(statusBarFrame, text='Welcome', bd=1, relief='sunken', anchor='w')
statusLabel.grid(row=0, column=0, sticky='nswe')

def updateStatusBar(text):
    statusLabel.configure(text=text)
    return



###
## RUN
###
root.mainloop()
