#====DataRoom====#

#=Libraries=#
#-----------------------------------------#
#Custom Libraries
import DrTools as DrT
#GUI libraries
import tkinter as tk
from tkinter import filedialog,messagebox,colorchooser,ttk
from tkinter.messagebox import askyesno
from PIL import ImageTk,Image
#graphing libraries
import matplotlib
matplotlib.use('TkAgg',force=True)
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="ticks")
#data manipulation libraries
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
#SQL libraries
from sqlalchemy import create_engine,exc
#warnings lib
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

#instantiating classes
#-----------------------------------------#
Dr_Exporter = DrT.DrExporter()
DrErr = DrT.DrError()

#=Subroutines=#
#-----------------------------------------#

#confirming user exit
def user_exit():
    #asks the user to confirm their exit by openening an option box
    if askyesno(title='Confrim Exit',message='Are you sure that you want to quit? All unsaved data will be lost!') == True:
        exit()

#importing data using a csv file
def import_data_csv():
    #sets up a filepath by getting the user to select a file using the file dialog menu
    filepath = filedialog.askopenfilename(initialdir="C:\\Users\\inaia\\Documents",
                                          title="Open Data",
                                          filetypes= (("all files","*.*"),("csv files","*.csv"),
                                                      ("text files",".txt")))
    #attempts to read the data and assign it in the form of a data frame to the variable "data"
    try:
        DrT.data = pd.read_csv(filepath)
        GUI._set_c_file(filepath)
    #simple error handling in case of importing errors
    except ValueError:
        messagebox.showerror('Importing Error', 'Error: File could not be opened, Please try again!')
    except FileNotFoundError:
        messagebox.showerror('Importing Error', 'Error: You have not selected a csv file, Please try again!')


def import_data_xlsx():
    filepath = filedialog.askopenfilename(initialdir="C:\\Users\\inaia\\Documents",
                                          title="Open Data",
                                          filetypes= (("all files","*.*"),("Excel files","*.xlsx"),
                                                      ("text files",".txt")))
    try:
        DrT.data = pd.read_excel(filepath)
        GUI._set_c_file(filepath)
    except ValueError:
        messagebox.showerror('Importing Error', 'Error: File could not be opened, Please try again!')
    except FileNotFoundError:
        messagebox.showerror('Importing Error', 'Error: You have not selected an excel file, Please try again!')


#-----------------------------------------#
#=MAIN=#

#setting up the root (the main menu, every other gui window will branch off the root)
root = tk.Tk()
root.geometry("1200x800")
root.config(bg=DrT.prim_clr)
root.resizable(0,0)
root.title('Data Room')

#creating the GUI class. This effectively holds the tkinter GUI code for every window and it's widgets.
#Further as the GUI class can only be called after the definition of the entire class, it is easier to define subroutines within the class.
class GUI_template:
    def __init__(self):
        #import data/current file frame and widgets
        self.__import_frame = tk.LabelFrame(root, width = 200,bg=DrT.prim_clr ,height = 10)
        self.__import_frame.place(x=0,y=0)

        self._import_button = tk.Button(self.__import_frame, text="Import Data",width=20,height = 2,activebackground=DrT.sec_clr,bg=DrT.sec_clr,command=import_data_csv)
        self._import_button.grid(row = 0, column = 0,pady=5, padx=10)
        self._c_file = tk.Label(self.__import_frame, text = f"Not Selected",width=100,bg=DrT.sec_clr)
        self._c_file.grid(row = 0, column = 1)
        #descriptive analytics frame and widgets
        self.__desc_frame = tk.LabelFrame(root, width = 500,bg=DrT.sec_clr,height = 300,relief="solid")
        self.__desc_frame.place(x=25,y=100)

        self.__desc_frame_title = tk.Label(self.__desc_frame, text="Descriptive Analytics",bg=DrT.sec_clr, font=("Arial",15))
        self.__desc_frame_title.grid(row = 0, column = 0,pady=5, padx=10)

        self.__view_df = tk.Button(self.__desc_frame, text="View DataFrame",width=70,height = 2,fg="#FFFFFF",relief="solid",activebackground=DrT.prim_clr,bg=DrT.prim_clr,command=lambda:(self.view_data_frame("View Data Frame")))
        self.__view_df.grid(row = 1, column = 0,pady=15, padx=10)

        self.__df_dimensions = tk.Button(self.__desc_frame, text="DataFrame Dimensions",width=70,height = 2,fg="#FFFFFF",relief="solid",activebackground=DrT.prim_clr,bg=DrT.prim_clr,command=lambda:(self.df_dimens("Data Frame Dimensions")))
        self.__df_dimensions.grid(row = 2, column = 0,pady=15, padx=10)

        self.__df_info = tk.Button(self.__desc_frame, text="DataFrame Information",width=70,height = 2,fg="#FFFFFF",relief="solid",activebackground=DrT.prim_clr,bg=DrT.prim_clr,command= lambda:(self.info_df("Data Frame Information")))
        self.__df_info.grid(row = 3, column = 0,pady=15, padx=10)

        self.__df_description = tk.Button(self.__desc_frame, text="DataFrame Description",width=70,height = 2,fg="#FFFFFF",relief="solid",activebackground=DrT.prim_clr,bg=DrT.prim_clr,command=lambda: (self.desc_df("Describe Data Frame")))
        self.__df_description.grid(row = 4, column = 0,pady=15, padx=10)
        #clean/sample data frame and widgets
        self.__clean_sample_frame = tk.LabelFrame(root, width = 500,bg=DrT.sec_clr,height = 300,relief="solid")
        self.__clean_sample_frame.place(x=25,y=450)

        self.__clean_sample_frame_title = tk.Label(self.__clean_sample_frame, text="Clean and Sample Data",bg=DrT.sec_clr, font=("Arial",15))
        self.__clean_sample_frame_title.grid(row = 0, column = 0,pady=5, padx=10)

        self.__report_null = tk.Button(self.__clean_sample_frame, text="Report Null Values",width=70,height = 2,fg="#FFFFFF",relief="solid",activebackground=DrT.prim_clr,bg=DrT.prim_clr,command=lambda:(self.rep_nulls("Reporting Null Values")))
        self.__report_null.grid(row = 1, column = 0,pady=15, padx=10)
       
        self.__patch_null = tk.Button(self.__clean_sample_frame, text="Patching Null Values",width=70,height = 2,fg="#FFFFFF",relief="solid",activebackground=DrT.prim_clr,bg=DrT.prim_clr,command=lambda:(self.patch_nulls("Patching Null Values")))
        self.__patch_null.grid(row = 2, column = 0,pady=15, padx=10)

        self.__rand_sample = tk.Button(self.__clean_sample_frame, text="Random Sampling of data",width=70,height = 2,fg="#FFFFFF",relief="solid",activebackground=DrT.prim_clr,bg=DrT.prim_clr,command=lambda:(self.random_sample_df("Randomly Sample Data")))
        self.__rand_sample.grid(row = 3, column = 0,pady=15, padx=10)


        #dataframe manipulation frame and widgets
        self.__manipulate_frame = tk.LabelFrame(root, width = 500,bg=DrT.sec_clr,height = 300,relief="solid")
        self.__manipulate_frame.place(x=600,y=100)

        self.__manipulate_frame_title = tk.Label(self.__manipulate_frame, text="DataFrame Manipulation",bg=DrT.sec_clr, font=("Arial",15))
        self.__manipulate_frame_title.grid(row = 0, column = 0,pady=5, padx=10)

        self.__del_column = tk.Button(self.__manipulate_frame, text="Delete Column",width=70,height = 2,fg="#FFFFFF",relief="solid",activebackground=DrT.prim_clr,bg=DrT.prim_clr,command=lambda:(self.colm_dropper("Delete Column")))
        self.__del_column.grid(row = 1, column = 0,pady=15, padx=10)

        self.__reshape_rows_button = tk.Button(self.__manipulate_frame, text="Reshape Number of Rows",width=70,height = 2,fg="#FFFFFF",relief="solid",activebackground=DrT.prim_clr,bg=DrT.prim_clr,command=lambda:(self.reshape_rows("Reshape Rows")))
        self.__reshape_rows_button.grid(row = 2, column = 0,pady=15, padx=10)

        self.__pca = tk.Button(self.__manipulate_frame, text="PCA",width=70,height = 2,fg="#FFFFFF",relief="solid",activebackground=DrT.prim_clr,bg=DrT.prim_clr,command=lambda:(self.DR_PCA("Principal Component Analysis")))
        self.__pca.grid(row = 3, column = 0,pady=15, padx=10)
       
        self.__calc_columns = tk.Button(self.__manipulate_frame, text="Calculate Between Columns",width=70,height = 2,fg="#FFFFFF",relief="solid",activebackground=DrT.prim_clr,bg=DrT.prim_clr,command=lambda:(self.calc_colms("Calculate Between Columns")))
        self.__calc_columns.grid(row = 4, column = 0,pady=15, padx=10)

        #visulatisations and algorithms frame and widgets
        self.__vis_algo_frame = tk.LabelFrame(root, width = 500,bg=DrT.sec_clr,height = 300,relief="solid")
        self.__vis_algo_frame.place(x=600,y=450)

        self.__vis_algo_frame_title = tk.Label(self.__vis_algo_frame, text="Visualisations and Algorithms",bg=DrT.sec_clr, font=("Arial",15))
        self.__vis_algo_frame_title.grid(row = 0, column = 0,pady=5, padx=10)

        self.__graph_vis = tk.Button(self.__vis_algo_frame, text="Graphical Visualisations",width=70,height = 2,fg="#FFFFFF",relief="solid",activebackground=DrT.prim_clr,bg=DrT.prim_clr,command=lambda:(self.graph_chooser("Select a graphical model")))
        self.__graph_vis.grid(row = 1, column = 0,pady=15, padx=10)
       
        self.__distribution_vis = tk.Button(self.__vis_algo_frame, text="Distribution Visualisation",width=70,height = 2,fg="#FFFFFF",relief="solid",activebackground=DrT.prim_clr,bg=DrT.prim_clr,command=lambda:(GUI.hist_plot("Histogram")))
        self.__distribution_vis.grid(row = 2, column = 0,pady=15, padx=10)

        self.__k_means = tk.Button(self.__vis_algo_frame, text="K-Means Clustering",width=70,height = 2,fg="#FFFFFF",relief="solid",activebackground=DrT.prim_clr,bg=DrT.prim_clr,command=lambda:(self.DR_KMeans("K-Means")))
        self.__k_means.grid(row = 3, column = 0,pady=15, padx=10)

        #Exit Button
        self.__exit_bttn = tk.Button(root, width=10,text="Exit", bg=DrT.sec_clr,relief="solid",activebackground="#FF4040",font=("Arial",14,"bold"),command=user_exit)
        self.__exit_bttn.place(x=995, y = 730)
        
        #toggle menu
        self._toggle_menu = toggle_menu_template()


#FUNCTIONS/PROCEDURES WITHIN CLASS:
    def _check_data(self):
        if DrT.data.empty == True:
            return False
        else:
            return True

    #setter for label to change to filepath
    def _set_c_file(self, filepath):
        self._c_file.config(text=f"filepath: {'%.95s' % filepath}")    

    def _hash_df(self):
        if GUI._check_data() == True:
            try:
                DrT.data['hash'] = pd.Series((hash(tuple(row)) for _, row in DrT.data.iterrows()))
                messagebox.showinfo("Successful Hash","Hash Column Successfully Created.")
            except:
                DrErr.add_error("Unknown error occoured while attempting to hash the dataframe")
                messagebox.showerror("Unknown Error", "An unexpected error occoured while hashing the dataframe, please try again")
        else:
            DrErr.add_error("user attempted to hash empty dataframe")
            messagebox.showerror("Empty DataFrame", "You have attempted to hash an empty dataframe, please try again with a non-empty dataframe")
