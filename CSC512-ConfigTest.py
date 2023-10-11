import os 

def main():
    #creating the library for the user or finding current library 
    dirList = os.listdir()
    
    if 'scriptLibrary' in dirList:
        dirList = os.listdir(os.path.join(os.getcwd() + '/scriptLibrary'))
        
        if 'ScriptLibrary.txt' in dirList:
            configFile = open((os.path.join(os.getcwd() + '/scriptLibrary' + "/ScriptLibrary.txt")), "w+")
        
        else:
            cwd = os.getcwd()
            path = os.path.join(cwd, "scriptLibrary", 'ScriptLibrary.txt')
            configFile = open(path, 'x')
            
    else:
        cwd = os.getcwd()
        path = os.path.join(cwd, "scriptLibrary")
        os.makedirs(path)
        dirList = os.listdir(os.path.join(os.getcwd() + '/scriptLibrary'))
        
        if 'ScriptLibrary.txt' in dirList:
            configFile = open((os.path.join(os.getcwd() + '/scriptLibrary' + "/ScriptLibrary.txt")), "w+")

        else:
            cwd = os.getcwd()
            path = os.path.join(cwd, "scriptLibrary", 'ScriptLibrary.txt')
            configFile = open(path, 'x')
        

    configFile.write('hi')
    configFile.close()
        
    
    
if __name__ == "__main__":
    main()