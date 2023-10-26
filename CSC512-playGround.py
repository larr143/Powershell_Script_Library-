import tkinter as tk
from tkinter import ttk
import os 

class windows(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        
        # Adding a title to the window
        self.wm_title("Script Library")

        # creating a frame and assigning it to container
        container = tk.Frame(self, width=400,height=600)
        
        # specifying the region where the frame is packed in root
        container.pack(side="top", fill="both", expand=True)

        # configuring the location of the container using grid
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # We will now create a dictionary of frames
        self.frames = {}
        
        # we'll create the frames themselves later but let's add the components to the dictionary.
        for F in (MainPage, SearchPage,TreeSearch,BasicSearch, LibraryCreatorOrLocator):
            frame = F(container, self)

            # the windows class acts as the root window for the frames.
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Using a method to switch frames
        self.show_frame(MainPage)
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        # raises the current frame to the top
        frame.tkraise()
        
        
        
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config = find_or_create_config()
        self.what_to_display()
        
    def clear_page(self):
        # Destroy all widgets inside the frame
        for widget in self.winfo_children():
            widget.destroy()

    def what_to_display(self):
        
        self.clear_page()
        
        
        label = tk.Label(self, text="Welcome To Your Script Library!")
        label.pack(padx=10, pady=10)
        
        if self.config.read() == "":
            label = tk.Label(self, text= "Please click on find or create library button to create or find your script library.")

            switch_to_Config_button = tk.Button(
                self,
                text="Find Or Create Library",
                command=lambda: self.controller.show_frame(LibraryCreatorOrLocator),
            )
            switch_to_Config_button.pack(side="bottom", fill=tk.X)
   
            
        else:
             
            
            # We use the switch_to_search_button in order to call the show_frame() method as a lambda function
            switch_to_search_button = tk.Button(
                self,
                text="Search For Scripts",
                command=lambda: self.controller.show_frame(SearchPage),
            )
            switch_to_search_button.pack(side="bottom", fill=tk.X)
        
            # Switch to Tree search
            switch_to_TreeSearch_button = tk.Button(
                self,
                text="Tree Script Search",
            command=lambda: self.controller.show_frame(TreeSearch),
            )
            switch_to_TreeSearch_button.pack(side="bottom", fill=tk.X)
        
            switch_to_BasicSearch_button = tk.Button(
                self,
                text="Basic Script Search",
                command=lambda: self.controller.show_frame(BasicSearch),
            )
            switch_to_BasicSearch_button.pack(side="bottom", fill=tk.X)


class LibraryCreatorOrLocator(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        
        label = tk.Label(self, text = "Please input the path of your script libary or the path where you want the library created.")
        label.pack(padx=10, pady=10)
        
        self.config = find_or_create_config()
        
        self.path = ""
        
        self.entry1 = tk.Entry(self, width= 40)
        self.entry1.pack(padx=10,pady=10)
        
        button = tk.Button(self, text="Enter", command=self.find_path)
        button.pack(padx=10, pady=10)
        

    def find_path(self):
        
        self.path = self.entry1.get()
        
        if self.path: 
            if os.path.exists(self.path):
                dirList = os.listdir(self.path)
                
                if "ScriptLibrary" in dirList:
                    self.path = os.path.join(self.path, "ScriptLibrary")
                                        
                    self.config.write(self.path)
                    
                    self.config.close()
                    
                    self.controller.frames[MainPage].what_to_display()
                    
                    self.controller.show_frame(MainPage)
                
                
                else:
                    os.mkdir(os.path.join(self.path, "ScriptLibrary")) 
                    self.path = os.path.join(self.path, "ScriptLibrary")
                    
                    self.config.write(self.path)
                    
                    self.controller.frames[MainPage].what_to_display()
                    
                    self.controller.show_frame(MainPage)
                
            else:
                self.path = ""
            
        else:
            self.path = ""
        
        



class SearchPage(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="This Is the Search Page")
        label.pack(padx=10, pady=10)

        go_Back_Button = tk.Button(
            self,
            text="Go Back",
            command=lambda: controller.show_frame(MainPage),
        )
        go_Back_Button.pack(side="bottom", fill=tk.X)

class TreeSearch(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Welcome to Tree Search")
        label.pack(padx=10, pady=10)
        
        go_Back_Button = tk.Button(
            self,
            text="Go Back",
            command=lambda: controller.show_frame(MainPage),
        )
        go_Back_Button.pack(side="bottom", fill=tk.X)
        
class BasicSearch(tk.Frame):
    
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        label = tk.Label(self, text="Welcome to Basic Search")
        label.pack(padx=10, pady=10)
        
        go_Back_Button = tk.Button(
            self,
            text="Go Back",
            command=lambda: controller.show_frame(MainPage),
        )
        go_Back_Button.pack(side="bottom", fill=tk.X)
        
        
        
def find_or_create_config():
    
    # Grabbing current directory list
    dirList = os.listdir()
     
    # finding script library file 
    if 'scriptLibrary' in dirList:
        # Creates the path to the found file 
        dirList = os.listdir(os.path.join(os.getcwd() + '/scriptLibrary'))
        
        #Checks if the config file exists, if so it sets config file to read and write on the file. 
        if 'ScriptLibrary.txt' in dirList:
            configFile = open((os.path.join(os.getcwd() + '/scriptLibrary' + "/ScriptLibrary.txt")), "w+")
        
        # If it doesnt exist it creates the config file
        else:
            cwd = os.getcwd()
            path = os.path.join(cwd, "/scriptLibrary", '/ScriptLibrary.txt')
            configFile = open(path, 'x')
           
    # if it doesnt exist it creates the file and config text file  
    else:
        cwd = os.getcwd()
        path = os.path.join(cwd, "scriptLibrary")
        os.makedirs(path)
        dirList = os.listdir(os.path.join(os.getcwd() + '/scriptLibrary'))
        
        if 'ScriptLibrary.txt' in dirList:
            configFile = open((os.path.join(os.getcwd() + '/scriptLibrary' + "/ScriptLibrary.txt")), "w+")

        else:
            cwd = os.getcwd()
            path = os.path.join(cwd, "/scriptLibrary", '/ScriptLibrary.txt')
            configFile = open(path, 'x')
           
    return(configFile)
        
        
        
if __name__ == "__main__":
    testObj = windows()
    testObj.mainloop()