#Inner/Nested Classes:

    #Parent Class for the graph windows:
    class g_window:
        def __init__(self, name):
            self._g_colour = "#000000"
            self._g_hue = None
            self._g_size = None
            self._y_col = "N/A"
            self._x_col = "N/A"
            self.__cmaps = plt.colormaps()
            self._g_cmap = None

            self.__df_columns = []
            for col in DrT.data.columns:
                self.__df_columns.append(col)
           
            self.__GraphWindow = tk.Toplevel(root)
            self.__GraphWindow.geometry("1400x800")
            self.__GraphWindow.config(bg=DrT.prim_clr)
            self.__title = tk.Label(self.__GraphWindow,text=name,fg="#FFFFFF",bg=DrT.prim_clr ,font=("Helvetica",18,"underline")).pack()

            #main frame
            #------------------------------------------------------------------------------------------------------------------------------#
            self._m_frame = tk.LabelFrame(self.__GraphWindow,width = 800,bg=DrT.sec_clr,height = 600)
            self._m_frame.place(x=50, y=75)
            
            self.__x_col_label = tk.Label(self._m_frame,text=f"X Axis Data: {'%.18s' % self._x_col}",bg=DrT.sec_clr,font=("Helvetica",18,"underline"))
            self.__x_col_label.place(x=25,y=25)
           
            self.__y_col_label = tk.Label(self._m_frame,text=f"Y Axis Data: {'%.18s' % self._y_col}",bg=DrT.sec_clr,font=("Helvetica",18,"underline"))
            self.__y_col_label.place(x=425,y=25)
            #Label to direct user to selecting a column from the combobox
            self.__x_ax_select_info = tk.Label(self._m_frame, bg=DrT.sec_clr,text="Select a column from the dropdown below for the X-Axis",font=("Helvetica",14))
            self.__x_ax_select_info.place(x=40,y=70)
            #Combobox to let the user select a column for the x axis
            self.__x_ax_select = ttk.Combobox(self._m_frame, values=self.__df_columns,width=115,state = "readonly")
            self.__x_ax_select.place(x=40,y=100)
            #Button to confirm selection of x axis column from combobox
            self.__x_ax_confirm = tk.Button(self._m_frame,bg=DrT.prim_clr,fg="#FFFFFF",text="Confirm Selection",command=self.__update_x_col)
            self.__x_ax_confirm.place(x=40,y=130)
            #Label to direct user to selecting a column from the combobox
            self.__y_ax_select_info = tk.Label(self._m_frame,bg=DrT.sec_clr, text="Select a column from the dropdown below for the Y-Axis",font=("Helvetica",14))
            self.__y_ax_select_info.place(x=40,y=230)
            #Combobox to let the user select a column for the y axis
            self.__y_ax_select = ttk.Combobox(self._m_frame,values=self.__df_columns,width=115,state = "readonly")
            self.__y_ax_select.place(x=40,y=260)
        
            #Button to confirm selection of y axis column from combobox
            self.__y_ax_confirm = tk.Button(self._m_frame,bg=DrT.prim_clr,fg="#FFFFFF",text="Confirm Selection",command=self.__update_y_col)
            self.__y_ax_confirm.place(x=40,y=290)
            
            #------------------------------------------------------------------------------------------------------------------------------#
           
            #options frame
            #----------------------------------------------------------------------------------------------------------------------------------------#
            self.__op_frame = tk.LabelFrame(self.__GraphWindow, width = 250,bg=DrT.sec_clr,height = 600)
            self.__op_frame.place(x=875, y=75)

            #choosing the colour of the graph
            self.__c_choose_info = tk.Label(self.__op_frame,bg=DrT.sec_clr,text="Graph colour selector",font=("Helvetica",12,"underline"))
            self.__c_choose_info.grid(column=0,row=0,pady=10,padx=15)
            self.__c_choose = tk.Button(self.__op_frame, text="Choose Colour",fg="#FFFFFF",bg=DrT.prim_clr, width=30, height=2, command = self.__clr_choose)
            self.__c_choose.grid(column=0,row=1,pady=10,padx=15)

            #choosing the hue of the graph
            #Label to direct user to selecting a column from the combobox
            self.__hue_select_info = tk.Label(self.__op_frame, bg=DrT.sec_clr,text="Select a column from the dropdown below for the hue",font=("Helvetica",12,"underline"))
            self.__hue_select_info.grid(column=0,row=2,pady=10,padx=15)
            #Combobox to let the user select a column for the hue
            self.__hue_dp = ttk.Combobox(self.__op_frame, values=self.__df_columns,width=50,state = "readonly")
            self.__hue_dp.grid(column=0,row=3,pady=10,padx=15)
            #Button to confirm selection of hue column from combobox
            self.__hue_confirm = tk.Button(self.__op_frame,bg=DrT.prim_clr,fg="#FFFFFF",text="Confirm Hue",width=30, height=2,command=self.__set_hue)
            self.__hue_confirm.grid(column=0,row=4,pady=10,padx=15)

            #choosing size correlation
            #Label to direct user to selecting a column from the combobox
            self.__size_select_info = tk.Label(self.__op_frame, bg=DrT.sec_clr,text="Select a column from the dropdown below for the size of points",font=("Helvetica",12,"underline"))
            self.__size_select_info.grid(column=0,row=5,pady=10,padx=15)
            #Combobox to let the user select a column for the hue
            self.__size_dp = ttk.Combobox(self.__op_frame, values=self.__df_columns,width=50,state = "readonly")
            self.__size_dp.grid(column=0,row=6,pady=10,padx=15)
            #Button to confirm selection of hue column from combobox
            self.__size_confirm = tk.Button(self.__op_frame,bg=DrT.prim_clr,fg="#FFFFFF",text="Confirm Size",width=30, height=2,command=self.__set_size)
            self.__size_confirm.grid(column=0,row=7,pady=10,padx=15)

            #choosing colour map
            #Label to direct user to select a colour map option
            self.__cmap_select_info = tk.Label(self.__op_frame, bg=DrT.sec_clr,text="Select a Colour Map from the below options",font=("Helvetica",12,"underline"))
            self.__cmap_select_info.grid(column=0,row=8,pady=10,padx=15)
            #Combobox to let the user select a column for the hue
            self.__cmap_list = ttk.Combobox(self.__op_frame, values=self.__cmaps,width=50,state = "readonly")
            self.__cmap_list.grid(column=0,row=9,pady=10,padx=15)
            #Button to confirm selection of hue column from combobox
            self.__cmap_confirm = tk.Button(self.__op_frame,bg=DrT.prim_clr,fg="#FFFFFF",text="Confirm Colour Map",width=30, height=2,command=self.__set_g_map)
            self.__cmap_confirm.grid(column=0,row=10,pady=10,padx=15)

            #-----------------------------------------------------------------------------------------------------------------------------------------#

            #create graph button
            self._c_graph =  tk.Button(self.__GraphWindow, text="Create Graph",width=113 ,height = 3,activebackground="#2AFF00",bg=DrT.sec_clr,command=None)
            self._c_graph.place(x=50, y=700)
        
            #close window button
            self.__close_win = tk.Button(self.__GraphWindow, text="Close",width=34 ,height = 3,activebackground="#FF4700",bg=DrT.sec_clr,command=lambda:[self.__GraphWindow.destroy()])
            self.__close_win.place(x=875,y=700)

       #updates the x and y column labels using '%.10s' % to limit the string so text doesnt overlap
        def __update_x_col(self):
            if self.__x_ax_select.get() != "":
                self._x_col = self.__x_ax_select.get()
                self.__x_col_label.config(text=f"X Axis Data: {'%.16s' % self._x_col}..")
            else:
                DrErr.add_error("User selected empty value from listbox")
                messagebox.showerror("ValueError","You have not selected a valid column from the entry box, please select a valid column")

        def __update_y_col(self):
            if self.__y_ax_select.get() != "":
                self._y_col = self.__y_ax_select.get()
                self.__y_col_label.config(text=f"Y Axis Data: {'%.16s' % self._y_col}..")
            else:
                DrErr.add_error("User selected empty value from listbox")
                messagebox.showerror("ValueError","You have not selected a valid column from the entry box, please select a valid column")
        #used to select the main colour of the graph (returns hex value)
        def __clr_choose(self):
            self._g_colour = tk.colorchooser.askcolor()[1]
        #changes the value of self.g_hue 
        def __set_hue(self):
            if self.__hue_dp.get() != "":
                self._g_hue = self.__hue_dp.get()
            else:
                DrErr.add_error("User selected empty value from listbox")
                messagebox.showerror("ValueError","You have not selected a valid column from the entry box, please select a valid column")

        def __set_g_map(self):
            if str(self.__cmap_list.get()) != "":
                self._g_cmap = str(self.__cmap_list.get())
            else:
                DrErr.add_error("User selected empty value from listbox")
                messagebox.showerror("ValueError","You have not selected a valid column from the entry box, please select a valid column")

        def __set_size(self):
            if self.__size_dp.get() != "":
                self._g_size = self.__size_dp.get()
            else:
                DrErr.add_error("User selected empty value from listbox")
                messagebox.showerror("ValueError","You have not selected a valid column from the entry box, please select a valid column")

        def _val_check(self):
            if self._y_col != "N/A" and self._x_col != "N/A":
                return True
    #Child class for each individual graph windows/graph models:
#======================================================================================================#
    class hex_plot(g_window):
        def __init__(self,name):
            super().__init__(name)
            self._c_graph.config(command=self.__cr_hex_plt)

        def __cr_hex_plt(self):
            if self._val_check() == True:
                try:
                    sns.jointplot(x=DrT.data.loc[:,self._x_col], y=DrT.data.loc[:,self._y_col], kind="hex", color=self._g_colour)
                    plt.show()
                except:
                    DrErr.add_error("Error Occoured while trying to create graph - most likely incorrect data type in column")
                    messagebox.showerror("Graphing Error","An error occoured while graphing, please check your data types for the column.")
            else:
                messagebox.showerror('Error:', 'Error - Please make sure you have chosen valid columns before you continue.')
                DrErr.add_error("Incorrect Inputs when creating a hex plot (eg missing column values) ")

#----------------------------------------------------------------------------------#
    class line_plot(g_window):
        def __init__(self, name):
            super().__init__(name)
            self._c_graph.config(command=self.__cr_line_plt)
        
        def __cr_line_plt(self):
            if self._val_check() == True:
                try:
                    sns.lineplot(x=DrT.data.loc[:,self._x_col], y=DrT.data.loc[:,self._y_col],hue=self._g_hue, data=DrT.data)
                    plt.show()
                except:
                    DrErr.add_error("Error Occoured while trying to create graph - most likely incorrect data type in column")
                    messagebox.showerror("Graphing Error","An error occoured while graphing, please check your data types for the column.")
            else:
                messagebox.showerror('Error:', 'Error - Please make sure you have chosen valid columns before you continue.')
                DrErr.add_error("Incorrect Inputs when creating a hex plot (eg missing column values) ")
#----------------------------------------------------------------------------------#
    class joint_density_plot(g_window):
            def __init__(self, name):
                super().__init__(name)
                self._c_graph.config(command=self.__cr_joint_density_plt)
            
            def __cr_joint_density_plt(self):
                if self._val_check() == True:
                    try:
                        #joint plot with topographic overlay for density
                        sns.jointplot(data=DrT.data,x=self._x_col, y=self._y_col, hue=self._g_hue,kind="kde")
                        plt.show()
                    except:
                        DrErr.add_error("Error Occoured while trying to create graph - most likely incorrect data type in column")
                        messagebox.showerror("Graphing Error","An error occoured while graphing, please check your data types for the column.")
                else:
                    messagebox.showerror('Error:', 'Error - Please make sure you have chosen valid columns before you continue.')
                    DrErr.add_error("Incorrect Inputs when creating a hex plot (eg missing column values) ")
                
#----------------------------------------------------------------------------------#
    class joint_plot(g_window):
        def __init__(self,name):
            super().__init__(name)
            self._c_graph.config(command=self.__cr_joint_plt)

        def __cr_joint_plt(self):
            if self._val_check() == True:
                try:
                    g = sns.JointGrid(data=DrT.data, x=self._x_col, y=self._y_col, marginal_ticks=True)
                    #Adding the histograms to the axes
                    g.plot_joint(sns.histplot, discrete=(True, False),cmap=self._g_cmap, pmax=.8, cbar=True,fill=True)
                    g.plot_marginals(sns.histplot, element="step", color=self._g_colour)
                    plt.show()
                except:
                    DrErr.add_error("Error Occoured while trying to create graph - most likely incorrect data type in column")
                    messagebox.showerror("Graphing Error","An error occoured while graphing, please check your data types for the column.")
            else:
                messagebox.showerror('Error:', 'Error - Please make sure you have chosen valid columns before you continue.')
                DrErr.add_error("Incorrect Inputs when creating a hex plot (eg missing column values) ")
#----------------------------------------------------------------------------------#
    class heat_map(g_window):
        def __init__(self,name):
            super().__init__(name)
            self.__df_columns = []
            for col in DrT.data.columns:
                self.__df_columns.append(col)
            self.__freq_col = None
            self.__freq_col_label = tk.Label(self._m_frame,bg=DrT.sec_clr, text="Select a column from the dropdown below for the frequency mapping",font=("Helvetica",14))
            self.__freq_col_label.place(x=40,y=380)
            self.__freq_col_select = ttk.Combobox(self._m_frame,values=self.__df_columns,width=115,state = "readonly")
            self.__freq_col_select.place(x=40,y=420)
            #Button to confirm selection of frequency column from combobox
            self.__freq_col_confirm = tk.Button(self._m_frame,bg=DrT.prim_clr,fg="#FFFFFF",text="Confirm Selection",command=self.__update_freq_col)
            self.__freq_col_confirm.place(x=40,y=450)

            self._c_graph.config(command=self.__cr_heat_map)

        def __update_freq_col(self):
            if self.__freq_col_select.get() != "":
                self.__freq_col = self.__freq_col_select.get()
                self.__freq_col_label.config(text=f"Frequency Axis Data: {'%.16s' % self.__freq_col}..")
            else:
                DrErr.add_error("User selected empty value from listbox")
                messagebox.showerror("ValueError","You have not selected a valid column from the entry box, please select a valid column")

        def __cr_heat_map(self):
            if (self._val_check() == True) and (self.__freq_col != "") and (self.__freq_col != None):
                try:
                    self.__map_data = DrT.data.pivot(index=self._y_col, columns=self._x_col, values=self.__freq_col)
                    sns.heatmap(self.__map_data, annot=True,cmap=self._g_cmap)
                    plt.show()
                except ValueError:
                    DrErr.add_error("Error Occoured while trying to create graph - most likely duplicate entries during reshaping")
                    messagebox.showerror("Graphing Error","An error occoured while graphing, Please make sure you dont have any duplicate entries")
                except:
                    DrErr.add_error("Error Occoured while trying to create graph - most likely incorrect data type in column")
                    messagebox.showerror("Graphing Error","An error occoured while graphing, please check your data types for the column.")
            else:
                messagebox.showerror('Error:', 'Error - Please make sure you have chosen valid columns before you continue.')
                DrErr.add_error("Incorrect Inputs when creating a hex plot (eg missing column values) ")
#----------------------------------------------------------------------------------#
    class pair_plot(g_window):
            def __init__(self,name):
                super().__init__(name)
                self._c_graph.config(command=self.__cr_pair_plt)

            def __cr_pair_plt(self):
                #does not need to check for x_col or y because doesnt need it 
                try:
                    sns.pairplot(DrT.data, hue=self._g_hue)
                    plt.show()
                except:
                    DrErr.add_error("Error Occoured while trying to create graph - most likely incorrect data type in column")
                    messagebox.showerror("Graphing Error","An error occoured while graphing, please check your data types for the column.")

