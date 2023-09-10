"""
Module containing the root window

The button operations are imported from operations.py

"""

# General imports
from tkinter import *
import ctypes

# Custom imports
import operations as ops
import parameters

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

class AutoGrid(Frame):
    """ Class to auto scale the image frames """
    def __init__(self, master=None, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.columns = None
        self.bind('<Configure>', self.regrid)

    def regrid(self, event):
        ops.resizeGrid()



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
imageFrame = AutoGrid(centerFrame, bg='white', highlightbackground='black', highlightthickness=1)
imageFrame.grid(row=0, column=2, sticky='nswe')


###
# Right functions
###

def swapFunction():
    highlightButton(buttonFunction1)
    parameters.currentAction = 'swap'
    updateStatusBar('Select page to swap')
    return

def deleteFunction():
    highlightButton(buttonFunction3)
    parameters.currentAction = 'delete'
    updateStatusBar('Select pages - press Enter to delete')
    return

def insertFunction():
    highlightButton(buttonFunction2)
    parameters.currentAction = 'insert'
    updateStatusBar('Select pages to insert - press Enter to continue')
    return

def highlightButton(button):
    unhighlightButtonAll()
    button.configure(relief='sunken')
    return

def unhighlightButtonAll():
    buttonFunction1.configure(relief='raised')
    buttonFunction2.configure(relief='raised')
    buttonFunction3.configure(relief='raised')
    return

leftFunctionsFrame = Frame(root, width=25)
leftFunctionsFrame.grid(row=1, column=1, sticky='nswe')
leftFunctionsFrame.grid_columnconfigure(0, weight=0)

buttonFunction1 = Button(leftFunctionsFrame, text='1', width=2, command=swapFunction)
buttonFunction1.grid(row=0, column=0, pady=(1,0), sticky='nswe')
buttonFunction2 = Button(leftFunctionsFrame, text='2', width=2, command=insertFunction)
buttonFunction2.grid(row=1, column=0, pady=(1,0), sticky='nswe')
buttonFunction3 = Button(leftFunctionsFrame, text='D', width=2, command=deleteFunction)
buttonFunction3.grid(row=2, column=0, pady=(1,0), sticky='nswe')


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
    statusLabel.update()
    return


###
## KEYS
###

def keyPressed(keyCode):
    """Function to update the parameters based on key input"""
    # Left shift
    if keyCode == 16: 
        parameters.shiftPressed = True
    return

def keyRelease(keyCode):
    """Function to update the parameters based on key input"""
    # print(keyCode)
    # Left shift
    if keyCode == 16: parameters.shiftPressed = False
    
    # ESC - Unhighlight current selection
    elif keyCode == 27:
        unhighlightAll()
        unhighlightButtonAll()
        parameters.currentAction = None
        parameters.currentSelection = set([])
        parameters.selectionDone = False
        parameters.secondPageSelection == None
        updateStatusBar('No function activated')
        

    # Enter - Confirm selection
    elif keyCode == 13:
        if parameters.currentAction == 'insert':
            parameters.selectionDone = True
            if parameters.currentAction == 'insert' and parameters.secondPageSelection==None: 
                updateStatusBar('Select page to insert red pages in front')
            elif parameters.currentAction == 'insert'and parameters.secondPageSelection!=None:
                ops.insertPages()
                updateStatusBar('Pages are inserted')
                unhighlightAll()
                parameters.currentSelection = set([])
                parameters.secondPageSelection = None
                parameters.selectionDone = False

        if parameters.currentAction == 'delete':
            ops.deletePages()
            updateStatusBar('Pages are deleted')
            parameters.currentSelection = set([])
            parameters.selectionDone = False

    # Shortcut to functions
    elif keyCode == 49: # 1 key
        swapFunction()
    elif keyCode == 50: # 2 key
        insertFunction()
    elif keyCode == 51: # 3 key
        deleteFunction()
    elif keyCode == 79: # o key
        ops.openPDF()
    elif keyCode == 83: # s key
        ops.saveAs()


    # Print programm information
    elif keyCode == 73: # i key
        print('Gridframes: ', parameters.gridFrames.keys())
        print('CurrentSelection: ', parameters.currentSelection)
        print('Num columns: ', parameters.numberOfColumns)
        print('row, column: ', parameters.row, parameters.column)
    return


def unhighlightAll():
    """ Unhighlight all selected frames """
    for fr in parameters.currentSelection:
        parameters.gridFrames[fr].unhighlight()
    
    if parameters.secondPageSelection != None:
        parameters.gridFrames[parameters.secondPageSelection].unhighlight()
    return

def enterMouse(event):
    """ Link mouse button as enter key """
    keyRelease(13)
    return

root.bind("<KeyPress>", lambda e: keyPressed(e.keycode))
root.bind("<KeyRelease>", lambda e: keyRelease(e.keycode))
root.bind("<Button-2>", enterMouse)


###
## RUN
###
ops.createImageFolder()
root.mainloop()
