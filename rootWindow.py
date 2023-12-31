"""
Module containing the root window

The button operations are imported from operations.py

"""

# General imports
from tkinter import *
import ctypes
import os

# Custom imports
import operations as ops
import parameters


####################################################################
##                             CLASSES                            ##
####################################################################

class VerticalScrolledFrame(Frame):
    """ Class to create a canvas including a frame and scrollbar """
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, highlightbackground='black', highlightthickness=1, background='white',
                           yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = AutoGrid(canvas, bg='white')
        interior_id = canvas.create_window(0, 0, window=interior, anchor=NW)


        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            interior.regrid(None)
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
            interior.regrid(None)    
        canvas.bind('<Configure>', _configure_canvas)

        # Bind mouse wheel
        self.canvas = canvas
        self.canvas.bind_all('<MouseWheel>', self.onMouseWheel)

    def onMouseWheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")


class AutoGrid(Frame):
    """ Class to auto scale the image frames """
    def __init__(self, master=None, **kwargs):
        Frame.__init__(self, master, **kwargs)
        self.columns = None
        self.bind('<Configure>', self.regrid)

    def regrid(self, event):
        ops.resizeGrid()
        return


####################################################################
##                            FUNCTIONS                           ##
####################################################################

###
## Buttons
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

def setNoneFunction():
    keyRelease(27)
    return

def clearAllFunction():
    keyRelease(27)

    # Delete frames
    allFrameNames = [i for i in parameters.gridFrames.keys()]
    for i in allFrameNames:
        parameters.gridFrames[i].deleteSelf()
        del parameters.gridFrames[i]
    
    # Reset parameters
    parameters.pdfNumber = 1
    parameters.frameNumber = 0
    parameters.gridFrames = {}
    parameters.pdfNames = {}
    parameters.row = 0
    parameters.column = 0
    parameters.numberOfColumns = 1

    ops.createImageFolder()
    clearSideMenu()
    updateStatusBar("Cleared all")
    return


###
## Menubar
###

def pageSizeMenuClick(item, tabNumber):
    """ Function to switch page size via menubar """
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
    """ Function to visualize the page details label """
    # Update GUI menu
    keepOpen('v')
    # Operate detail function
    details = showPageDetails.get()
    ops.updatePageDetails(details)
    return

def keepOpen(key='', subTab=None):
    """ Function to keep open the current menubar tab """
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

def openManual():
    os.system('start usermanual.docx')
    return

###
## Left side bar
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

def clearSideMenu():
    for widgets in sideMenuFrame.winfo_children():
            widgets.destroy()
    titleSideMenu = Label(sideMenuFrame, text='Current Files', font='Helvetica 12 bold')
    titleSideMenu.grid(row=0, column=0, pady=(50,0), columnspan=2, sticky='w')
    return

###
# Statusbar
###

def updateStatusBar(text):
    statusLabel.configure(text=text)
    statusLabel.update()
    return


###
## Keys
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
        ops.unhighlightAll()
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
                updateStatusBar('Pages are inserted - Select new pages to insert - Press enter to continue or esc to stop')
                ops.unhighlightAll()
                parameters.currentSelection = set([])
                parameters.secondPageSelection = None
                parameters.selectionDone = False

        if parameters.currentAction == 'delete':
            ops.deletePages()
            updateStatusBar('Pages are deleted - Select new pages to delete - Press enter to continue or esc to stop')
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


    return

def enterMouse(event):
    """ Link mouse button to enter key """
    keyRelease(13)
    return



####################################################################
##                              ROOT                              ##
####################################################################

###
# Create main window
###
root = Tk()
root.state('zoomed')
root.minsize(height=400, width=600)
root.title('PDF page merger')

# Binding to root
root.bind("<KeyPress>", lambda e: keyPressed(e.keycode))
root.bind("<KeyRelease>", lambda e: keyRelease(e.keycode))
root.bind("<Button-2>", enterMouse)


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
menubar = Menu(root)

# File 
fileMenu = Menu(menubar, tearoff=0)
fileMenu.add_command(label='Open pdf', command=ops.openPDF)
fileMenu.add_command(label='Open pdf as one', command= lambda: ops.openPDF(asOne=True))
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

# Functions
functionMenu = Menu(menubar, tearoff=0)
functionMenu.add_command(label='Swap pages', command=swapFunction)
functionMenu.add_command(label='Insert selection', command=insertFunction)
functionMenu.add_command(label='Delete pages', command=deleteFunction)
functionMenu.add_command(label='None', command=setNoneFunction)
functionMenu.add_command(label='Clear all', command=clearAllFunction)
menubar.add_cascade(label='Functions', menu=functionMenu)