#----------------------------------------------------------------------------------#
    class rel_plot(g_window):
            def __init__(self,name):
                super().__init__(name)
                self._c_graph.config(command=self.__cr_rel_plt)

            def __cr_rel_plt(self):
                if self._val_check() == True:
                    try:
                        sns.relplot(x=DrT.data.loc[:,self._x_col], y=DrT.data.loc[:,self._y_col], hue=self._g_hue, size=self._g_size, alpha=0.5 ,data=DrT.data)
                        plt.show()
                    except:
                        DrErr.add_error("Error Occoured while trying to create graph - most likely incorrect data type in column")
                        messagebox.showerror("Graphing Error","An error occoured while graphing, please check your data types for the column.")
                else:
                    messagebox.showerror('Error:', 'Error - Please make sure you have chosen valid columns before you continue.')
                    DrErr.add_error("Incorrect Inputs when creating a hex plot (eg missing column values) ")   

#----------------------------------------------------------------------------------#

    class box_plot(g_window):
            def __init__(self,name):
                super().__init__(name)
                self._c_graph.config(command=self.__cr_box_plt)

            def __cr_box_plt(self):
                if self._val_check() == True:
                    try:
                        sns.boxplot(x=DrT.data.loc[:,self._x_col], y=DrT.data.loc[:,self._y_col])
                        plt.show()
                    except:
                        DrErr.add_error("Error Occoured while trying to create graph - most likely incorrect data type in column")
                        messagebox.showerror("Graphing Error","An error occoured while graphing, please check your data types for the column.")
                else:
                    messagebox.showerror('Error:', 'Error - Please make sure you have chosen valid columns before you continue.')
                    DrErr.add_error("Incorrect Inputs when creating a hex plot (eg missing column values) ")   

#----------------------------------------------------------------------------------#
    class hist_plot(g_window):
            def __init__(self,name):
                if GUI._check_data():
                    super().__init__(name)
                    self._c_graph.config(command=self.__cr_hist_plt)
                else:
                    DrErr.add_error("User attempted to perform action on empty dataframe.")
                    messagebox.showerror('Error', 'Error: You have not imported a file or have imported an empty file, Please try again after importing a file!')   
  
 
            def __cr_hist_plt(self):
                if self._x_col != "":
                    try:
                        sns.distplot(a=DrT.data.loc[:,self._x_col], hist=True)
                        plt.show()
                    except:
                        DrErr.add_error("Error Occoured while trying to create graph - most likely incorrect data type in column")
                        messagebox.showerror("Graphing Error","An error occoured while graphing, please check your data types for the column.")
                else:
                    messagebox.showerror('Error:', 'Error - Please make sure you have chosen valid columns before you continue.')
                    DrErr.add_error("Incorrect Inputs when creating a hex plot (eg missing column values) ")   

#----------------------------------------------------------------------------------#

    class violin_plot(g_window):
            def __init__(self,name):
                super().__init__(name)
                self._c_graph.config(command=self.__cr_violin_plt)

            def __cr_violin_plt(self):
                if self._val_check() == True:
                    try:
                        #drawing a scatter plot that will code size and colour based on selected columns
                        sns.violinplot(x=self._x_col, y=self._y_col,data=DrT.data)
                        plt.show()
                    except:
                        DrErr.add_error("Error Occoured while trying to create graph - most likely incorrect data type in column")
                        messagebox.showerror("Graphing Error","An error occoured while graphing, please check your data types for the column.")
                else:
                    messagebox.showerror('Error:', 'Error - Please make sure you have chosen valid columns before you continue.')
                    DrErr.add_error("Incorrect Inputs when creating a hex plot (eg missing column values) ")  
#----------------------------------------------------------------------------------#


    class scat_plot(g_window):
            def __init__(self,name):
                super().__init__(name)
                self._c_graph.config(command=self.__cr_scat_plt)

            def __cr_scat_plt(self):
                if self._val_check() == True:
                    try:
                        #drawing a scatter plot that will code size and colour based on selected columns
                        sns.scatterplot(x=self._x_col, y=self._y_col,hue=self._g_hue, size=self._g_size,data=DrT.data)
                        plt.show()
                    except:
                        DrErr.add_error("Error Occoured while trying to create graph - most likely incorrect data type in column")
                        messagebox.showerror("Graphing Error","An error occoured while graphing, please check your data types for the column.")
                else:
                    messagebox.showerror('Error:', 'Error - Please make sure you have chosen valid columns before you continue.')
                    DrErr.add_error("Incorrect Inputs when creating a hex plot (eg missing column values) ")  
#----------------------------------------------------------------------------------#
    class scat3d_plot(g_window):
            def __init__(self,name):
                super().__init__(name)
                self.__df_columns = []
                for col in DrT.data.columns:
                    self.__df_columns.append(col)
                self._c_graph.config(command=self.__cr_3Dscat_plt)
                self.__z_col = None
                self.__z_col_label = tk.Label(self._m_frame,bg=DrT.sec_clr, text="Select a column from the dropdown below for the Y-Axis",font=("Helvetica",14))
                self.__z_col_label.place(x=40,y=380)
                self.__z_ax_select = ttk.Combobox(self._m_frame,values=self.__df_columns,width=115,state = "readonly")
                self.__z_ax_select.place(x=40,y=420)
                #Button to confirm selection of z axis column from combobox
                self.__z_ax_confirm = tk.Button(self._m_frame,bg=DrT.prim_clr,fg="#FFFFFF",text="Confirm Selection",command=self.__update_z_col)
                self.__z_ax_confirm.place(x=40,y=450)
                
            def __cr_3Dscat_plt(self):
                if (self._val_check() == True) and (self.__z_col != (None) and self.__z_col != ""):
                    try:
                        #creating the 3D graph:
                        #creating the figure
                        self.__fig = plt.figure()
                        #adding a subplot to the figure
                        self.__plot = self.__fig.add_subplot(projection='3d')
                        #creating the scatter plot from the pca data
                        self.__plot.scatter(xs=DrT.data.loc[:,self._x_col], ys=DrT.data.loc[:,self._y_col], zs=DrT.data.loc[:,self.__z_col],cmap=self._g_cmap,c=self._g_colour)
                        #adding the x,y and z axis labels to the 3d graph
                        self.__plot.set_xlabel(self._x_col, fontsize=10)
                        self.__plot.set_ylabel(self._y_col, fontsize=10)
                        self.__plot.set_zlabel(self.__z_col, fontsize=10)
                        plt.show()
                    except:
                        DrErr.add_error("Error Occoured while trying to create graph - most likely incorrect data type in column")
                        messagebox.showerror("Graphing Error","An error occoured while graphing, please check your data types for the column.")
                else:
                    messagebox.showerror('Error:', 'Error - Please make sure you have chosen valid columns before you continue.')
                    DrErr.add_error("Incorrect Inputs when creating a hex plot (eg missing column values) ")  
            
            def __update_z_col(self):
                if self.__z_ax_select.get() != "":
                    self.__z_col = self.__z_ax_select.get()
                    self.__z_col_label.config(text=f"Z Axis Data: {'%.16s' % self.__z_col}..")
                else:
                    DrErr.add_error("User selected empty value from listbox")
                    messagebox.showerror("ValueError","You have not selected a valid column from the entry box, please select a valid column")

    class scat_bin_plot(g_window):
        def __init__(self,name):
            super().__init__(name)
            self._c_graph.config(command=self.__cr_scat_bin_plot)
        
        def __cr_scat_bin_plot(self):
            if (self._val_check() == True):
                try:
                    #creating a scatterplot and histogram plot plot and overlaying them
                    ax = plt.subplots()
                    sns.scatterplot(x=DrT.data.loc[:,self._x_col], y=DrT.data.loc[:,self._y_col], color=self._g_colour,s=6,alpha=0.5,)
                    sns.histplot(x=DrT.data.loc[:,self._x_col], y=DrT.data.loc[:,self._y_col], bins=50, pthresh=0.1, cmap=self._g_cmap)
                    plt.show()
                except:
                    DrErr.add_error("Error Occoured while trying to create graph - most likely incorrect data type in column")
                    messagebox.showerror("Graphing Error","An error occoured while graphing, please check your data types for the column.")
            else:
                messagebox.showerror('Error:', 'Error - Please make sure you have chosen valid columns before you continue.')
                DrErr.add_error("Incorrect Inputs when creating a hex plot (eg missing column values) ")  
#======================================================================================================#

#GUI colour palette chooser
#----------------------------------------------------------------------------------------------------------------------------------------------#
    class GUI_palette():
        def __init__(self):
            try:
                self.__new_s_clr = tk.colorchooser.askcolor()[1]
                if self.__new_s_clr != None:
                    self.__change_scolour(self.__new_s_clr)
                    GUI._toggle_menu._dele_tog_menu()
                    GUI._c_file.config(bg=self.__new_s_clr)
                    GUI._import_button.config(bg=self.__new_s_clr,activebackground=self.__new_s_clr)
                    DrT.sec_clr = self.__new_s_clr
                else:
                    messagebox.showinfo('Changing colours cancelled', 'You have cancelled the change of GUI colour')
            except:
                messagebox.showerror('Error:', 'Error - An Error Occoured while trying to change the GUI colour')
                DrErr.add_error("unknown error occoured when user attempted to change GUI colour")

        #Recursive algorithm to perform a depth first search into the children of containers (to change their colour)
        def __change_scolour(self,colour,container=None):
            try:
                #checking if the container is None so that it will go back to the root window
                if container is None:
                    container = root 
                #making sure it does not change the bg of containers that do not have the DrT.sec_clr colour.
                if container != root and container != GUI._toggle_menu:
                    container.config(bg=colour)
                #checks if the container has any children entities (this can be widgets or containers)
                for child in container.winfo_children():
                    #changing only the colour of the widgets that previously had DrT.sec_clr
                    if child["background"] == DrT.sec_clr:
                        #checking if child has any children
                        if child.winfo_children():
                            #if the child has children, recurse through its children
                            self.__change_scolour(colour, child)
                        #otherwise changing certain attributes respective to which kind of widget it is.
                        elif type(child) is tk.Label:
                            child.config(bg=colour)
                        elif type(child) is tk.Button:
                            child.config(highlightbackground=colour)
                            child.config(bg=colour)
            except:
                DrErr.add_error("Error Occoured while recurring through the children of containers while changing the colour of the GUI")
                messagebox.showerror('Error', 'Error: Unkown Error Occoured While Changing Colour')  


#----------------------------------------------------------------------------------------------------------------------------------------------#

    #Parent Class for the popup windows (sets up a toplevel to help create new windows):
    class pop_window:
        def __init__(self, name):
            self._popup = tk.Toplevel(root)
            self._popup.geometry("800x500")
            self._popup.config(bg=DrT.prim_clr)
            self.__title = tk.Label(self._popup,text=name,fg="#FFFFFF",bg=DrT.prim_clr ,font=("Helvetica",18,"underline")).pack()
