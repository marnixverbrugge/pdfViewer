pdfNumber = 1
frameNumber = 0
gridFrames = {}
frameHighlighted = None
pdfNames = {}
row = 0
column = 0
numberOfColumns = 1
imagesSize = 'medium'
showPageDetails = False

dictImagesSizes = {'small' : (88, 68),
                   'medium': (150, 120),
                   'large' : (250, 200)}


# Functions
currentAction = None
currentSelection = set([])
shiftPressed = False
selectionDone = False
secondPageSelection = None