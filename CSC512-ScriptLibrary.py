from ast import main
import os
import re
import subprocess
import tkinter as tk
import tkinter.messagebox
from tkinter import simpledialog, ttk, filedialog

class windows(tk.Tk):
    """windows Classmethod to handle windows .

    This class is the base frame that handles the containing and switching of 
    other frames. It also handles the styling of the main frame, including
    the menus options and dialogs. 

    Attributes:
        frames: A dictionary for containing tkinter frames.

    Args:
        tk ([tkinter]): [a reference to the root window of the Tkinter application]
    """
    def __init__(self, *args, **kwargs):
        """__init__ Initialize the Tk ."""
        tk.Tk.__init__(self, *args, **kwargs)
        self.frames = {}

        self.wm_title("Script Library")
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        for F in (MainPage, TreeSearch, LibraryCreatorOrLocator):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        self.menu_bar()
        self.show_frame(MainPage) 

    def menu_bar(self):
        """menu_bar called to create the menubar ar the top of the program"""
        
        menuBar = tk.Menu(self)
        self.fileMenu = tk.Menu(menuBar, tearoff=0)
        self.fileMenu.add_command(label="Open Library Location", command=self.open)
        self.fileMenu.add_command(label="Search For Script",
            command=self.frames[TreeSearch].user_search, state="disabled")
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label="Exit", command=self.quit)
        menuBar.add_cascade(label="File", menu=self.fileMenu)
        
        helpMenu = tk.Menu(menuBar, tearoff=0)
        helpMenu.add_command(label="Help Index",
            command=self.help_dialog)
        helpMenu.add_command(label="About...",
            command=self.about_dialog)
        menuBar.add_cascade(label="Help", menu=helpMenu)
        
        self.config(menu=menuBar)
    
    def help_dialog(self):
        """help_dialog Creates help dialog when called"""        
        message = """
        If you are having trouble using the search dialog enter words that are in the name of the script you 
        are looking for. The words are case sensitive. 
        If you are looking for Set_Execution_Policy.ps1. 
        Searches that will show this script: 
        1. Set
        2. Execution
        3. .ps1 - will return all scripts in library
        4. Set_Exe
        Searches that wont return this script:
        1. set
        2.execution
        3. set execution - you can't substitute underlines. 
        """
        
        tkinter.messagebox.showinfo("Help", message)
    
    def about_dialog(self):
        """about_dialog Creates about dialog when called"""        
        message = """
        This program creates a library on your computer at the location you choose. 
        The program also creates a config file where the program is stored that will point 
        the program to the library on startup. If you are looking to search for a script in the library 
        you can use the file menu for searching.  

        This program was written by Larry Tieken. 
        """
        
        tkinter.messagebox.showinfo("Help", message)
        
    def open(self):
        """opens file explorer at the library's location """
        config = self.find_or_create_config()
        path = config.read()
        os.system("explorer.exe " + path)   
        print(path) 
        
    def find_or_create_config(self):
        """find_or_create_config Finds the config file for the program and returns it.

        Returns:
            TextIOWrapper: The file that contains the config for the program.
        """
        
        script_library_path = os.path.join(os.getcwd(), 'scriptLibrary')
        script_library_file_path = os.path.join(script_library_path, 'ScriptLibrary.txt')

        # Check if the script library directory exists
        if not os.path.exists(script_library_path):
            os.makedirs(script_library_path)

        # Check if the ScriptLibrary.txt file exists
        if not os.path.exists(script_library_file_path):
            with open(script_library_file_path, 'w') as configFile:
                pass

        # Open the file in read mode
        configFile = open(script_library_file_path, 'r+')
        return configFile
    
    def show_frame(self, cont):
        """show_frame Raises desired container

        Args:
            cont (Container): Contains the container the program wants to display.
        """
        frame = self.frames[cont]
        if cont is MainPage: frame.what_to_display()
        if cont is TreeSearch: frame.directory_display()
        frame.tkraise()
        
