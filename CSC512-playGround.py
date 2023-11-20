import tkinter as tk
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

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Using a method to switch frames
        self.show_frame(MainPage) 
        
    def show_frame(self, cont):
        frame = self.frames[cont]
        if cont is MainPage: [frame.config_init(), frame.what_to_display()]
        if cont is TreeSearch: frame.directory_display()
        frame.tkraise()
        
        
        
class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.config = None
        
    def clear_page(self):
        # Destroy all widgets inside the frame
        for widget in self.winfo_children():
            widget.destroy() 
            
    def config_init(self):  
        self.config = find_or_create_config()

    def what_to_display(self):
        
        self.clear_page()
        
        label = tk.Label(self, text="Welcome To Your Script Library!")
        label.pack(padx=10, pady=10)
        
        if self.config.read() == "":
            label = tk.Label(self, text= "Please click on find or create library button to create or find your script library.")

            switch_to_Config_button = tk.Button(
                self,
                text="Find Or Create Library",
                command=lambda: [self.controller.show_frame(LibraryCreatorOrLocator), self.config.close()],
            )
            switch_to_Config_button.pack(side="bottom", fill=tk.X)
   
            
        else:
             
            
            # We use the switch_to_search_button in order to call the show_frame() method as a lambda function
            switch_to_search_button = tk.Button(
                self,
                text="Search For Scripts",
                command=lambda: [self.controller.show_frame(SearchPage), self.config.close()],
            )
            switch_to_search_button.pack(side="bottom", fill=tk.X)
        
            # Switch to Tree search
            switch_to_TreeSearch_button = tk.Button(
                self,
                text="Tree Script Search",
            command=lambda: [self.controller.show_frame(TreeSearch), self.config.close()],
            )
            switch_to_TreeSearch_button.pack(side="bottom", fill=tk.X)
        
            switch_to_BasicSearch_button = tk.Button(
                self,
                text="Basic Script Search",
                command=lambda: [self.controller.show_frame(BasicSearch), self.config.close()],
            )
            switch_to_BasicSearch_button.pack(side="bottom", fill=tk.X)

class LibraryCreatorOrLocator(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        
        label = tk.Label(self, text = "Please input the path of your script library or the path where you want the library created.")
        label.pack(padx=10, pady=10)
        
        self.path = ""
        
        self.entry1 = tk.Entry(self, width= 40)
        self.entry1.pack(padx=10,pady=10)
        
        button = tk.Button(self, text="Enter", command=self.find_path)
        button.pack(padx=10, pady=10)
        

    def find_path(self):
        
        self.config = find_or_create_config()
        
        self.path = self.entry1.get()
        
        if self.path: 
            if os.path.exists(self.path):
                dirList = os.listdir(self.path)
                
                if "ScriptLibrary" in dirList:
                    self.path = os.path.join(self.path, "ScriptLibrary")
                                        
                    self.config.write(self.path)
                    
                    self.config.close()
                    
                    self.controller.show_frame(MainPage)
                
                
                else:
                    os.mkdir(os.path.join(self.path, "ScriptLibrary")) 
                    self.path = os.path.join(self.path, "ScriptLibrary")
                    
                    self.config.write(self.path)
                    
                    self.config.close()
                    
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
        self.library_path = ""
        self.working_path = ""
        self.config = None
        
        label = tk.Label(self, text="Welcome to Tree Search")
        label.pack(padx=10, pady=10)
        
        self.file_list = tk.Listbox(self)
        self.file_list.pack(padx = 10, pady = 10)
        
        go_Back_Button = tk.Button(
            self,
            text="Go to home page",
            command=lambda: [controller.show_frame(MainPage), self.config.close()],
        )
        go_Back_Button.pack(side="bottom", fill=tk.X)
        
        leave_current_file = tk.Button(
            self,
            text="Leave Current file",
            command=lambda:  [self.go_back(), self.path_to_cwd_list()]
        )
        go_Back_Button.pack(side="bottom", fill=tk.X)
        
        
    def directory_display(self):
        self.config = find_or_create_config()
        self.working_path = self.library_path = self.config.read()
        self.config.close()
        self.path_to_cwd_list()
            
            
    def path_to_cwd_list(self):
        
        dr_list = os.listdir(self.working_path)
        
        self.file_list.delete(0, tk.END)
        
        for item in dr_list:
            self.file_list.insert(tk.END, item)
            
    def go_back(self):
        pass
        
    
        
        
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
    script_library_path = os.path.join(os.getcwd(), 'scriptLibrary')
    script_library_file_path = os.path.join(script_library_path, 'ScriptLibrary.txt')

    # Check if the script library directory exists
    if not os.path.exists(script_library_path):
        os.makedirs(script_library_path)

    # Check if the ScriptLibrary.txt file exists
    if not os.path.exists(script_library_file_path):
        with open(script_library_file_path, 'w') as configFile:
            # Write default content or leave it empty
            pass

    # Open the file in read mode
    configFile = open(script_library_file_path, 'r+')
    return configFile
        
        
        
if __name__ == "__main__":
    testObj = windows()
    testObj.mainloop()