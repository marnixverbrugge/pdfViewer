from tkinter import *
from tkinter import filedialog


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
menubar = Menu(root)

# File 
fileMenu = Menu(menubar, tearoff=0)
fileMenu.add_command(label='Open pdf', command=lambda: updateStatusBar('File - Open PDF'))
fileMenu.add_command(label='Save as', command=lambda: updateStatusBar('File - Save PDF'))
fileMenu.add_separator()
fileMenu.add_command(label='Quit', command=root.quit)
menubar.add_cascade(label='File', menu=fileMenu)

# View
viewMenu = Menu(menubar, tearoff=0)
viewMenu.add_command(label='Page size', command=lambda: updateStatusBar('View - Page size'))
viewMenu.add_command(label='Show page details', command=lambda: updateStatusBar('View - Show page details'))
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

buttonOpen = Button(topFunctionsFrame, text='open', command=lambda: updateStatusBar('Open Button'))
buttonOpen.grid(row=0, column=0, padx=(3,0))
buttonSave = Button(topFunctionsFrame, text='save as', command=lambda: updateStatusBar('Save as Button'))
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
statusLabel = Label(statusBarFrame, text='test status', bd=1, relief='sunken', anchor='w')
statusLabel.grid(row=0, column=0, sticky='nswe')

def updateStatusBar(text):
    statusLabel.configure(text=text)
    return



###
## RUN
###
root.mainloop()
