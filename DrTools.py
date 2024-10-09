#Imports
#===================================================================================================#
from tkinter import * 
from tkinter import ttk
from tkinter.filedialog import asksaveasfile
from tkinter import messagebox
import pandas as pd
from PIL import ImageTk,Image
#===================================================================================================#


#Psuedo Global: Variables / CONSTANTS / Secrets
#===================================================================================================#
"""
This variable acts as a psuedo global variable as it accessible from anywhere in main.py when DrTools
is importing which avoids global addressing in the main.py file
"""
data = pd.DataFrame()
#the image of the X that is used to close the toggle menu that comes out from the right side of the root window - constant
CLOSE_IMG = Image.open("close.png")
#primary colour of GUI
prim_clr = "#6B6B6B"
#secondary colour of GUI
sec_clr = "#40C6FF"

#===================================================================================================#

#DrExporter
#===================================================================================================#
"""
Curated module used to make exporting simple as cake... or atleast easier
"""

#Main class containing procedures used to export files
class DrExporter():
    def __init__(self):
        #private variables created
        self.__file = 0
        
    #save as csv subroutine
    def sv_csv(self,opt_index,opt_header,compressiontype):
        #asking the user to create a file in desired location
        self.__file = asksaveasfile(filetypes = [('CSV File', '*.csv')],defaultextension =[('CSV File', '*.csv')])           
        #checking if the file was created
        if self.__file != None:
            #getting the filepath of the created file
            self.__filepath = self.__file.name
            #handling exceptions that could arise due to user permission
            try:
                #writing the data that is being exported to this file (uses the same filetype)
                data.to_csv(self.__filepath,index=opt_index,header=opt_header)
                messagebox.showinfo('Successful Export', 'You have successfully exported the file')
            except:
                messagebox.showerror('Export Error', 'Error: An error occoured exporting this file, make sure you have suffiecient permission to save at the chosen directory')
        else:
            messagebox.showinfo('Cancelled Export', 'You have cancelled the export')


    #save as excel subroutine (same format as above csv save) refer to comments above in case of confusion
    def sv_excel(self,opt_index,opt_header,compressiontype):
        self.__file = asksaveasfile(filetypes = [('Excel File', '*.xlsx')], defaultextension = [('Excel File', '*.xlsx')])           
        if self.__file != None:
            self.__filepath = self.__file.name
            try:
                data.to_excel(self.__filepath,index=opt_index,header=opt_header)
                messagebox.showinfo('Successful Export', 'You have successfully exported the file')
            except:
                messagebox.showerror('Export Error', 'Error: An error occoured exporting this file, make sure you have suffiecient permission to save at the chosen directory')
        else:
            messagebox.showinfo('Cancelled Export', 'You have cancelled the export')

    #accessor for the private variable 'file' could be used to get filepath of saved data etc
    def get_save_data(self):
        return self.__file
#===================================================================================================#


#DrError
#===================================================================================================#
"""
Used for debugging purposes. implementing a stack as an array in python to hold errors in order of occourance during runtime
"""

class DrError():
    def __init__(self):
        #initialising the error stack
        self.__err_stack = []

    #public method to add an error to the stack.
    def add_error(self,error):
        self.__err_stack.append(error)

    #public method to create the error console from which the developer can view the error stack using a scrollable list box
    def error_console(self):
        #creating the root window alongside sizing it and locking the geometry so it cannot be changed
        self.__root = Tk()
        self.__root.title("Error Console")
        self.__root.geometry("450x500")
        self.__root.resizable(0,0)
        #creating the scrollbars used to scroll the listbox
        self.__scroll_y_axis = Scrollbar(self.__root,orient="vertical")
        self.__scroll_x_axis = Scrollbar(self.__root, orient="horizontal")
        #creating the listbox to contain all errors
        self.__error_list = Listbox(self.__root, relief=GROOVE,width = 50, height=50,yscrollcommand=self.__scroll_y_axis,xscrollcommand=self.__scroll_x_axis)
        
        #appending all errors from the stack to the listbox using f string formatting
        for i in range(len(self.__err_stack)):
            self.__error_list.insert((i+1),f"{i}:| {self.__err_stack[i]}")
        #configurating the listbox command so that they are binded to scrolling the listbox alongside packing them.
        self.__scroll_y_axis.config(command=self.__error_list.yview)
        self.__scroll_y_axis.pack(side="right",fill="y")

        self.__scroll_x_axis.config(command=self.__error_list.xview)
        self.__scroll_x_axis.pack(side="bottom",fill="x")
        #finally packing the listbox its self.
        self.__error_list.pack(pady=10,padx=10)

#===================================================================================================#


#checks if the module is being run standalone (directly) or being imported (if it is being imported it will not do what is in the selection statement)
if __name__ == "__main__":
    print("this script is being run alone!")