class MainPage(tk.Frame):
    """MainPage 
    
    Fills the frame with either the main page to select the tree search or 
    send the user to config creation if there isn't one found in find_or_create_config.

    Attributes:
        config: A variable that contains the config file. 

    Args:
        tk ([tkinter]): [a reference to the root window of the Tkinter application]
    """
    def __init__(self, parent, controller):
        """__init__ Initialize the Tk ."""
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
    def clear_page(self):
        # Destroy all widgets inside the frame
        for widget in self.winfo_children():
            widget.destroy() 

    def what_to_display(self):
        """Decides whether the program is going to create a config or go to tree search."""
        self.clear_page()
        
        self.config = self.controller.find_or_create_config()
        
        self.label = tk.Label(self, text="Welcome To Your Script Library!", font=(20))
        self.label.grid(column=0, row=0, padx=2, pady=2)
        
        self.switch_to_Config_button = tk.Button(
            self,
            text="Change Library",
            command=lambda: [self.controller.show_frame(LibraryCreatorOrLocator), self.config.close()],
             font=(16)
        )
        self.switch_to_TreeSearch_button = tk.Button(
            self,
            text="Tree Script Search",
            command=lambda: [self.controller.show_frame(TreeSearch), self.config.close()],
            font=(16)
        )
        
        if self.config.read() == "":
            self.label.config(text= "Please click on the Find Library \n button to create or find your script library.")
            self.switch_to_Config_button.grid(column=0, row=1, padx=2, pady=2)
            self.switch_to_Config_button.config(text="Find or Create Library")
        else:
            self.switch_to_TreeSearch_button.grid(column=0, row=1, padx=2, pady=2)
        
        self.grid_rowconfigure([0,1], weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.page_style()

    def page_style(self):
        """Styles the container and widgets."""
        self.controller.geometry("400x400")
        
        style=ttk.Style(self)
        style.theme_use('alt')
        
        self.label.config(background='#141414',foreground="#F3B61F")
        self.switch_to_Config_button.config(foreground="#F3B61F", background='#252525', 
            width=20, height=5)
        self.switch_to_TreeSearch_button.config(foreground="#F3B61F",  background='#252525',
            width=20, height=5)
        
        self.configure(bg='#141414')

class LibraryCreatorOrLocator(tk.Frame):
    """LibraryCreatorOrLocator Allows the user to choose a location for the library and create a config.

    Attributes:
        path: A string that will contain the users chosen location for the library

    Args:
        tk ([tkinter]): [a reference to the root window of the Tkinter application]
    """
    def __init__(self, parent, controller):
        """__init__ Initialize the Tk ."""
        tk.Frame.__init__(self, parent)
        
        self.controller = controller
        self.path = ""
        
        self.controller.geometry("400x400")
        
        style=ttk.Style(self)
        style.theme_use('alt')
        
        self.label = tk.Label(self, text = "Please click on the browse button to find \n your script library or input desired location")
        self.label.config(background='#141414',foreground="#F3B61F")
        self.label.pack(padx=10, pady=10)
        
        self.browser = tk.Button(self, text="Browse", command=self.find_path)
        self.browser.pack(padx=10, pady=10)
        self.browser.config(foreground="#F3B61F", background='#252525', 
            width=20, height=5)    
        
        self.configure(bg='#141414')
    
    def find_path(self):
        """Attempts to find the path the user has given. """
        self.config = self.controller.find_or_create_config()
        self.path = filedialog.askdirectory()
        dirList = os.listdir(self.path)
        
        if "ScriptLibrary" in self.path:
            self.config.write(self.path)
            self.config.close()
            self.controller.show_frame(MainPage)
                
        elif "ScriptLibrary" in dirList:
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

class TreeSearch(tk.Frame):
    """TreeSearch _summary_

    Attributes:
        Library_path: A string that will contain the library path. 
        Working_path: A string that will contain the programs current working path
        config: A variable that will contain the TextIOWrapper for the config file.

    Args:
        tk ([tkinter]): [a reference to the root window of the Tkinter application]
    """
    def __init__(self, parent, controller):
        """__init__ Initialize the Tk ."""
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.library_path = ""
        self.working_path = ""
        self.config = None
               
    def window_fill(self, script_edit = False, path = None):
        """window_fill initializes all widgets of the TreeSearch Page.

        Args:
            script_edit (bool, optional): Changes the frame to allow user to edit script.   Defaults to False.
            path (_type_, optional): For editing the script at path if script edit is True. Defaults to None.
        """
        self.clear_page()
        self.controller.fileMenu.entryconfig("Search For Script",state='normal')
        
        if script_edit == False:
            self.label = tk.Label(self, text="Welcome to Tree Search")
            self.file_list = tk.Listbox(self)
            self.text_display = tk.Text(self, exportselection = False)
            self.script_description_display = tk.Text(self, exportselection = False)
        
            self.go_Back_Button = tk.Button(
                self, text="Go to home page",
                command=lambda: [self.controller.show_frame(MainPage), self.config.close()],
            )
            self.leave_current_file = tk.Button(
                self, text="Leave Current file",
                command=lambda:  self.path_to_cwd_list(go_back=True)
            )
            self.open_selected_file = tk.Button(
                self, text="Open Selected File",
                command=lambda:  self.path_to_cwd_list(
                    pathToJoin=self.file_list.get(self.file_list.curselection())
                    )
            )
            self.run_script = tk.Button(
                self, text="Run Script",
                command=lambda:  self.power_shell_display(self.file_list.curselection()[0], run=True)
            )
            
            self.file_scroll_Y = ttk.Scrollbar(self, command=self.file_list.yview)
            self.file_list['yscrollcommand'] = self.file_scroll_Y.set
            
            self.text_scroll_Y = ttk.Scrollbar(self, command=self.text_display.yview)
            self.text_display['yscrollcommand'] = self.text_scroll_Y.set
            
            self.script_scroll_Y = ttk.Scrollbar(self, 
                command=self.script_description_display.yview)
            self.script_description_display['yscrollcommand'] = self.script_scroll_Y.set
            
            
            self.text_scroll_X = ttk.Scrollbar(self, orient="horizontal",
                command=self.text_display.xview)
            self.text_display['xscrollcommand'] = self.text_scroll_X.set
            
            self.script_scroll_X = ttk.Scrollbar(self, orient="horizontal",
                command=self.script_description_display.xview)
            self.script_description_display['xscrollcommand'] = self.script_scroll_X.set
            
            
            self.label.grid(column=0, row=0, sticky="nsew", columnspan=4, pady=2, padx=2)
            
            self.file_list.grid(column=0, row=1, rowspan=4, sticky="nsew", pady=2, padx=2)
            self.file_scroll_Y.grid(column=1, row=1, rowspan=4, sticky="nsew")
            
            self.text_display.grid(column=2, row=1, sticky="nsew", pady=2, padx=2)
            self.text_scroll_Y.grid(column=3, row=1, sticky="nsew")
            self.text_scroll_X.grid(column=2, row=2, sticky="nsew")
            
            self.script_description_display.grid(column=2, row=3, sticky="nsew", pady=2, padx=2)
            self.script_scroll_Y.grid(column=3, row=3, sticky="nsew")
            self.script_scroll_X.grid(column=2, row=4, sticky="nsew")
            
            self.text_display.config(height=10)
            self.script_description_display.config(height=10)
            
            self.open_selected_file.grid(column=0, row=5, pady=2, padx=2)
            self.go_Back_Button.grid(column=2, row=5, pady=2, padx=2, sticky="e")
            self.leave_current_file.grid(column=2, row=5, sticky="w", pady=2, padx=2)
            self.run_script.grid(column=2, row=5, pady=2, padx=2)
            
            self.file_list.bind("<<ListboxSelect>>", self.show_content)
            
            self.window_style()
            
        if script_edit == True and os.path.exists(path): 
            
            self.script_edit_label = tk.Label(self, text="Please fill in at minimum the summary and author box.")
            
            self.synopsis_label = tk.Label(self, text="Summary:")
            self.description_label = tk.Label(self, text="Full description: ")
            self.notes_label = tk.Label(self, text="Author: ")
            self.extra_notes_label = tk.Label(self, text="Notes: ")
            
            self.synopsis_entry_box = tk.Text(self)
            self.description_entry_box = tk.Text(self)
            self.notes_entry_box = tk.Text(self)
            self.extra_notes_entry_box = tk.Text(self)
            
            self.done_button = tk.Button(
                self, text="Done",
                command=lambda:  self.script_comment_adder(path)
            )
            
            self.script_edit_label.grid(column=0 , row= 0, sticky="nsew", columnspan=2, padx= 2, pady =2)
            
            self.synopsis_label.grid(column=0, row=1, padx= 2, pady =2)
            self.description_label.grid(column=0, row=2, padx= 2, pady =2)
            self.notes_label.grid(column=0, row=3, padx= 2, pady =2)
            self.extra_notes_label.grid(column=0, row=4, padx= 2, pady =2)
            
            self.synopsis_entry_box.grid(column=1, row=1, padx= 2, pady =2)
            self.description_entry_box.grid(column=1, row=2, padx= 2, pady =2)
            self.notes_entry_box.grid(column=1, row=3, padx= 2, pady =2)
            self.extra_notes_entry_box.grid(column=1, row=4, padx= 2, pady =2)
            
            self.done_button.grid(column= 0, row=5, sticky="nsew", columnspan=2, padx=2, pady=7)
            
            self.window_style(True)
            
    def window_style(self, script_edit=None):
        """Styles the container and widgets.
        
        Args:
            script_edit (bool, optional): tells the program which version of the window to style.
        
        """
        if script_edit == None:
            self.controller.geometry("800x600")
            
            self.text_display.configure(font=("Consolas", 10), wrap=tk.NONE)
            self.script_description_display.configure(font=("Consolas", 10), wrap=tk.NONE)
            
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure([0,1,3], weight=1)
            
            self.label.config(background="#141414", foreground="#F3B61F", font=(14))
            
            self.file_list.config(background="#141414", foreground="#F3B61F")
            self.text_display.config(background="#141414", foreground="#F3B61F")
            self.script_description_display.config(background="#141414", foreground="#F26157")
            
            style=ttk.Style(self)
            style.theme_use('alt')
            style.configure("Vertical.TScrollbar", relief = 0,
                background="#8A4F7D", troughcolor = "#141414")
            style.configure("Horizontal.TScrollbar", relief = 0, 
                background="#8A4F7D", troughcolor = "#141414")
        
            self.configure(bg='#141414')
        
        elif script_edit == True:
            
            self.controller.geometry("450x650")
            
            self.script_edit_label.config(background="#1B1B1E",
                foreground="#F3B61F", font=(14))
            
            self.synopsis_label.config(background="#1B1B1E",
                foreground="#F3B61F",font=(12))
            self.description_label.config(background="#1B1B1E",
                foreground="#F3B61F",font=(12))
            self.notes_label.config(background="#1B1B1E",
                foreground="#F3B61F",font=(12))
            self.extra_notes_label.config(background="#1B1B1E",
                foreground="#F3B61F",font=(12))
            
            self.synopsis_entry_box.config(width= 40, height=6, font=("Consolas", 10), background="#1B1B1E", foreground="#F26157")
            self.description_entry_box.config(width= 40, height=6, font=("Consolas", 10), background="#1B1B1E", foreground="#F26157")
            self.notes_entry_box.config(width= 40, height=6, font=("Consolas", 10), background="#1B1B1E", foreground="#F26157")
            self.extra_notes_entry_box.config(width= 40, height=6, font=("Consolas", 10), background="#1B1B1E", foreground="#F26157")
            
            self.grid_columnconfigure(1, weight=1)
            
            self.configure(bg='#1B1B1E')
                   
    def script_comment_adder(self, path):
        """Takes the path of the script and displays contents on the page.
        
        When called the function will take the path of the script split it into 
        the comments on the script and the script itself. Insert the parts into their
        respective text boxes. 

        Args:
            path (Str): Path of the file to display.
        """
        readable_file = open(path, encoding='utf-8-sig' , mode="r")
        readable_file_contents = readable_file.read()
        
        #Checks for a multi line string in the script.
        if "<#" in readable_file_contents: 
                readable_file.close()
                writable_file = open(path, encoding='utf-8-sig' , mode="w+")
                readable_file_contents = readable_file_contents.split("<#")[0]
                writable_file.write(readable_file_contents)
                writable_file.close()
        else:
            readable_file.close()
        
        file = open(path, encoding='utf-8-sig' , mode="a")
        
        #creates comments with players input.
        if len(self.synopsis_entry_box.get('1.0', 'end-1c')) > 0 and len(self.notes_entry_box.get('1.0', 'end-1c')) > 0:
            
            synopsis = self.synopsis_entry_box.get('1.0', 'end-1c')
            description = self.description_entry_box.get('1.0', 'end-1c')
            author = self.notes_entry_box.get('1.0', 'end-1c')
            extra_notes = self.extra_notes_entry_box.get('1.0', 'end-1c')
            
            comment = ( "\n\n" + "<#" + "\n\n" + ".SYNOPSIS" + "\n" + "   " +
                synopsis + "\n\n" +  ".DESCRIPTION" + "\n" + "   " + description + 
                "\n\n" + ".NOTES" + "\n" + "Author: " + author + "\n" + 
                extra_notes + "\n\n" + "#>" 
            )
            
            file.write(comment)
            file.close()
            self.directory_display()
               
    def directory_display(self):
        """directory_display initializes the window building functions and configs.
        """
        self.window_fill()
        self.run_script["state"] = "disabled"
        self.in_search = False
        self.config = self.controller.find_or_create_config()
        self.working_path = self.library_path = self.config.read()
        self.config.close()
        self.path_to_cwd_list()
             
    def show_content(self, event):
        """show_content displays information on selected entry in list box.

        Args:
            event (<<listboxselect>>): tells function the user selected something.
        """
        #grabs file to display based on if the user is searching or not.
        x = self.file_list.curselection()[0]
        if self.in_search == False:
            file = os.path.join(self.working_path, self.file_list.get(x))
        elif self.in_search == True: 
            for i in self.dr_list:
                if self.file_list.get(x) in i:
                    file = i
                    break
            
        if ".txt" in file:
            with open(file) as file:
                file = file.read()
            self.run_script["state"] = "disabled"
            self.text_display.delete('1.0', tk.END)
            self.text_display.insert(tk.END, file)
            self.script_description_display.delete('1.0', tk.END)
        elif ".ps1" in file:
            self.power_shell_display(file, run=False)
            self.run_script["state"] = "normal"
        else: 
            self.run_script["state"] = "disabled"
            self.text_display.delete('1.0', tk.END)
            self.script_description_display.delete('1.0', tk.END)
            self.text_display.insert(tk.END, "This is a folder named: " + os.path.basename(file)) 
        
    def user_search(self):
        """user_search creates a simple dialog for searching through scripts.
        """
        self.in_search = False
        result = []
        input = simpledialog.askstring(title="Search Dialog",
            prompt="(Case sensitive) Name of script you are looking for:")
        
        for root, dirs, files in os.walk(self.library_path):
            for name in files:
                if input in name:
                    result.append(os.path.join(root, os.path.basename(name)))
        
        if len(result) > 0:
            self.in_search = True
            self.path_to_cwd_list(files_to_display=result)
        else:
            tkinter.messagebox.showinfo("Error", "Script was not found try again." )      
        
    def power_shell_display(self, path, run):
        """ Displays currently selected power shell and makes the user edit it if there isn't a comment.
        
        Args:
            path (Str): Contains the path to the script to either run or display. 
            run (Bool): A bool for either displaying or running passed script at path. 
        """
        if run == True:
            
            if self.in_search == False:
                path = os.path.join(self.working_path, self.file_list.get(path))
            elif self.in_search == True: 
                for i in self.dr_list:
                    if self.file_list.get(path) in i:
                        path = i
                        break

                        
            p = subprocess.Popen([
                "powershell.exe", "-File", f"""{path}"""
            ],stdout=subprocess.PIPE)

            output, err = p.communicate()
            
            self.text_display.delete('1.0', tk.END)
            self.text_display.insert(tk.END, "The selected Script ran! It terminated with this output: " + 
                str(output) + "\n\nerr: " + str(err) + 
                "\n\n (Note: if there is no output or an unintelligible output it most likely ran correctly)")
            
        if run == False:
            with open(path, encoding='utf-8-sig') as file:
                file = file.read()
            if "<#" and "#>" and ".SYNOPSIS" not in file: 
                tkinter.messagebox.showinfo(message="Script Issue, you are going to be redirected to a script editing page to add comments.", title="Script Error")
                self.window_fill(script_edit=True, path=path)
            else: 
                self.text_display.delete('1.0', tk.END)
                self.script_description_display.delete('1.0', tk.END)
                script = file.split("<#")
                self.text_display.insert(tk.END, script[0])
                
                # Define the patterns for each section
                synopsis_pattern = re.compile(r'\.SYNOPSIS(.*?)(\.|\#>)', re.DOTALL)
                description_pattern = re.compile(r'\.DESCRIPTION(.*?)(\.|\#>)', re.DOTALL)
                notes_pattern = re.compile(r'\.NOTES(.*?)(\.|\#>)', re.DOTALL)

                # Extract content for each section
                synopsis_match = synopsis_pattern.search(script[1])
                description_match = description_pattern.search(script[1])
                notes_match = notes_pattern.search(script[1])

                # Get the content from the matches
                synopsis_content = synopsis_match.group(1).strip() if synopsis_match else None
                description_content = description_match.group(1).strip() if description_match else None
                notes_content = notes_match.group(1).strip() if notes_match else None
                
                self.script_description_display.insert(tk.END, "Summary of script: \n" + synopsis_content + "\n\n" +
                    "Full description of script: \n" + description_content + "\n\n" + "Script notes: \n" + notes_content)               
    
    def path_to_cwd_list(self, files_to_display = None, pathToJoin = None, go_back = None):
        """path_to_cwd_list Populates the file list based on current working path

        Args:
            files_to_display (List[str], optional): A list containing paths for when users 
                search for scripts. Defaults to None.
            pathToJoin (Str, optional): A string that contains where 
                the user wants to go. Defaults to None.
            go_back (Bool, optional): A bool for if the user wants to 
                go back in the file structure . Defaults to None.
        """
        
        if go_back == True and self.in_search == False:
            if self.working_path != self.library_path:
                self.working_path = os.path.dirname(self.working_path)
        elif self.in_search == True and go_back == True:
            self.in_search = False
        
        if pathToJoin != None:
            self.working_path = os.path.join(self.working_path, pathToJoin)
        
        if files_to_display != None:
            self.dr_list = files_to_display
        else:
            self.dr_list = os.listdir(self.working_path)
        
        self.file_list.delete(0, tk.END)
        
        for item in self.dr_list:
            if ".txt" in item:
                self.file_list.insert(tk.END, os.path.basename(item))
            if "." not in item:
                self.file_list.insert(tk.END, os.path.basename(item))
            if ".ps1" in item:
                self.file_list.insert(tk.END, os.path.basename(item))
    
    def clear_page(self):
        # Destroy all widgets inside the frame
        for widget in self.winfo_children():
            widget.destroy() 
               
if __name__ == "__main__":
    testObj = windows()
    testObj.mainloop()