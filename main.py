"""
Main script to start the program

Create a tkinter window to show the pages of a pdf document

The pages are stored as .png in the imageFolder (re)created by the script

Comment: incorrect startxref pointer(1) --> possible to solve?
Comment: slow with large pdf files
"""

# Local imports
import rootWindow as rW

# Run main
rW.root.mainloop()