#----------------------------------------------------------------------------------------------------------------------------------------------#


    #Child class for each individual pop up windows:

    #child class for the Principal Component Analysis
    class DR_PCA(pop_window):
        def __init__(self,name):
            if (GUI._check_data() == True):
                #inheriting all attributes from parent class (pop_window)
                super().__init__(name)
                self._popup.geometry("900x600")
                #initialising array to hold names of columns that will undergo PCA
                self.__col_indexes = []
                self.__target_var = None
                self.__data = None
                self.__target = None
                self.__pca_data = None

                #calling on private method within class to get the names of the columns
                self.__get_columns()

                #select column portion
                #------------------------------------------------------------------------------------------------------------------------------------------------------#
                #Select column label
                self.__col_select_frame_lbl = tk.Label(self._popup,text="Select Columns for PCA",bg=DrT.prim_clr,fg="white",font=("Helvetica",15,"underline"))
                self.__col_select_frame_lbl.place(x=70,y=80)

                #creating a frame to contain the widgets used to select the columns
                self.__col_select_frame = tk.LabelFrame(self._popup,bg=DrT.sec_clr,relief="solid")
                self.__col_select_frame.place(x=20,y=120)
                #creating scrollbars for the user to view the names of the columns easier in the listbox
                self.__scroll_y_axis = tk.Scrollbar(self.__col_select_frame,orient="vertical")
                self.__scroll_x_axis = tk.Scrollbar(self.__col_select_frame, orient="horizontal")
                #creating the listbox to contain the columns in
                self.__column_list = tk.Listbox(self.__col_select_frame, relief="groove",width = 50, height=25,yscrollcommand=self.__scroll_y_axis,xscrollcommand=self.__scroll_x_axis, selectmode="multiple")
                #inserting all column names into the list box with f string formatting
                for i in range(len(self.__df_columns)):
                    self.__column_list.insert((i+1),f"{i}:| {self.__df_columns[i]}")
                #binding the command to scroll the listbox to the scroll bars and then packing them and using fill to adjust height/length respectively
                self.__scroll_y_axis.config(command=self.__column_list.yview)
                self.__scroll_y_axis.pack(fill="y",side="right")

                #packing the listbox
                self.__column_list.pack(pady=1,padx=1)

                self.__scroll_x_axis.config(command=self.__column_list.xview)
                self.__scroll_x_axis.pack(fill="x")

                self.__select_all_items = tk.Button(self.__col_select_frame,text="Select All",height=1,bg=DrT.sec_clr ,command=self.__select_all)
                self.__select_all_items.pack(fill="x")
                #--------------------

                self.__tar_combo_info = tk.Label(self._popup,text="Select the target variable for PCA:",bg=DrT.prim_clr,fg="white",font=("Helvetica",15,"underline"))
                self.__tar_combo_info.place(x=400,y=80)
                self.__target_select = ttk.Combobox(self._popup,values=self.__df_columns,width=45,state = "readonly")
                self.__target_select.place(x=400,y=120)
                self.__target_confirm = tk.Button(self._popup,bg=DrT.sec_clr,text="Confirm Target",command=self.__change_target)
                self.__target_confirm.place(x=400,y=150)

                self.__2D_PCA_bttn = tk.Button(self._popup,bg=DrT.sec_clr,text="Project with 2 dimensions",command=self.__project_2d, width=20 ,height =2,relief="solid")
                self.__2D_PCA_bttn.place(x=400,y=200)
                self.__3D_PCA_bttn = tk.Button(self._popup,bg=DrT.sec_clr,text="Project with 3 dimensions",command=self.__project_3d, width=20 ,height =2,relief="solid")
                self.__3D_PCA_bttn.place(x=400,y=250)

            else:
                DrErr.add_error("User attempted to perform action on empty dataframe.")
                messagebox.showerror('Error', 'Error: You have not imported a file or have imported an empty file, Please try again after importing a file!')   
                
        #private function to get all column names
        def __get_columns(self):
                #clearing the df_columns array
                self.__df_columns = []
                #appending the column names to the df_columns array.
                for col in DrT.data.columns:
                    self.__df_columns.append(col)

        def __change_target(self):
            self.__target_var = self.__target_select.get()

        #procedure to select all items in the listbox
        def __select_all(self):
            self.__column_list.select_set(0,tk.END)

        def __initialise_data(self,num_components):
            try:  
                #creating a numpy array to contain the indexes of the columns - equal to the numbers next to the column names
                self.__col_indexes = np.array(self.__column_list.curselection())
                #.flatten is used to collapse the array into 1 dimension
                self.__col_indexes.flatten()

                #Formatting the data into a dataframe (the data) and an array/list (the target variable)
                self.__data = DrT.data.iloc[:,self.__col_indexes]
                self.__target = DrT.data.loc[:,self.__target_var]

                #standardise the data to prevent scaling errors that could arise from different units/metrics
                self.__normaliser = StandardScaler()
                self.__normaliser.fit(self.__data)
                #normalised data df
                self.__norm_data = self.__normaliser.transform(self.__data)
                #setting up/instantiating the pca class
                #n_components refers to the number of principal components generated
                if num_components == 2:
                    self.__pca = PCA(n_components=2)
                elif num_components==3:
                    self.__pca = PCA(n_components=3)
                #using fit_transform to both .fit() the data and .transform() the data for it to be able to be projected correctly.
                self.__pca_data = self.__pca.fit_transform(self.__norm_data)   
            except ValueError:
                DrErr.add_error("ValueError - User attempted to perform PCA with incorrect inputs for either target variable or data columns(wrong datatype)")
                messagebox.showerror("ValueError","Please make sure you have selected at least 2 valid columns along with a target variable")
            except:
                DrErr.add_error("Unknown Error Occoured while initialising pca data.")
                messagebox.showerror("Unknown Error","An unknown error occoured while attempting to perform PCA")
        def __project_2d(self):
            if (len(self.__column_list.curselection()) >= 2) and (self.__target_select.get() != ""):   
                #performing pca on the data and initialising data variables, the number of principal components is 2
                self.__initialise_data(2)
                try:
                    sns.scatterplot(x=self.__pca_data[:,0], y=self.__pca_data[:,1], hue=self.__target)
                    plt.xlabel("Principal Component 1")
                    plt.ylabel("Principal Component 2")
                    plt.title("Explained Variance: "+str(round(((self.__pca.explained_variance_ratio_.sum())*100),2))+ " %")
                    plt.show()
                except:
                    DrErr.add_error("An unknown error occoured while trying to create a 2d graph of the PCA data")
                    messagebox.showerror("Unknown Error","An unknown error occoured while attempting to create the PCA graph.")
            else:
                DrErr.add_error("User attempted to perform PCA with incorrect inputs for either target variable or data columns")
                messagebox.showerror("Incorrect Inputs","Please make sure you have selected at least 2 valid columns along with a target variable")
        def __project_3d(self):
            if (len(self.__column_list.curselection()) >= 3) and (self.__target_select.get() != ""):  
                #performing pca on the data and initialising data variables, the number of principal components is 3
                self.__initialise_data(3)
                try:
                    #creating the 3D graph:
                    #creating the figure
                    self.__fig = plt.figure()
                    #adding a subplot to the figure
                    self.__plot = self.__fig.add_subplot(projection='3d')
                    #creating the scatter plot from the pca data
                    self.__plot.scatter(xs=self.__pca_data[:,0], ys=self.__pca_data[:,1], zs=self.__pca_data[:,2])#,c=self.__target)
                    #adding the x,y and z axis labels to the 3d graph
                    self.__plot.set_xlabel("Principal Component 1", fontsize=10)
                    self.__plot.set_ylabel("Principal Component 2", fontsize=10)
                    self.__plot.set_zlabel("Principal Component 3", fontsize=10)
                    self.__plot.set_title("Explained Variance: "+str(round(((self.__pca.explained_variance_ratio_.sum())*100),2))+ " %")
                    plt.show()
                except:
                    DrErr.add_error("An unknown error occoured while trying to create a 3d graph of the PCA data")
                    messagebox.showerror("Unknown Error","An unknown error occoured while attempting to create the PCA graph.")
            else:
                DrErr.add_error("User attempted to perform PCA with incorrect inputs for either target variable or data columns")
                messagebox.showerror("Incorrect Inputs","Please make sure you have selected at least 2 valid columns along with a target variable")

    #child class for KMeans clustering

    class DR_KMeans(pop_window):
        def __init__(self,name):
            if GUI._check_data() == True:
                #inheriting all attributes from parent class (pop_window)
                super().__init__(name)
                self._popup.geometry("900x600")
                self.__x_col = None
                self.__y_col = None
                self.__data = pd.DataFrame()
            
                self.__df_columns = []
                for col in DrT.data.columns:
                    self.__df_columns.append(col)
            
                self.__m_frame = tk.LabelFrame(self._popup,width = 800,bg=DrT.sec_clr,height = 500)
                self.__m_frame.place(x=50, y=75)
                
                self.__x_col_label = tk.Label(self.__m_frame,text=f"X Axis Data: {'%.18s' % self.__x_col}",bg=DrT.sec_clr,font=("Helvetica",18,"underline"))
                self.__x_col_label.place(x=25,y=25)
            
                self.__y_col_label = tk.Label(self.__m_frame,text=f"Y Axis Data: {'%.18s' % self.__y_col}",bg=DrT.sec_clr,font=("Helvetica",18,"underline"))
                self.__y_col_label.place(x=425,y=25)
                #Label to direct user to selecting a column from the combobox
                self.__x_ax_select_info = tk.Label(self.__m_frame, bg=DrT.sec_clr,text="Select a column from the dropdown below for the X-Axis",font=("Helvetica",14))
                self.__x_ax_select_info.place(x=40,y=70)
                #Combobox to let the user select a column for the x axis
                self.__x_ax_select = ttk.Combobox(self.__m_frame, values=self.__df_columns,width=65,state = "readonly")
                self.__x_ax_select.place(x=40,y=100)
                #Button to confirm selection of x axis column from combobox
                self.__x_ax_confirm = tk.Button(self.__m_frame,bg=DrT.prim_clr,fg="#FFFFFF",text="Confirm Selection",command=self.__update_x_col)
                self.__x_ax_confirm.place(x=40,y=130)
                #Label to direct user to selecting a column from the combobox
                self.__y_ax_select_info = tk.Label(self.__m_frame,bg=DrT.sec_clr, text="Select a column from the dropdown below for the Y-Axis",font=("Helvetica",14))
                self.__y_ax_select_info.place(x=40,y=180)
                #Combobox to let the user select a column for the y axis
                self.__y_ax_select = ttk.Combobox(self.__m_frame,values=self.__df_columns,width=65,state = "readonly")
                self.__y_ax_select.place(x=40,y=210)
            
                #Button to confirm selection of y axis column from combobox
                self.__y_ax_confirm = tk.Button(self.__m_frame,bg=DrT.prim_clr,fg="#FFFFFF",text="Confirm Selection",command=self.__update_y_col)
                self.__y_ax_confirm.place(x=40,y=240)
                #label to specify what to enter
                self.__max_c_info = tk.Label(self.__m_frame,text="Enter the maximum number of clusters for optimisation: ",bg=DrT.sec_clr)
                self.__max_c_info.place(x=40,y=280)
                #entry box for the number of clusters
                self.__max_c_entry = tk.Entry(self.__m_frame,width=40)
                self.__max_c_entry.place(x=40,y=310)

                #Button to carry out optimisation on number of clusters recommended
                self.__optimal_c = tk.Button(self.__m_frame, width=25, bg=DrT.sec_clr,relief="solid",font=("Arial",12,"bold"),fg="black",text="Cluster Count Optimisation",command=lambda:(self.__optimise_k_means()))
                self.__optimal_c.place(x=40,y=350)
                
                #label to specify what to enter
                self.__n_clusters_info = tk.Label(self.__m_frame,text="Enter the number of clusters: ",bg=DrT.sec_clr)
                self.__n_clusters_info.place(x=400,y=280)
                #entry box for the number of clusters
                self.__n_clusters = tk.Entry(self.__m_frame,width=40)
                self.__n_clusters.place(x=400,y=310)

                #Button to carry out Kmeans on selected columns
                self.__KMean_bttn = tk.Button(self.__m_frame, width=12, bg=DrT.sec_clr,relief="solid",font=("Arial",12,"bold"),text="KMean Graph",command=lambda:(self.__KMeans_graph()))
                self.__KMean_bttn.place(x=400,y=350)
            
            else:
                DrErr.add_error("User attempted to perform action on empty dataframe.")
                messagebox.showerror('Error', 'Error: You have not imported a file or have imported an empty file, Please try again after importing a file!')   
                

       #updates the x and y column labels using '%.10s' % to limit the string so text doesnt overlap
        def __update_x_col(self):
            if self.__x_ax_select.get() != "":
                self.__x_col = self.__x_ax_select.get()
                self.__x_col_label.config(text=f"X Axis Data: {'%.16s' % self.__x_col}..")
            else:
                DrErr.add_error("User selected empty value from listbox")
                messagebox.showerror("ValueError","You have not selected a valid column from the entry box, please select a valid column")

        def __update_y_col(self):
            if self.__y_ax_select.get() != "":
                self.__y_col = self.__y_ax_select.get()
                self.__y_col_label.config(text=f"Y Axis Data: {'%.16s' % self.__y_col}..")
            else:
                DrErr.add_error("User selected empty value from listbox")
                messagebox.showerror("ValueError","You have not selected a valid column from the entry box, please select a valid column")

        def __initialise(self):
            try:
                self.__data = DrT.data.loc[:,[self.__x_col,self.__y_col]]
                #standardising the data so that the mean is 0 and standard deviation is 1
                self.__scaler = StandardScaler()
                self.__standard_data = pd.DataFrame()
                #creating the dataframe for the standard data
                self.__standard_data[self.__data.columns.values] = self.__scaler.fit_transform(self.__data)
            except ValueError:
                DrErr.add_error("ValueError occoured during initialising KMEANS clustering most likely user did not confirm column")
                messagebox.showerror('ValueError', 'Error: Please make sure you have selected valid columns and then try again')

        def __KMeans_graph(self):
            try:
                int(self.__n_clusters.get())
                if int(self.__n_clusters.get()) > 0:
                    self.__initialise()
                    n_clusters = int(self.__n_clusters.get())
                    kmeans = KMeans(n_clusters=n_clusters,n_init="auto")
                    kmeans.fit(self.__standard_data.loc[:,:])
                    self.__data['kmeans_data'] = kmeans.labels_
                    plt.scatter(x=self.__data.loc[:,self.__x_col],y=self.__data.loc[:,self.__y_col],c=self.__data['kmeans_data'])
                    plt.show()
                else:
                    DrErr.add_error("user entered less than 1 cluster during KMEANS clustering")
                    messagebox.showerror('Error', 'Error: You have not provided a valid number of clusters, Please try again.')
            except ValueError:
                DrErr.add_error("user did not enter an integer during KMEANS clustering")
                messagebox.showerror('Error', 'Error: You have not provided a valid integer number of clusters, Please try again.') 
            except:
                DrErr.add_error("Unknown error occoured during KMEANS clustering")
                messagebox.showerror('Unknown Error', 'Error: An Unknown error occoured, Please try again after you check your inputs.')


        def __optimise_k_means(self):
            try:
                int(self.__n_clusters.get())
                if int(self.__n_clusters.get()) > 0:
                    self.__initialise()
                    #just an array to hold and keep track of cluster sizes that have been tested for graphing
                    self.__cluster_sizes = []
                    #inertias are measures of spread from the centroid - smaller inertia means smaller distance from centroid which is desired
                    self.__inertias = []
                    self.__max_c = int(self.__max_c_entry.get())

                    for c in range(1,self.__max_c):
                        kmeans = KMeans(n_clusters=c,n_init="auto")
                        kmeans.fit(self.__standard_data)

                        self.__inertias.append(kmeans.inertia_)
                        self.__cluster_sizes.append(c)

                    fig = plt.subplots(figsize=(10,5))
                    plt.plot(self.__cluster_sizes,self.__inertias,"o-")
                    plt.xlabel("Number of clusters")
                    plt.ylabel("Inertia")
                    plt.show()
                else:
                    DrErr.add_error("user entered less than 1 cluster during KMEANS clustering")
                    messagebox.showerror('Error', 'Error: You have not provided a valid number of clusters, Please try again.')
            except ValueError:
                DrErr.add_error("user did not enter an integer during KMEANS clustering")
                messagebox.showerror('Error', 'Error: You have not provided a valid integer number of clusters, Please try again.') 
            except:
                DrErr.add_error("Unknown error occoured during KMEANS clustering")
                messagebox.showerror('Unknown Error', 'Error: An Unknown error occoured, Please try again after you check your inputs.')

