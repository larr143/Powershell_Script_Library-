from ast import Pass
from logging import captureWarnings
from operator import contains
from pydoc import synopsis
import tkinter as tk
from tkinter import DISABLED, ttk
import os 
import tkinter.messagebox
import re
import subprocess
import sys

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
        self.controller = controller
        self.library_path = ""
        self.working_path = ""
        self.config = None
    
        
    def window_fill(self, script_edit = False, path = None):
        
        self.clear_page()
        
        if script_edit == False:
            label = tk.Label(self, text="Welcome to Tree Search")
            self.file_list = tk.Listbox(self)
            self.text_display = tk.Text(self)
            self.script_description_display = tk.Text(self)
        
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
                    self.file_list.get(self.file_list.curselection())
                    )
            )
            self.run_script = tk.Button(
                self, text="Run Script",
                command=lambda:  self.power_shell_display(self.file_list.curselection()[0], run=True)
            )
            
            label.grid(column=0, row=0, sticky="nsew", columnspan=2, pady=2, padx=2)
            self.file_list.grid(column=0, row=1, rowspan=2, sticky="nsew", pady=2, padx=2)
            
            self.text_display.grid(column=1, row=1, sticky="nsew", pady=2, padx=2)
            self.script_description_display.grid(column=1, row=2, sticky="nsew", pady=2, padx=2)
            self.text_display.config(height=10)
            self.script_description_display.config(height=10)
            
            self.open_selected_file.grid(column=0, row=3, sticky="nsew", pady=2, padx=2)
            self.go_Back_Button.grid(column=1, row=3, pady=2, padx=2, sticky="e")
            self.leave_current_file.grid(column=1, row=3, sticky="w", pady=2, padx=2)
            self.run_script.grid(column=1, row=3, pady=2, padx=2)

            self.grid_rowconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=1)
            
            # self.text_display.configure(state="disabled")
            
            self.file_list.bind("<<ListboxSelect>>", self.show_content)
            
        if script_edit == True and os.path.exists(path): 
            
            self.script_edit_label = tk.Label(self, text="Please fill in at minimum the summary and author box.")
            
            synopsis_label = tk.Label(self, text="Summary:")
            description_label = tk.Label(self, text="Full description: ")
            notes_label = tk.Label(self, text="Author: ")
            extra_notes_label = tk.Label(self, text="Notes: ")
            
            self.synopsis_entry_box = tk.Text(self, width= 40, height=5)
            self.description_entry_box = tk.Text(self, width= 40, height=5)
            self.notes_entry_box = tk.Text(self, width= 40, height=5)
            self.extra_notes_entry_box = tk.Text(self, width= 40, height=5)
            
            done_button = tk.Button(
                self, text="Done",
                command=lambda:  self.script_comment_adder(path)
            )
            
            self.script_edit_label.grid(column=0 , row= 0, sticky="nsew", columnspan=2, padx= 2, pady =7)
            
            synopsis_label.grid(column=0, row=1, padx= 2, pady =5)
            description_label.grid(column=0, row=2, padx= 2, pady =5)
            notes_label.grid(column=0, row=3, padx= 2, pady =5)
            extra_notes_label.grid(column=0, row=4, padx= 2, pady =5)
            
            self.synopsis_entry_box.grid(column=1, row=1, padx= 2, pady =5)
            self.description_entry_box.grid(column=1, row=2, padx= 2, pady =5)
            self.notes_entry_box.grid(column=1, row=3, padx= 2, pady =5)
            self.extra_notes_entry_box.grid(column=1, row=4, padx= 2, pady =5)
            
            done_button.grid(column= 0, row=5, sticky="nsew", columnspan=2, padx=2, pady=7)
            
          
            
    def script_comment_adder(self, path):
        
        readable_file = open(path, encoding='utf-8-sig' , mode="r")
        readable_file_contents = readable_file.read()
        
        if "<#" in readable_file_contents: 
                readable_file.close()
                writable_file = open(path, encoding='utf-8-sig' , mode="w+")
                readable_file_contents = readable_file_contents.split("<#")[0]
                writable_file.write(readable_file_contents)
                writable_file.close()
        else:
            readable_file.close()
        
        file = open(path, encoding='utf-8-sig' , mode="a")
        
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
        self.window_fill()
        self.run_script["state"] = "disabled"
        self.config = find_or_create_config()
        self.working_path = self.library_path = self.config.read()
        self.config.close()
        self.path_to_cwd_list()
        
       
        
    def show_content(self, event):
        
        try:
            x = self.file_list.curselection()[0]
            file = os.path.join(self.working_path, self.file_list.get(x))
            
            if ".txt" in file:
                with open(file) as file:
                    file = file.read()
                self.run_script["state"] = "disabled"
                self.text_display.delete('1.0', tk.END)
                self.text_display.insert(tk.END, file)
            elif ".ps1" in file:
                self.power_shell_display(file, run=False)
                self.run_script["state"] = "normal"
            else: 
                self.run_script["state"] = "disabled"
                self.text_display.delete('1.0', tk.END)
                self.text_display.insert(tk.END, "This is a folder named: " + os.path.basename(file)) 
            
        except: IndexError
            # need to fix 
            
            
    def power_shell_display(self, path, run = True):
        
        if run == True:
            path = os.path.join(self.working_path, self.file_list.get(path)) 
            
            p = subprocess.Popen(
            [
                "powershell.exe", 
                "-noprofile", "-c",
                r""" exit (Start-Process -Verb RunAs -PassThru -Wait powershell.exe -Args "
                        -noprofile -c Set-Location \`"$PWD\`"; & {path}; exit `$LASTEXITCODE
                    "
                ).ExitCode
                """.format(path=path)
            ],
            stdout=sys.stdout
            )
            p.communicate()
            
            self.text_display.delete('1.0', tk.END)
            self.text_display.insert(tk.END, "The selected Script ran! It terminated with exit code: " + str(p.returncode))
            
        if run == False:
            with open(path, encoding='utf-8-sig') as file:
                file = file.read()
            if "<#" and "#>" and ".SYNOPSIS" not in file:
                tkinter.messagebox.showinfo("Script Issue, you are going to be redirected to a script editing page to add comments.")
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
        
                 
    
    def path_to_cwd_list(self, pathToJoin = None, go_back = None):
        
        if go_back == True:
            self.working_path = os.path.dirname(self.working_path)
        
        if pathToJoin != None:
            self.working_path = os.path.join(self.working_path, pathToJoin)
        
        dr_list = os.listdir(self.working_path)
        
        self.file_list.delete(0, tk.END)
        
        for item in dr_list:
            if ".txt" in item:
                self.file_list.insert(tk.END, item)
            if "." not in item:
                self.file_list.insert(tk.END, item)
            if ".ps1" in item:
                self.file_list.insert(tk.END, item)
    
    def clear_page(self):
        # Destroy all widgets inside the frame
        for widget in self.winfo_children():
            widget.destroy() 
    
        
        
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