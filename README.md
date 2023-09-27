# PDF Merger
Software to merge pdf's and update the page order.

A description of the available functions is given in the user manual.


#### Image size
The program is designed for A4 sized documents. It's possible to import 
other types but the page visualization will scale to A4.


#### manualUpdates
The default tkPDFViewer.py needs to be replaced with the py-file from
this folder.


#### imageFolder
All pages of an imported pdf are being stored as images in the imageFolder.
This folder is created by the script. For 'open pdf as one' holds that
only the first page is converted to png. A red 'A' is added to the image 
left top corner. Do not update or delete this folder while running the 
program.