#Child class for calculating between columns
#----------------------------------------------------------------------------------------------------------------------------------------------#
    class calc_colms(pop_window):
        def __init__(self,name):
            #checking if data has been imported to handle exceptions
            if GUI._check_data() == True:
                super().__init__(name)
                self._popup.geometry("1200x800")
                self._popup.resizable(0,0)
                #attributes:
                self.__column_1 = None
                self.__column_2 = None
                self.__new_colm_name = None
                #column 1 (x variable) frame
                #------------------------------------------------------------------------------------------------#
                self.__col1_frame = tk.LabelFrame(self._popup,width=260,height=610,bg=DrT.sec_clr)
                self.__col1_frame.place(x=30,y=60)

                self.__col1_frame_lbl = tk.Label(self.__col1_frame,text="Select Column 1",font=("Helvetica",15,"underline"),bg=DrT.sec_clr,fg="white")
                self.__col1_frame_lbl.place(x=50,y=15)

                self.__update_combo()

                self.__colm1_select = ttk.Combobox(self.__col1_frame,values=self.__df_columns,width=30,state = "readonly")
                self.__colm1_select.place(x=20,y=80)

                self.__confirm_col2 = tk.Button(self.__col1_frame,text="Confirm Column 1",bg=DrT.prim_clr,relief="solid",fg="white",command=self.__get_col1_val)
                self.__confirm_col2.place(x=20,y=120)

                self.__col1_list_frame = tk.LabelFrame(self.__col1_frame)
                self.__col1_list_frame.place(x=15,y=180,width=228,height=350)
                
                self.__col1_view = tk.Listbox(self.__col1_list_frame, relief="groove",width = 50, height=25)
                self.__col1_view.place(relheight=0.95,relwidth=0.92)
                #creating and placing the x and y scrollbars to move the treeview window
                self.__list1scrolly = tk.Scrollbar(self.__col1_list_frame, orient="vertical", command=self.__col1_view.yview)
                self.__list1scrolly.pack(side="right",fill="y")
                
                self.__list1scrollx = tk.Scrollbar(self.__col1_list_frame, orient="horizontal", command=self.__col1_view.xview)
                self.__list1scrollx.pack(side="bottom",fill="x")
                #assigning the scrolling command to move the treeview to each scroll bar.
                self.__col1_view.config(yscrollcommand=self.__list1scrolly.set,xscrollcommand=self.__list1scrollx.set)

                self.__update1_button = tk.Button(self.__col1_frame, text="Update View", width=31 ,height = 2,fg="#FFFFFF",relief="solid",bg=DrT.prim_clr,command=lambda:(self.__update_list(1)))
                self.__update1_button.place(x=15,y=550)


                #column 2 (y variable) frame
                #------------------------------------------------------------------------------------------------#
                self.__col2_frame = tk.LabelFrame(self._popup, width=260,height=610,bg=DrT.sec_clr)
                self.__col2_frame.place(x=320,y=60)

                self.__col2_frame_lbl = tk.Label(self.__col2_frame,text="Select Column 2",font=("Helvetica",15,"underline"),bg=DrT.sec_clr,fg="white")
                self.__col2_frame_lbl.place(x=50,y=15)

                self.__update_combo()

                self.__colm2_select = ttk.Combobox(self.__col2_frame,values=self.__df_columns,width=30,state = "readonly")
                self.__colm2_select.place(x=20,y=80)

                self.__confirm_col2 = tk.Button(self.__col2_frame,text="Confirm Column 2",bg=DrT.prim_clr,relief="solid",fg="white",command=self.__get_col2_val)
                self.__confirm_col2.place(x=20,y=120)

                self.__col2_list_frame = tk.LabelFrame(self.__col2_frame)
                self.__col2_list_frame.place(x=15,y=180,width=228,height=350)
                
                self.__col2_view = tk.Listbox(self.__col2_list_frame, relief="groove",width = 50, height=25)
                self.__col2_view.place(relheight=0.95,relwidth=0.92)
                #creating and placing the x and y scrollbars to move the treeview window
                self.__list2scrolly = tk.Scrollbar(self.__col2_list_frame, orient="vertical", command=self.__col2_view.yview)
                self.__list2scrolly.pack(side="right",fill="y")
                
                self.__list2scrollx = tk.Scrollbar(self.__col2_list_frame, orient="horizontal", command=self.__col2_view.xview)
                self.__list2scrollx.pack(side="bottom",fill="x")
                #assigning the scrolling command to move the treeview to each scroll bar.
                self.__col2_view.config(yscrollcommand=self.__list2scrolly.set,xscrollcommand=self.__list2scrollx.set)

                self.__update2_button = tk.Button(self.__col2_frame, text="Update View", width=31 ,height = 2,fg="#FFFFFF",relief="solid",bg=DrT.prim_clr,command=lambda:(self.__update_list(2)))
                self.__update2_button.place(x=15,y=550)

                #operation frame
                #------------------------------------------------------------------------------------------------#
                self.__op_frame = tk.LabelFrame(self._popup, width=260,height=610,bg=DrT.sec_clr)
                self.__op_frame.place(x=610,y=60)

                self.__op_frame_lbl = tk.Label(self.__op_frame,text="Calculations",font=("Helvetica",15,"underline"),bg=DrT.sec_clr,fg="white")
                self.__op_frame_lbl.place(x=70,y=15)

                self.__add_btn = tk.Button(self.__op_frame,text="Column 1 + Column 2",height=2,width=32,fg="white",bg=DrT.prim_clr,relief="solid",command=lambda:(self.__cr_colm(mode="add")))
                self.__add_btn.place(x=10,y=70)
                self.__subtract_btn = tk.Button(self.__op_frame,text="Column 1 - Column 2",height=2,width=32,fg="white",bg=DrT.prim_clr,relief="solid",command=lambda:(self.__cr_colm(mode="sub")))
                self.__subtract_btn.place(x=10,y=145)
                self.__multiply_btn = tk.Button(self.__op_frame,text="Column 1 x Column 2",height=2,width=32,fg="white",bg=DrT.prim_clr,relief="solid",command=lambda:(self.__cr_colm(mode="mult")))
                self.__multiply_btn.place(x=10,y=220)
                self.__divide_btn = tk.Button(self.__op_frame,text="Column 1 / Column 2",height=2,width=32,fg="white",bg=DrT.prim_clr,relief="solid",command=lambda:(self.__cr_colm(mode="div")))
                self.__divide_btn.place(x=10,y=295)
                self.__raise_power_btn = tk.Button(self.__op_frame,text="Column 1 ^(Column 2)",height=2,width=32,fg="white",bg=DrT.prim_clr,relief="solid",command=lambda:(self.__cr_colm(mode="exp")))
                self.__raise_power_btn.place(x=10,y=370)
                self.__mean_btn = tk.Button(self.__op_frame,text="Mean Of Columns",height=2,width=32,fg="white",bg=DrT.prim_clr,relief="solid",command=lambda:(self.__cr_colm(mode="mean")))
                self.__mean_btn.place(x=10,y=445)

                #resulting column frame
                #------------------------------------------------------------------------------------------------#
                self.__result_col_frame = tk.LabelFrame(self._popup,width=260,height=610,bg=DrT.sec_clr)
                self.__result_col_frame.place(x=900,y=60)

                self.__result_col_frame_lbl = tk.Label(self.__result_col_frame,text="Resulting Column",font=("Helvetica",15,"underline"),bg=DrT.sec_clr,fg="white")
                self.__result_col_frame_lbl.place(x=50,y=15)

                self.__new_column_name_lbl = tk.Label(self.__result_col_frame,text=f"New Column Name: {('%.9s' % self.__new_colm_name)}",font=("Helvetica",12),bg=DrT.sec_clr,fg="white")
                self.__new_column_name_lbl.place(x=20,y=50)

                self.__colm_name_entry = tk.Entry(self.__result_col_frame, width=34)
                self.__colm_name_entry.place(x=20,y=80)

                self.__colm_name_entry_confirm = tk.Button(self.__result_col_frame,text="Confirm Name",width=28,fg="white",bg=DrT.prim_clr,relief="solid",command=self.__update_new_colm_name)
                self.__colm_name_entry_confirm.place(x=20,y=110)

                self.__col3_list_frame = tk.LabelFrame(self.__result_col_frame)
                self.__col3_list_frame.place(x=15,y=180,width=228,height=350)
                
                self.__col3_view = tk.Listbox(self.__col3_list_frame, relief="groove",width = 50, height=25)
                self.__col3_view.place(relheight=0.95,relwidth=0.92)
                #creating and placing the x and y scrollbars to move the treeview window
                self.__list3scrolly = tk.Scrollbar(self.__col3_list_frame, orient="vertical", command=self.__col3_view.yview)
                self.__list3scrolly.pack(side="right",fill="y")
                
                self.__list3scrollx = tk.Scrollbar(self.__col3_list_frame, orient="horizontal", command=self.__col3_view.xview)
                self.__list3scrollx.pack(side="bottom",fill="x")
                #assigning the scrolling command to move the treeview to each scroll bar.
                self.__col3_view.config(yscrollcommand=self.__list3scrolly.set,xscrollcommand=self.__list3scrollx.set)

                self.__update3_button = tk.Button(self.__result_col_frame, text="Update View", width=31 ,height = 2,fg="#FFFFFF",relief="solid",bg=DrT.prim_clr,command=lambda:(self.__update_list(3)))
                self.__update3_button.place(x=15,y=550)

                #close button to close the window
                self.__close_button = tk.Button(self._popup, width=20 ,height = 2,text="Exit", bg=DrT.sec_clr,relief="solid",activebackground="#FF4040",command=lambda:(self._popup.destroy()))
                self.__close_button.place(x=1010,y=700)

            else:  
                #exception handling in case that the dataframe is empty - will add the error to the error stack in DrTools
                DrErr.add_error("User attempted to perform action on empty dataframe.")
                messagebox.showerror('Error', 'Error: You have not imported a file or have imported an empty file, Please try again after importing a file!')

        def __update_combo(self):
            self.__df_columns = []
            for col in DrT.data.columns:
                self.__df_columns.append(col)

        def __get_col1_val(self):
            if self.__colm1_select.get() != "":
                self.__column_1 = self.__colm1_select.get()
            else:
                DrErr.add_error("User selected empty value from listbox")
                messagebox.showerror("ValueError","You have not selected a valid column from the entry box, please select a valid column")
            

        def __get_col2_val(self):
            if self.__colm2_select.get() != "":
                self.__column_2 = self.__colm2_select.get()
            else:
                DrErr.add_error("User selected empty value from listbox")
                messagebox.showerror("ValueError","You have not selected a valid column from the entry box, please select a valid column")
        def __update_new_colm_name(self):
            self.__new_colm_name = str(self.__colm_name_entry.get())
            self.__new_column_name_lbl.config(text=f"New Column Name: {('%.9s' % self.__new_colm_name)}")

        def __update_list(self,ID):
            if ID == 1:
                self.__col1_view.delete(0,tk.END)
                self.__display_data = DrT.data[self.__colm1_select.get()]              
                for i in range(len(self.__display_data)):
                    self.__col1_view.insert((i+1),f"{i}:| {self.__display_data.iloc[i]}")
            elif ID == 2:
                self.__col2_view.delete(0,tk.END)
                self.__display_data = DrT.data[self.__colm2_select.get()]              
                for i in range(len(self.__display_data)):
                    self.__col2_view.insert((i+1),f"{i}:| {self.__display_data.iloc[i]}")
            elif ID ==3:
                self.__col3_view.delete(0,tk.END)
                self.__display_data = DrT.data[f"{self.__new_colm_name}"]              
                for i in range(len(self.__display_data)):
                    self.__col3_view.insert((i+1),f"{i}:| {self.__display_data.iloc[i]}")

        def __cr_colm(self,mode):
            try:
                if (self.__new_colm_name != None) and (self.__column_1 != None) and (self.__column_2 != None) and (self.__new_colm_name != ""):
                    if (DrT.data[self.__column_2].isnull().sum() == 0) and (DrT.data[self.__column_1].isnull().sum() == 0):
                        if mode == "add":
                            DrT.data[f"{self.__new_colm_name}"] = DrT.data[self.__column_1] + DrT.data[self.__column_2]
                        elif mode == "sub":
                            DrT.data[f"{self.__new_colm_name}"] = DrT.data[self.__column_1] - DrT.data[self.__column_2]
                        elif mode == "mult":
                            DrT.data[f"{self.__new_colm_name}"] = DrT.data[self.__column_1] * DrT.data[self.__column_2]
                        elif mode == "div":
                            DrT.data[f"{self.__new_colm_name}"] = DrT.data[self.__column_1] / DrT.data[self.__column_2]
                        elif mode == "exp":
                            DrT.data[f"{self.__new_colm_name}"] = DrT.data[self.__column_1] ** DrT.data[self.__column_2]
                        elif mode == "mean":
                            DrT.data[f"{self.__new_colm_name}"] = (DrT.data[self.__column_1] + DrT.data[self.__column_2]) / 2
                        self.__update_list(3)
                        messagebox.showinfo(title="Successful Creation",message= (f"New column: {self.__new_colm_name} alongside values successfully created"))
                    else:
                        messagebox.showerror("Error","Before you attempt to create a new column, please make sure there are no null values in both child columns")
                        DrErr.add_error("User Attempted to create new column with invalid columns (columns containing null values)")
                else:
                    messagebox.showerror("Error","Before you attempt to create a new column, please make sure you have correctly selected: column 1, column 2 and new column name")
                    DrErr.add_error("User Attempted to create new column with invalid details (column name, column1, column2)")
            except TypeError as error:
                messagebox.showerror("Type Error:","Make sure all data in the column is quantitative! ")
                DrErr.add_error(f"{error} - user entered column containing qualitative data when adding columns")
            except:
                messagebox.showerror("Error:","An Error occoured while attempting to create new column, please check column data types")
                DrErr.add_error("Error Occoured when user attempting to create new column - most likely data type error")



