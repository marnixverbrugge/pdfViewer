# PDF Merger
Software to merge pdf's and update the page order by page visualization.

#### Image size
The programm is designed for A4 pages. It's possible to import other
types of sizes but the page visualization will always scale to A4.


#### manualUpdates
The current tkPDFViewer.py needs to be replaced with the py-file from
this folder.

#### imageFolder
All pages of an imported pdf are being stored as images in the imageFolder.
This folder is created by the script. For 'open pdf as one' holds that
only the first page is converted to png. An additional red 'A' is added to 
the image left top corner. Do not update or delete this folder while
running the programm.