# Help
helpMenu = Menu(menubar, tearoff=0)
helpMenu.add_command(label='Manual', command=openManual)
menubar.add_cascade(label='Help', menu=helpMenu)

root.config(menu=menubar)


###
# Top functions
###
topFunctionsFrame = Frame(root, height=25)
topFunctionsFrame.grid(row=0, column=0, columnspan=2, sticky='nswe')

buttonOpen = Button(topFunctionsFrame, text='open', command=ops.openPDF)
buttonOpen.grid(row=0, column=0, padx=(3,0))
buttonOpen = Button(topFunctionsFrame, text='open as one', command= lambda: ops.openPDF(asOne=True))
buttonOpen.grid(row=0, column=1, padx=(1,0))
buttonSave = Button(topFunctionsFrame, text='save as', command=ops.saveAs)
buttonSave.grid(row=0, column=2, padx=(1,0))


###
# Center frame
###
centerFrame = Frame(root)
centerFrame.grid(row=1, column=0, sticky='nswe')
centerFrame.grid_columnconfigure(0, weight=0)
centerFrame.grid_columnconfigure(1, weight=0)
centerFrame.grid_columnconfigure(2, weight=1)
centerFrame.grid_rowconfigure(0, weight=1)

# Side menu
sideMenuFrame = Frame(centerFrame, width=300, highlightbackground='black', highlightthickness=1)
sideMenuFrame.grid(row=0, column=0, sticky='nswe')
sideMenuFrame.grid_propagate(0)
titleSideMenu = Label(sideMenuFrame, text='Current Files', font='Helvetica 12 bold')
titleSideMenu.grid(row=0, column=0, pady=(50,0), columnspan=2, sticky='w')

# Drag bar
dragBarFrame = Frame(centerFrame, bg='grey', width=7)
dragBarFrame.mouseX = 0
dragBarFrame.grid(row=0, column=1, sticky='nsw')

dragBarFrame.bind("<Motion>", dragBarMotion)
dragBarFrame.bind("<Button-1>", dragBarClick)
dragBarFrame.bind("<ButtonRelease-1>", dragBarRelease)

# Image frame
imageCanvas = VerticalScrolledFrame(centerFrame)
imageCanvas.grid(row=0, column=2, sticky='nswe')
imageFrame = imageCanvas.interior


###
# Right functions
###
leftFunctionsFrame = Frame(root)
leftFunctionsFrame.grid(row=1, column=1, sticky='nswe')
leftFunctionsFrame.grid_columnconfigure(0, weight=0)
leftFunctionsFrame.grid_rowconfigure(5, weight=1)
leftFunctionsFrame.grid_rowconfigure(6, weight=0)


title = Label(leftFunctionsFrame, text='Functions', font='Helvetica 9 bold')
title.grid(row=0, column=0, pady=1, sticky='nswe')
buttonFunction1 = Button(leftFunctionsFrame, text='Swap', width=10, command=swapFunction)
buttonFunction1.grid(row=1, column=0, pady=(1,0), sticky='nswe')
buttonFunction2 = Button(leftFunctionsFrame, text='Insert', command=insertFunction)
buttonFunction2.grid(row=2, column=0, pady=(1,0), sticky='nswe')
buttonFunction3 = Button(leftFunctionsFrame, text='Delete', command=deleteFunction)
buttonFunction3.grid(row=3, column=0, pady=(1,0), sticky='nswe')
buttonFunction4 = Button(leftFunctionsFrame, text='None', command=setNoneFunction)
buttonFunction4.grid(row=4, column=0, pady=(1,0), sticky='nswe')
space= Label(leftFunctionsFrame, text='').grid(row=5, column=0, sticky='nswe')
buttonFunction5 = Button(leftFunctionsFrame, text='Clear All', command=clearAllFunction)
buttonFunction5.grid(row=6, column=0, pady=(1,0), sticky='nswe')


###
# Statusbar
###
statusBarFrame = Frame(root, height=25)
statusBarFrame.grid(row=2, column=0, columnspan=2, pady=1, padx=1, sticky='nswe')
statusBarFrame.grid_columnconfigure(0, weight=1)
statusLabel = Label(statusBarFrame, text='Welcome', bd=1, relief='sunken', anchor='w')
statusLabel.grid(row=0, column=0, sticky='nswe')



####################################################################
##                               RUN                              ##
####################################################################
ops.createImageFolder()
root.mainloop()