#patching nulls
#==============================================================================================================================================================================#

    class patch_nulls(pop_window):
        def __init__(self,name):
            #checking if data has been imported to handle exceptions
            if GUI._check_data() == True:
                #inheriting all attributes from parent class (pop_window)
                super().__init__(name)
                self._popup.geometry("1000x600")
                self._popup.resizable(0,0)
                #initialising array to hold names of columns that will undergo null patching
                self.__df_columns = []
                #calling on private method within class to get the names of the columns
                self.__get_columns()

                #select column portion
                #------------------------------------------------------------------------------------------------------------------------------------------------------#
                #Select column label
                self.__col_select_frame_lbl = tk.Label(self._popup,text="Select Column/s",bg=DrT.prim_clr,fg="white",font=("Helvetica",15,"underline"))
                self.__col_select_frame_lbl.place(x=120,y=80)

                #creating a frame to contain the widgets used to select the columns
                self.__col_select_frame = tk.LabelFrame(self._popup,bg=DrT.sec_clr,relief="solid")
                self.__col_select_frame.place(x=20,y=120)
                #creating scrollbars for the user to view the names of the columns easier in the listbox
                self.__scroll_y_axis = tk.Scrollbar(self.__col_select_frame,orient="vertical")
                self.__scroll_x_axis = tk.Scrollbar(self.__col_select_frame, orient="horizontal")
                #creating the listbox to contain the columns in
                self.__column_list = tk.Listbox(self.__col_select_frame, relief="groove",width = 50, height=25,yscrollcommand=self.__scroll_y_axis,xscrollcommand=self.__scroll_x_axis, selectmode="multiple")
                #inserting all column names into the list box with f string formatting
                for i in range(len(self.__df_columns)):
                    self.__column_list.insert((i+1),f"{i}:| {self.__df_columns[i]}")
                #binding the command to scroll the listbox to the scroll bars and then packing them and using fill to adjust height/length respectively
                self.__scroll_y_axis.config(command=self.__column_list.yview)
                self.__scroll_y_axis.pack(fill="y",side="right")

                #packing the listbox
                self.__column_list.pack(pady=1,padx=1)

                self.__scroll_x_axis.config(command=self.__column_list.xview)
                self.__scroll_x_axis.pack(fill="x")

                self.__select_all_items = tk.Button(self.__col_select_frame,text="Select All",height=1,bg=DrT.sec_clr ,command=self.__select_all)
                self.__select_all_items.pack(fill="x")
                #------------------------------------------------------------------------------------------------------------------------------------------------------#

                #patch quantitative portion
                #------------------------------------------------------------------------------------------------------------------------------------------------------#
                self.__patch_quant_label= tk.Label(self._popup,text="Quantatitive Patching",bg=DrT.prim_clr,fg="white",font=("Helvetica",15,"underline"))
                self.__patch_quant_label.place(x=450,y=80)


                self.__patch_quant_frame=tk.LabelFrame(self._popup,bg=DrT.sec_clr,width=275,height=446,relief="solid")
                self.__patch_quant_frame.place(x=400,y=120)

                self.__replacement_method_lbl = tk.Label(self.__patch_quant_frame,text="Replacement Method:" ,bg=DrT.sec_clr,fg="black",font=("Helvetica",13))
                self.__replacement_method_lbl.place(x=20,y=20)

                #button to patch nulls with the mean
                self.__mean_patch = tk.Button(self.__patch_quant_frame,width=28,height=2, text="Patch Nulls With Mean", command=lambda:(self.__patch_columns_quant("mean")),fg="white",bg=DrT.prim_clr,relief="solid",activebackground=DrT.sec_clr)
                self.__mean_patch.place(x=30,y=70)

                #Button to patch nulls with median
                self.__median_patch = tk.Button(self.__patch_quant_frame,width=28,height=2 ,text="Patch Nulls With Median", command=lambda:(self.__patch_columns_quant("median")),fg="white",bg=DrT.prim_clr,relief="solid",activebackground=DrT.sec_clr)
                self.__median_patch.place(x=30,y=140)

                #Button to patch nulls with mode
                self.__mode_patch = tk.Button(self.__patch_quant_frame,width=28,height=2 ,text="Patch Nulls With Mode", command=lambda:(self.__patch_columns_quant("mode")),fg="white",bg=DrT.prim_clr,relief="solid",activebackground=DrT.sec_clr)
                self.__mode_patch.place(x=30,y=210)

                #Button to patch nulls with maximum
                self.__max_patch = tk.Button(self.__patch_quant_frame,width=28,height=2 ,text="Patch Nulls With Maximum", command=lambda:(self.__patch_columns_quant("max")),fg="white",bg=DrT.prim_clr,relief="solid",activebackground=DrT.sec_clr)
                self.__max_patch.place(x=30,y=280)

                #Button to patch nulls with minimum
                self.__min_patch = tk.Button(self.__patch_quant_frame,width=28,height=2 ,text="Patch Nulls With Minimum", command=lambda:(self.__patch_columns_quant("min")),fg="white",bg=DrT.prim_clr,relief="solid",activebackground=DrT.sec_clr)
                self.__min_patch.place(x=30,y=350)


                #------------------------------------------------------------------------------------------------------------------------------------------------------#

                #patch qualitative portion
                #------------------------------------------------------------------------------------------------------------------------------------------------------#

                self.__patch_qual_label= tk.Label(self._popup,text="Qualitative Patching" ,bg=DrT.prim_clr,fg="white",font=("Helvetica",15,"underline"))
                self.__patch_qual_label.place(x=750,y=80)

                self.__patch_qual_frame=tk.LabelFrame(self._popup,bg=DrT.sec_clr,width=275,height=150,relief="solid")
                self.__patch_qual_frame.place(x=700,y=120)

                self.__replacement_str_lbl = tk.Label(self.__patch_qual_frame,text="Replacement String:",bg=DrT.sec_clr,fg="black",font=("Helvetica",13))
                self.__replacement_str_lbl.place(x=20,y=10)

                self.__fill_value_entry = tk.Entry(self.__patch_qual_frame,width=38)
                self.__fill_value_entry.place(x=20,y=45)

                #creating a button to confirm the patching of quanlitative columns
                self.__patch_colm_quant = tk.Button(self.__patch_qual_frame, width=32,height=2, text="Confirm Choice", command = self.__patch_columns_qual,fg="white",bg=DrT.prim_clr,relief="solid",activebackground=DrT.sec_clr)
                self.__patch_colm_quant.place(x=20,y=85)
                #------------------------------------------------------------------------------------------------------------------------------------------------------#
                
                #change null syntax
                #------------------------------------------------------------------------------------------------------------------------------------------------------#
                self.__null_syn_frame=tk.LabelFrame(self._popup,bg=DrT.sec_clr,width=275,height=170,relief="solid")
                self.__null_syn_frame.place(x=700,y=280)

                self.__null_syn_label= tk.Label(self.__null_syn_frame,text="Change Null Syntax" ,bg=DrT.sec_clr,fg="white",font=("Helvetica",15,"underline"))
                self.__null_syn_label.place(x=45,y=10)

                self.__og_null_lbl = tk.Label(self.__null_syn_frame,text="Null Syntax: ",bg=DrT.sec_clr,fg="black",font=("Helvetica",13))
                self.__og_null_lbl.place(x=20,y=45)

                self.__og_null_syn = tk.Entry(self.__null_syn_frame,width=38)
                self.__og_null_syn.place(x=20,y=75)

                #creating a button to confirm the patching of quanlitative columns
                self.__change_null_syn = tk.Button(self.__null_syn_frame,width=32,height=2,text="Correct Null Syntax", command = self.__change_null_syntax,fg="white",bg=DrT.prim_clr,relief="solid",activebackground=DrT.sec_clr)
                self.__change_null_syn.place(x=20,y=110)
                #------------------------------------------------------------------------------------------------------------------------------------------------------#

                #delete rows with nulls
                #------------------------------------------------------------------------------------------------------------------------------------------------------#
                self.__null_row_frame=tk.LabelFrame(self._popup,bg=DrT.sec_clr,width=275,height=105,relief="solid")
                self.__null_row_frame.place(x=700,y=460)

                self.__del_null_row_label= tk.Label(self.__null_row_frame,text="Delete Rows with nulls" ,bg=DrT.sec_clr,fg="white",font=("Helvetica",15,"underline"))
                self.__del_null_row_label.place(x=35,y=10)

                #creating a button to confirm the patching of quantitative columns
                self.__del_null_rows = tk.Button(self.__null_row_frame,width=32,height=2,text="Delete Rows", command = self.__delete_null_rows,fg="white",bg=DrT.prim_clr,relief="solid",activebackground=DrT.sec_clr)
                self.__del_null_rows.place(x=20,y=50)
                #------------------------------------------------------------------------------------------------------------------------------------------------------#
            else:  
                #exception handling in case that the dataframe is empty - will add the error to the error stack in DrTools
                DrErr.add_error("User attempted to perform action on empty dataframe.")
                messagebox.showerror('Error', 'Error: You have not imported a file or have imported an empty file, Please try again after importing a file!')

        def __change_null_syntax(self):
            try:
                indexes = np.array(self.__column_list.curselection())
                #.flatten is used to collapse the array into 1 dimension
                indexes.flatten()
                for index in indexes:
                    DrT.data[self.__df_columns[index]].replace(str(self.__og_null_syn.get()), np.nan,inplace=True)
                messagebox.showinfo("Syntax Changed","The Null syntax has been successfully changed for the selected columns/s that contained the original null syntax")
            except:
                DrErr.add_error("Error Occoured while changing the syntax of null values")
                messagebox.showerror('Error', 'Error: An error occoured while changing the syntax of nulls')                  

        def __select_all(self):
            self.__column_list.select_set(0,tk.END)

        def __delete_null_rows(self):
            try:
                indexes = np.array(self.__column_list.curselection())
                #.flatten is used to collapse the array into 1 dimension
                indexes.flatten()
                for index in indexes:
                    DrT.data.dropna(axis=0, subset=[DrT.data.columns[index]],inplace=True)
                messagebox.showinfo("Deletion Complete", "Successfully deleted all rows that contained a null value from the selected column/s")
            except:
                DrErr.add_error("Error Occoured while deleting rows that contain null values")
                messagebox.showerror('Error', 'Error: An error occoured while deleting the rows that contain null values.')             
    

        def __patch_columns_qual(self):
            try:
                indexes = np.array(self.__column_list.curselection())
                #.flatten is used to collapse the array into 1 dimension
                indexes.flatten()
                for index in indexes:
                    DrT.data[self.__df_columns[index]].fillna(str(self.__fill_value_entry.get()),inplace=True)
                messagebox.showinfo("Patching Completed", "Successfully patched all qualitative null values with entered string for selected column/s")
            except:
                DrErr.add_error("Error Occoured while patching qualitative data")
                messagebox.showerror('Error', 'Error: An error occoured while patching qualitative data, please check your replacement value')             

        def __patch_columns_quant(self,method):
            try:
                indexes = np.array(self.__column_list.curselection())
                #.flatten is used to collapse the array into 1 dimension
                indexes.flatten()
                for index in indexes:
                    if method == "mean":
                        DrT.data[self.__df_columns[index]].fillna(DrT.data[self.__df_columns[index]].mean(),inplace=True)
                    elif method == "median":
                        DrT.data[self.__df_columns[index]].fillna(DrT.data[self.__df_columns[index]].median(),inplace=True)
                    elif method == "mode":
                        DrT.data[self.__df_columns[index]].fillna(DrT.data[self.__df_columns[index]].mode(),inplace=True)
                    elif method == "max":
                        DrT.data[self.__df_columns[index]].fillna(DrT.data[self.__df_columns[index]].max(),inplace=True)
                    elif method == "min":
                        DrT.data[self.__df_columns[index]].fillna(DrT.data[self.__df_columns[index]].min(),inplace=True)
                messagebox.showinfo("Patching Completed", "Successfully patched all quantitative null values with entered string for selected column/s")
            except:
                DrErr.add_error("Error Occoured while patching quantitative data")
                messagebox.showerror('Error', 'Error: An error occoured while patching qualitative data, please check your replacement value')


        #private function to get all column names
        def __get_columns(self):
                #clearing the df_columns array
                self.__df_columns = []
                #appending the column names to the df_columns array.
                for col in DrT.data.columns:
                    self.__df_columns.append(col)

#==============================================================================================================================================================================#


#column dropper
#==============================================================================================================================================================================#
    class colm_dropper(pop_window):
        def __init__(self,name):
            #checking if data has been imported to handle exceptions
            if GUI._check_data() == True:
                #inheriting all attributes from parent class (pop_window)
                super().__init__(name)
                #initialising array to hold names of columns
                self.__df_columns = []
                #calling on private method within class to get the names of the columns
                self.__get_columns()
                #creating a frame to contain the widgets used to select the columns
                self.__col_select_frame = tk.LabelFrame(self._popup)
                self.__col_select_frame.place(x=40,y=40)
                #creating scrollbars for the user to view the names of the columns easier in the listbox
                self.__scroll_y_axis = tk.Scrollbar(self.__col_select_frame,orient="vertical")
                self.__scroll_x_axis = tk.Scrollbar(self.__col_select_frame, orient="horizontal")
                #creating the listbox to contain the columns in
                self.__column_list = tk.Listbox(self.__col_select_frame, relief="groove",width = 50, height=25,yscrollcommand=self.__scroll_y_axis,xscrollcommand=self.__scroll_x_axis, selectmode="multiple")
                #inserting all column names into the list box with f string formatting
                for i in range(len(self.__df_columns)):
                    self.__column_list.insert((i+1),f"{i}:| {self.__df_columns[i]}")
                #binding the command to scroll the listbox to the scroll bars and then packing them and using fill to adjust height/length respectively
                self.__scroll_y_axis.config(command=self.__column_list.yview)
                self.__scroll_y_axis.pack(side="right",fill="y")

                self.__scroll_x_axis.config(command=self.__column_list.xview)
                self.__scroll_x_axis.pack(side="bottom",fill="x")
                #finally packing the listbox
                self.__column_list.pack(pady=10,padx=10)
                #creating a button to confirm deletion of columns
                self.__del_colm = tk.Button(self._popup, text="Confirm Choice", command = self.__delete_column, bg=DrT.sec_clr,relief="solid",activebackground=DrT.sec_clr)
                self.__del_colm.place(x= 500,y=100)
           
            else:  
                #exception handling in case that the dataframe is empty - will add the error to the error stack in DrTools
                DrErr.add_error("User attempted to perform action on empty dataframe.")
                messagebox.showerror('Error', 'Error: You have not imported a file or have imported an empty file, Please try again after importing a file!')

        #private function to delete selected columns
        def __delete_column(self):
            #creating a numpy array to contain the indexes of the columns - equal to the numbers next to the column names
            indexes = np.array(self.__column_list.curselection())
            #.flatten is used to collapse the array into 1 dimension
            indexes.flatten()
            #dropping the columns of indexes specified above
            DrT.data.drop(DrT.data.columns[indexes], axis=1, inplace=True)
            #clearing the listbox from start (0) to end (tk.END)
            self.__column_list.delete(0,tk.END)
            #re-getting the columns as they have changed since they have been removed now.
            self.__get_columns()
            #re-inserting all columns back into listbox to successefully update the listbox
            for i in range(len(self.__df_columns)):
                self.__column_list.insert((i+1),f"{i}:| {self.__df_columns[i]}")
            messagebox.showinfo("Successful Deletion","Selected Columns Deleted")

        #private function to get all column names
        def __get_columns(self):
                #clearing the df_columns array
                self.__df_columns = []
                #appending the column names to the df_columns array.
                for col in DrT.data.columns:
                    self.__df_columns.append(col)

