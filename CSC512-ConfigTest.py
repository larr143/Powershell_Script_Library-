import os 
import fnmatch

def main():
    
    filtered_files = os.listdir("C:/Users/larry/OneDrive/Documents/ScriptLibrary")
        
    for i in filtered_files:
        if "." not in i:
            print(i)
        if ".py" in i:
            print(i)
        if ".txt" in i:
            print(i)
        
        #print(i, os.path.isdir(i))
        
    
    
if __name__ == "__main__":
    main()