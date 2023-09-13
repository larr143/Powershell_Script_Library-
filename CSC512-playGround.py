import psutil


def main(): 
    boolean = ("chrome.deb" in (i.name() for i in psutil.process_iter()))
    print(boolean)
    
if __name__ == "__main__":
    main()