#==============================================================================================================================================================================#

#Delete/Reshape rows
#==============================================================================================================================================================================#
    class reshape_rows(pop_window):
        def __init__(self,name):
            #checking if data has been imported to handle exceptions
            if GUI._check_data() == True:
                #inheriting all attributes from parent class (pop_window)
                super().__init__(name)
                #changing the geometry of the popup window
                self._popup.geometry("600x300")
                self._popup.config(bg=DrT.prim_clr)
                self._popup.resizable(0,0)
                #button to update the rows
                self.__update_button = tk.Button(self._popup, text="Reshape DataFrame", width=20 ,height = 2,fg="#000000",activebackground="#39ADDE",relief="solid",bg=DrT.sec_clr,command=lambda: self.__reshape_rows())
                self.__update_button.place(x=400,y=225)
                #label to explain the entry box
                self.__num_rows_label = tk.Label(self._popup, text = "Number of rows to keep: ",fg="#FFFFFF",bg=DrT.prim_clr ,font=("Helvetica",14))
                self.__num_rows_label.place(x=50,y=100)
                #entry box for the user to enter a number of rows to keep
                self.__num_rows = tk.Entry(self._popup, width=15, font=("Helvetica",20))
                self.__num_rows.place(x=300,y=100) 
                #close button to close the window
                self.__close_button = tk.Button(self._popup, width=20 ,height = 2,text="Exit", bg=DrT.sec_clr,relief="solid",activebackground="#FF4040",command=lambda:(self._popup.destroy()))
                self.__close_button.place(x=50,y=225)
            else:  
                #exception handling in case that the dataframe is empty - will add the error to the error stack in DrTools
                DrErr.add_error("User attempted to perform action on empty dataframe.")
                messagebox.showerror('Error', 'Error: You have not imported a file or have imported an empty file, Please try again after importing a file!')

        def __reshape_rows(self):
            try:
                DrT.data = DrT.data.iloc[:int(self.__num_rows.get())]
                messagebox.showinfo(title="Reshape Complete",message="Successful removal of rows")
                self._popup.destroy()
            except:
                messagebox.showerror("Error",message="Unknown error occoured while attempting to delete rows, please check your index values")
                DrErr.add_error("Error occoured during the process of reshaping the dataframe (rows)")

#==============================================================================================================================================================================#

#dataframe dimensions
#==============================================================================================================================================================================#
    class df_dimens(pop_window):
        def __init__(self,name):
            if GUI._check_data() == True:
                #inheriting all attributes from parent class (pop_window)
                super().__init__(name)
                self._popup.geometry("400x200")
                self.__data_view = tk.Label(self._popup, text=f"Rows: {DrT.data.shape[0]} \n Columns: {DrT.data.shape[1]}",fg="white",bg=DrT.prim_clr,font=("Helvetica",15))
                self.__data_view.place(x=80,y=50)
                self.__close_win = tk.Button(self._popup,text="Exit",width=10,relief="solid",bg=DrT.sec_clr,fg="black",activebackground="#FF4040",font=("Arial",14,"bold"),command=lambda:(self._popup.destroy()))
                self.__close_win.place(x=200,y=130)
            else:
                DrErr.add_error("User attempted to perform action on empty dataframe.")
                messagebox.showerror('Error', 'Error: You have not imported a file or have imported an empty file, Please try again after importing a file!')
#==============================================================================================================================================================================#

#data frame information
#==============================================================================================================================================================================#
    class info_df(pop_window):
            def __init__(self,name):
                if GUI._check_data() == True:
                    #inheriting all attributes from parent class (pop_window)
                    super().__init__(name)
                    self._popup.geometry("550x600")

                    self.__data_view = tk.Label(self._popup, text=f"{DrT.data.dtypes}",fg="white",bg=DrT.prim_clr,font=("Helvetica",15))
                    self.__data_view.place(x=80,y=50)
                    self.__close_win = tk.Button(self._popup,text="Exit",width=10,relief="solid",bg=DrT.sec_clr,fg="black",activebackground="#FF4040",font=("Arial",14,"bold"),command=lambda:(self._popup.destroy()))
                    self.__close_win.place(x=400,y=520)
                    DrT.data.info()
                    messagebox.showinfo("Information Provided", "Information about the data has been printed.")
                else:
                    DrErr.add_error("User attempted to perform action on empty dataframe.")
                    messagebox.showerror('Error', 'Error: You have not imported a file or have imported an empty file, Please try again after importing a file!')
#==============================================================================================================================================================================#

#reporting null values
#==============================================================================================================================================================================#
  
    class rep_nulls(pop_window):
        def __init__(self,name):
            if GUI._check_data() == True:
                #inheriting all attributes from parent class (pop_window)
                super().__init__(name)
                self.__data_view = tk.Label(self._popup, text=DrT.data.isnull().sum(),fg="white",bg=DrT.prim_clr,font=("Helvetica",14)).pack()
            else:
                DrErr.add_error("User attempted to perform action on empty dataframe.")
                messagebox.showerror('Error', 'Error: You have not imported a file or have imported an empty file, Please try again after importing a file!')
#==============================================================================================================================================================================#

#Random sampling of data from the dataframe
#==============================================================================================================================================================================#
    class random_sample_df(pop_window):
        def __init__(self,name):
            if GUI._check_data() == True:
                #inheriting all attributes from parent class (pop_window)
                super().__init__(name)
                #changing attributes of pop up window
                self._popup.geometry("450x200")
                self._popup.resizable(0,0)
                #label to indicate the entry box is for sample size
                self.__entry_label = tk.Label(self._popup, text = "Sample Size: ",fg="#FFFFFF",bg=DrT.prim_clr ,font=("Helvetica",14))
                self.__entry_label.place(x=25,y=70)
                #entry box for user to enter sample size
                self.__num_samples = tk.Entry(self._popup, width=15, font=("Helvetica",20))
                self.__num_samples.place(x=150,y=70)
                #button to confirm and begin sampling
                self.__sample_btn = tk.Button(self._popup, text="Sample Data", width=20 ,height = 2,fg="#000000",relief="solid",activebackground="#39ADDE",bg=DrT.sec_clr,command=lambda: self.__sample())
                self.__sample_btn.place(x=225,y=140)
            else:  
                #exception handling in case that the dataframe is empty - will add the error to the error stack in DrTools
                DrErr.add_error("User attempted to perform action on empty dataframe.")
                messagebox.showerror('Error', 'Error: You have not imported a file or have imported an empty file, Please try again after importing a file!')

        def __sample(self):
            try:
                #performing a random sample that will sample on the axis 0 (aka sample rows)
                DrT.data = DrT.data.sample(n=(int(self.__num_samples.get())), axis=0)
                messagebox.showinfo(title="Sample Complete",message="Successful Sampling of Rows")
                self._popup.destroy()
            except:
                messagebox.showerror("Error",message="Unknown error occoured while attempting to sample, please check your sample size")
                DrErr.add_error("Error occoured during the process of sampling")
            

#==============================================================================================================================================================================#

#importing databases
#==============================================================================================================================================================================#
    class import_database(pop_window):
        def __init__(self,name):
            super().__init__(name)
            self.__import_db_frame = tk.LabelFrame(self._popup, text ="Enter Database Details",bg=DrT.sec_clr,fg="black")
            self.__import_db_frame.place(x=75,y=75,width=650,height=380)

            self.__username_entry_info = tk.Label(self.__import_db_frame,text="ENTER USERNAME TO DATABASE:",fg="black",bg=DrT.sec_clr,font=("Arial",10)).place(x=50,y=50)
            self.__username_entry = tk.Entry(self.__import_db_frame,width=40)
            self.__username_entry.place(x=50,y=80)
            self.__password_entry_info = tk.Label(self.__import_db_frame,text="ENTER PASSWORD TO DATABASE:",fg="black",bg=DrT.sec_clr,font=("Arial",10)).place(x=50,y=120)
            self.__password_entry = tk.Entry(self.__import_db_frame,width=40)
            self.__password_entry.place(x=50,y=160)
            self.__host_entry_info = tk.Label(self.__import_db_frame,text="ENTER HOST OF DATABASE:",fg="black",bg=DrT.sec_clr,font=("Arial",10)).place(x=50,y=200)
            self.__host_entry = tk.Entry(self.__import_db_frame,width=40)
            self.__host_entry.place(x=50,y=240)
            self.__database_entry_info = tk.Label(self.__import_db_frame,text="ENTER NAME OF DATABASE:",fg="black",bg=DrT.sec_clr,font=("Arial",10)).place(x=380,y=50)
            self.__database_entry = tk.Entry(self.__import_db_frame,width=40)
            self.__database_entry.place(x=380,y=80)
            self.__cq_tn_entry_info = tk.Label(self.__import_db_frame,text="ENTER SQL QUERY OR TABLE NAME:",fg="black",bg=DrT.sec_clr,font=("Arial",10)).place(x=380,y=120)
            self.__cq_tn_entry = tk.Entry(self.__import_db_frame,width=40)
            self.__cq_tn_entry.place(x=380,y=160)
            self.__import_bttn = tk.Button(self.__import_db_frame,text="Import Data",width=10,relief="solid",bg=DrT.prim_clr,fg="white",activebackground="green",font=("Arial",14,"bold"),command=lambda:(self.__import_data())).place(x=500,y=300)


        def __import_data(self):
            self.__URL = self.__URL_Creator(
                dialect="mysql",
                username=self._get_username(),
                password=self._get_password(),
                host=self._get_host(),
                database=self._get_database())
            
            self.__mysql_engine = create_engine(self.__URL)

            #QC_TN is custom query or table name (user assigns a string to this variable to get data from a database)
            self.__cq_tn = self._get_cq_tn()
            #read_sql is a wrapper for read_sql_table and query so the first arg can either be a table name which then uses read_sql_table or if a query is passed through, will use read_sql_query

            try:
                DrT.data = pd.read_sql(self.__cq_tn,self.__mysql_engine)
                GUI._set_c_file(f"SQL DATABASE; Host: {self._get_host()}, Username: {self._get_username()}, Database: {self._get_database()}")
                messagebox.showinfo(title="Connection Established",message="Successful Connection And Retrieval Of Data")
                self._popup.destroy()
            except exc.OperationalError as err:
                error = str(err.__dict__['orig'])
                DrErr.add_error(error)
                #Entered database does not exist
                if "1049" in error:
                    messagebox.showerror("error code: 1049","The Database does not exist.")
                #Connection Error - Invalid server host
                elif "2005" in error:
                    messagebox.showerror("error code: 2005","Unknown server host - could not resolve a connection between host")
                #auth error - invalid user / pass
                elif "1045" in error:
                    messagebox.showerror("error code: 1045","Incorrect Password or Username - Access Denied.")
                #invalid column name in query syntax
                elif "1054" in error:
                    messagebox.showerror("error code: 1054","Column does not exist in Table")
            except exc.ProgrammingError as err:
                error =  str(err.__dict__['orig'])
                DrErr.add_error(error)
                if "1064" in error:
                    messagebox.showerror("error code: 1064","You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use")
                else:
                    messagebox.showerror("error code: Unknown error","Unexpected error occoured, try again")
            
        #creates a connection URL using f string manipulation
        def __URL_Creator(self,dialect,username,password,host,database):
            URL = f"{dialect}://{username}:{password}@{host}/{database}"
            return URL
        
        #Accessors for the private entry boxes: username, password, host, database
        def _get_username(self):
            return self.__username_entry.get()
        def _get_password(self):
            return self.__password_entry.get()
        def _get_host(self):
            return self.__host_entry.get()
        def _get_database(self):
            return self.__database_entry.get()
        def _get_cq_tn(self):
            return self.__cq_tn_entry.get()
#==============================================================================================================================================================================#

#getting data from an api
#==============================================================================================================================================================================#
    class api_import(pop_window):
        def __init__(self,name):
            super().__init__(name)
            self._popup.geometry("300x150")
            self._popup.resizable(0,0)
            self.__instructions = tk.Label(self._popup,text="Enter the URL:" ,fg="white",bg=DrT.prim_clr,font=("Helvetica",14))
            self.__instructions.place(x=15,y=40)
            self.__user_url_input = tk.Entry(self._popup,width=45)
            self.__user_url_input.place(x=15,y=70)
            self.__json_button = tk.Button(self._popup,text="Import as JSON",fg="white",width=16,height=2,relief="solid",bg=DrT.sec_clr,command=lambda:(self.__get_url("json")))
            self.__json_button.place(x=15,y=100)
            self.__csv_button = tk.Button(self._popup,text="Import as CSV",fg="white",width=16,height=2,relief="solid",bg=DrT.sec_clr,command=lambda:(self.__get_url("csv")))
            self.__csv_button.place(x=170,y=100)

        def __get_url(self,mode):
            try:
                if mode == "csv":
                    DrT.data = pd.read_csv(self.__user_url_input.get())
                    GUI._set_c_file(self.__user_url_input.get())
                elif mode == "json":
                    DrT.data = pd.read_json(self.__user_url_input.get())
                    GUI._set_c_file(self.__user_url_input.get())
                messagebox.showinfo("Successful Import","Data imported successfully.")
                self._popup.destroy()
            #simple error handling in case of importing errors
            except ValueError:
                messagebox.showerror('Importing Error', 'Error: File could not be opened, Please check whether the data was outputted as CSV or JSON and try again!')
                DrErr.add_error("Value error, file couldnt be opened when importing via CSV URL method ")
            except FileNotFoundError:
                messagebox.showerror('Importing Error', 'Error: You have not entered a valid public URL, Please try again!')
                DrErr.add_error("FileNotFoundError , the file could not be located - invalid URL provided ")
            except:
                messagebox.showerror('Unknown Importing Error', 'An Unknown Error Occoured, make sure you have entered a valid API/URL')
                DrErr.add_error("Unknown Error, An unknown error occoured when the user attempted to import data via API/URL")                

