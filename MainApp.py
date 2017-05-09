exec(open('StartPage.py', 'r').read())
exec(open('ClassifyPage.py', 'r').read())
exec(open('ScorePage.py', 'r').read())
exec(open('LogbookPage.py', 'r').read())
exec(open('UserPage.py', 'r').read())

import tkinter as tk   
import tkinter.ttk as ttk
from tkinter import messagebox

class MainApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("SensorPlus") 
        self.resizable(width=False, height=False)
        self.user = 'Admin'
        self.createMenu()
        self.initializeContainer()
        self.showFrame("StartPage") # initialize with the startpage
        

    def createMenu(self):
        menubar = tk.Menu(self)  
        settingmenu = tk.Menu(menubar, tearoff=0)
        settingmenu.add_command(label="About Us", command=self.aboutUs)
        menubar.add_cascade(label="More", menu = settingmenu)  
        self.config(menu = menubar)
    
    def initializeContainer(self):
        container = tk.Frame(self) # configure the container
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)
     
        self.frames = {} # stack the pages
        self.currentPage = 'StartPage'
        for F in (StartPage, ClassifyPage, ScorePage, LogbookPage, UserPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row = 0, column = 0, sticky="nsew")
            frame.grid_rowconfigure(1, weight = 1)
            frame.grid_columnconfigure(1, weight = 1)
            
    def showFrame(self, pageName): # switch to another page   
        frame = self.frames[pageName]     
        if pageName == 'StartPage':
            self.geometry("630x415")           
            if (self.currentPage == 'ClassifyPage' or   
                self.currentPage == 'ScorePage'): 
                # clear the remaining update process
                currentFrame = self.frames[self.currentPage] 
                if currentFrame.updateConnectedProcess is not None:
                    currentFrame.after_cancel(currentFrame.updateConnectedProcess)
        elif pageName == 'ClassifyPage':
            self.frames['ClassifyPage'].updateConnect()
            self.frames['ClassifyPage'].refreshUser()
        elif pageName == 'ScorePage':  
            self.frames['ScorePage'].updateConnect()
            self.frames['ScorePage'].refreshUser()
        elif pageName == 'LogbookPage':  
            self.frames['LogbookPage'].refreshData()
        #elif pageName == 'UserPage':
            #self.geometry("240x360")              
        self.currentPage = pageName
        frame.tkraise() 
            
    def aboutUs(self): # info about us
        messagebox.showinfo("Team Info", "Teamed up with my roommates & buddies.\nManager: Zhu Feng\nDeveloper: Zhang Qianhao, Gao Wei\nData: Nie Lei, Chen Dengbo\n ")   
        
    def close(self):
        self.destroy()
            
if __name__ == "__main__":
    app = MainApp()
    app.mainloop()