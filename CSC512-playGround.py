import tkinter as tk


def main(): 
    root = tk.Tk()
    root.title("Script Library")
    root.minsize(300, 300)
    root.geometry("300x300+50+50")

    
    openingLabel = tk.Label(root,text = "Welcome to your Script Library")
    openingLabel.place(y=(root.winfo_height()/3), x=(root.winfo_width()/3))    
    
    button = tk.Button(root,text ="click me")
    button.place(y=(root.winfo_height()/2), x=(root.winfo_width()/2))
    

    root.mainloop()
    

if __name__ == "__main__":
    main()