#==============================================================================================================================================================================#

#------------------------------------------------------------------------------------------
        #Child class of graph window where user can choose which model they desire.
    class graph_chooser(pop_window):
        def __init__(self,name):
            if GUI._check_data() == True:
                #inheriting all attributes from parent class (pop_window)
                super().__init__(name)
                self._popup.geometry("800x600")

                self.__graph_choose_frame = tk.LabelFrame(self._popup, bg=DrT.sec_clr,width=600,height=400,relief="solid")
                self.__graph_choose_frame.place(x=40,y=100)

                self.__hex_btn = tk.Button(self.__graph_choose_frame,text="Hex plot",command=lambda:(GUI.hex_plot("Hex Plot")),width=40,height=2,relief="solid",bg=DrT.prim_clr,fg="white")
                self.__hex_btn.grid(column=0,row=0,padx=30,pady=10)
                self.__joint_plot_btn = tk.Button(self.__graph_choose_frame,text="Joint Plot",command=lambda:(GUI.joint_plot("Joint Plot")),width=40,height=2,relief="solid",bg=DrT.prim_clr,fg="white")
                self.__joint_plot_btn.grid(column=0,row=1,padx=30,pady=10)           
                self.__heat_map_btn = tk.Button(self.__graph_choose_frame,text="Heat Map",command=lambda:(GUI.heat_map("Heat Map")),width=40,height=2,relief="solid",bg=DrT.prim_clr,fg="white")
                self.__heat_map_btn.grid(column=0,row=2,padx=30,pady=10)
                self.__pair_plot_btn = tk.Button(self.__graph_choose_frame,text="Pair Plot",command=lambda:(GUI.pair_plot("Pair Plot")),width=40,height=2,relief="solid",bg=DrT.prim_clr,fg="white")
                self.__pair_plot_btn.grid(column=0,row=3,padx=30,pady=10)
                self.__rel_plot_btn = tk.Button(self.__graph_choose_frame,text="Rel Plot",command=lambda:(GUI.rel_plot("Rel Plot")),width=40,height=2,relief="solid",bg=DrT.prim_clr,fg="white")
                self.__rel_plot_btn.grid(column=0,row=4,padx=30,pady=10)
                self.__scat_btn = tk.Button(self.__graph_choose_frame,text="Scatter Plot",command=lambda:(GUI.scat_plot("Scatter Plot")),width=40,height=2,relief="solid",bg=DrT.prim_clr,fg="white")
                self.__scat_btn.grid(column=1,row=0,padx=30,pady=10)
                self.__hill_shade_btn = tk.Button(self.__graph_choose_frame,text="3D Scatter Plot",command=lambda:(GUI.scat3d_plot("3D Scatter Plot")),width=40,height=2,relief="solid",bg=DrT.prim_clr,fg="white")
                self.__hill_shade_btn.grid(column=1,row=1,padx=30,pady=10)
                self.__joint_denisty_plot_btn = tk.Button(self.__graph_choose_frame,text="joint density",command=lambda:(GUI.joint_density_plot("joint density plot")),width=40,height=2,relief="solid",bg=DrT.prim_clr,fg="white")
                self.__joint_denisty_plot_btn.grid(column=1,row=2,padx=30,pady=10)
                self.__line_plt_btn = tk.Button(self.__graph_choose_frame,text="line plot",command=lambda:(GUI.line_plot("line plot")),width=40,height=2,relief="solid",bg=DrT.prim_clr,fg="white")
                self.__line_plt_btn.grid(column=1,row=3,padx=30,pady=10)
                self.__spd_plt_btn = tk.Button(self.__graph_choose_frame,text="Scatter plot w/ density bins",command=lambda:(GUI.scat_bin_plot("Scatter Plot w/ Density bins")),width=40,height=2,relief="solid",bg=DrT.prim_clr,fg="white")
                self.__spd_plt_btn.grid(column=1,row=4,padx=30,pady=10)
                self.__hist_plt_btn = tk.Button(self.__graph_choose_frame,text="Violin Plot",command=lambda:(GUI.violin_plot("Violin Plot")),width=40,height=2,relief="solid",bg=DrT.prim_clr,fg="white")
                self.__hist_plt_btn.grid(column=0,row=5,padx=30,pady=10)
                self.__box_plt_btn = tk.Button(self.__graph_choose_frame,text="Box Plot",command=lambda:(GUI.box_plot("Box Plot")),width=40,height=2,relief="solid",bg=DrT.prim_clr,fg="white")
                self.__box_plt_btn.grid(column=1,row=5,padx=30,pady=10)


                self.__close_wind = tk.Button(self._popup,text="Exit",width=10,relief="solid",bg=DrT.sec_clr,fg="black",activebackground="#FF4040",font=("Arial",14,"bold"),command=lambda:(self._popup.destroy()))
                self.__close_wind.place(x=615,y=525)
            else:
                DrErr.add_error("User attempted to perform action on empty dataframe.")
                messagebox.showerror('Error', 'Error: You have not imported a file, Please try again after importing a file!') 
#------------------------------------------------------------------------------------------
    #parent class for treeview window used to view the dataframe
    class Dr_TV:
        def __init__(self, name):
            self.__popup = tk.Toplevel(root)
            self.__popup.geometry("1000x800")
            self.__popup.config(bg=DrT.prim_clr)
            self.__title = tk.Label(self.__popup,text=name,fg="#FFFFFF",bg=DrT.prim_clr ,font=("Helvetica",18,"underline")).pack()
            
            self.__data_view_frame = tk.LabelFrame(self.__popup,text=name)
            self.__data_view_frame.place(y=200,x=50,height=500,width=900)

            self.__update_button = tk.Button(self.__popup, text="Update View", width=20 ,height = 2,fg="#000000",relief="solid",activebackground="#39ADDE",bg=DrT.sec_clr,command=lambda: self.__update_tree_view())
            self.__update_button.place(x=800,y=100)
            
            self.__num_rows_label = tk.Label(self.__popup, text = "Number of rows to be displayed: \n (Leave empty to display all)",fg="#FFFFFF",bg=DrT.prim_clr ,font=("Helvetica",14))
            self.__num_rows_label.place(x=50,y=100)

            self.__num_rows = tk.Entry(self.__popup, width=20, font=("Helvetica",20))
            self.__num_rows.place(x=340,y=100) 

            self.__data_tv = ttk.Treeview(self.__data_view_frame)
            self.__data_tv.place(relheight=0.975, relwidth=0.975)

            #creating and placing the x and y scrollbars to move the treeview window
            self.__treescrolly = tk.Scrollbar(self.__data_view_frame, orient="vertical", command=self.__data_tv.yview)
            self.__treescrolly.pack(side="right",fill="y")
            
            self.__treescrollx = tk.Scrollbar(self.__data_view_frame, orient="horizontal", command=self.__data_tv.xview)
            self.__treescrollx.pack(side="bottom",fill="x")
            #assigning the scrolling command to move the treeview to each scroll bar.
            self.__data_tv.config(yscrollcommand=self.__treescrolly.set,xscrollcommand=self.__treescrollx.set)

            self.__update_tree_view()

            
        def __update_tree_view(self):
            #initially clears the treeview
            self.__clear_tree_view()
            self.__display_data = self._tv_data
            #checking if the entry box for number of rows is empty
            if self.__num_rows.get() != "":
                try:
                    self.__display_data = self._tv_data.iloc[:int(self.__num_rows.get())]
                except:
                    DrErr.add_error("User did not enter correct data type (integer) into entry box - Number of rows entry box in view dataframe")
                    messagebox.showerror('Error', 'Error: You have not entered an integer as the number of rows you wish to display')

            #splits the dataframe into columns which are inserted into the treeview via a for loop
            self.__data_tv["column"] = list(self.__display_data.columns)
            self.__data_tv["show"] = "headings"
            for column in self.__data_tv["columns"]:
                self.__data_tv.heading(column,text=column)
            #splitting the dataframe into rows which are then inserted via for loop
            dis_df_rows = self.__display_data.to_numpy().tolist()
            for row in dis_df_rows:
                self.__data_tv.insert("","end",values=row)

        def __clear_tree_view(self):
            self.__data_tv.delete(*self.__data_tv.get_children())  #using splat operator to delete all the children of the tree view

    class view_data_frame(Dr_TV):
        def __init__(self,name):
            if GUI._check_data() == True:
                self._tv_data = DrT.data
                super().__init__(name)
            else:
                DrErr.add_error("User attempted to perform action on empty dataframe.")
                messagebox.showerror('Error', 'Error: You have not imported a file or have imported an empty file, Please try again after importing a file!')
            
    class desc_df(Dr_TV):
        def __init__(self,name):
            if GUI._check_data() == True:
                self._tv_data = DrT.data.describe().reset_index()
                super().__init__(name)
            else:
                DrErr.add_error("User attempted to perform action on empty dataframe.")
                messagebox.showerror('Error', 'Error: You have not imported a file, Please try again after importing a file!')

class toggle_menu_template:
    def __init__(self):
        self.__CLOSE_TOG = ImageTk.PhotoImage(DrT.CLOSE_IMG)
        self.__TOG_MENU_OPEN = ImageTk.PhotoImage(Image.open("data_room_bttn.png"))
        tk.Button(root, image=self.__TOG_MENU_OPEN,
                command=self.__toggle_win,
                bg=DrT.prim_clr,
                border=0,
                activebackground=DrT.prim_clr).place(x=1000,y=0)

    #removes the toggled menu from the main menu
    def _dele_tog_menu(self):
        self.__tog_menu.destroy()
    
    #generalised bttn function for the toggled menu (modularising the original button widget for more effecient implementation)
    def __bttn(self,x,y,text,bcolour,fcolour,cmnd):
        #procedure to change the colour of the button when the cursor is on it.
        def __on_entering_t(event):
            m_bttn['background'] = bcolour
            m_bttn['foreground']= '#262626'
        #procedure to return the colour of the button to its original when cursor leaves it.
        def __on_leaving_t(event):
            m_bttn['background'] = fcolour
            m_bttn['foreground']= '#262626'
        #Creating the tkinter button.
        m_bttn = tk.Button(self.__tog_menu ,text=text,
                        width=42,
                        height=2,
                        fg='#262626',
                        bg=fcolour,
                        border=0,
                        activeforeground='#262626',
                        activebackground=bcolour,            
                        command=cmnd)
        #binding the previously defined procedure (on_entering) to the event that the cursor enters the button
        m_bttn.bind('<Enter>', __on_entering_t)
        #binding the previously defined procedure (on_leaving) to the event that the cursor leaves the button
        m_bttn.bind('<Leave>', __on_leaving_t)
        #Placing the button with respect to Args passed in
        m_bttn.place(x=x,y=y)

    #subroutine to toggle on and off the dropdown menu on the right side of the root window
    def __toggle_win(self):
        self.__tog_menu=tk.Frame(root,width=200,height=800,bg="#40C6FF")
        self.__tog_menu.place(x=1000,y=0)

        #defining the buttons using the bttn subroutine defined above.
        self.__bttn(-50,5, "S E T T I N G S","#40C6FF","#40C6FF", None)
        self.__bttn(-50,80,"Import data from Excel File","#39ADDE","#40C6FF", lambda: (import_data_xlsx()))
        self.__bttn(-50,120,"Import data from API via URL","#39ADDE","#40C6FF", lambda: (GUI.api_import("CSV URL IMPORT")))
        self.__bttn(-50,160,"Import From Database","#39ADDE","#40C6FF",lambda:(GUI.import_database("Import Database")))
        self.__bttn(-50,200,"Export As Excel File","#39ADDE","#40C6FF",lambda:(Dr_Exporter.sv_excel(opt_index=False,opt_header=True,compressiontype=True)))
        self.__bttn(-50,240,"Export As CSV File","#39ADDE","#40C6FF", lambda:(Dr_Exporter.sv_csv(opt_index=False,opt_header=True,compressiontype=True)))
        self.__gui_clr_lbl = tk.Label(self.__tog_menu,text="Change Colour Of GUI: ",bg="#40C6FF")
        self.__gui_clr_lbl.place(x=35, y=280)
        self.__gui_clr_bttn = tk.Button(self.__tog_menu,width=2, height=1,borderwidth=1,bg =DrT.sec_clr,activebackground=DrT.sec_clr,command = lambda:(GUI.GUI_palette()))
        self.__gui_clr_bttn.place(x=165,y=279)
        self.__bttn(-50,304,"Hash DataFrame","#39ADDE","#40C6FF",lambda:(GUI._hash_df()))
        self.__bttn(-50,440,"Error Console (Dev Purpose)","#39ADDE","#40C6FF",lambda:(DrErr.error_console()))

        #importing the image that will act as the button to close the menu
        #Creating the button to close the toggled window.
        tk.Button(self.__tog_menu,
                image=self.__CLOSE_TOG,
                border=0,
                command=self._dele_tog_menu,
                bg="#40C6FF",
                activebackground="#40C6FF").place(x=5,y=10)

       
if __name__ == "__main__":
    GUI = GUI_template()
    root.mainloop()
