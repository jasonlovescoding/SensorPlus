import tkinter as tk   
import tkinter.ttk as ttk
from PIL import Image, ImageTk

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.createWidgets()
    
    def createWidgets(self):
        self.canvas = tk.Canvas(self)
        self.backgroundImage = Image.open("./background/background.jpg")
        self.backgroundImage = self.backgroundImage.resize((630, 415), Image.ANTIALIAS)
        self.backgroundImage = ImageTk.PhotoImage(self.backgroundImage)
        self.backgroundLabel = tk.Label(self, image=self.backgroundImage)
        self.backgroundLabel.place(x = 0, y = 0, relwidth = 1, relheight = 1)    
        
        startButtonStyle = ttk.Style() # style of the buttons
        startButtonStyle.configure('start.TButton', font=('Verdana', 10),
                                  width = 28, justify = 'center')
              
        self.classifyButton = ttk.Button(self) # unaccompanied page button
        self.classifyButton["style"] = 'start.TButton'
        self.classifyButton["text"] = "Unaccompanied Practice"
        self.classifyButton["command"] = (lambda: 
                                    self.controller.showFrame("ClassifyPage"))   
        self.classifyButton.place(x = 378, y = 100)
            
        self.scoreButton = ttk.Button(self) # accompanied page button
        self.scoreButton["style"] = 'start.TButton'
        self.scoreButton["text"] = "Accompanied Practice"
        self.scoreButton["command"] = (lambda: 
                                    self.controller.showFrame("ScorePage"))
        self.scoreButton.place(x = 378, y = 150)
        
        self.logbookButton = ttk.Button(self) # history button
        self.logbookButton["style"] = 'start.TButton'
        self.logbookButton["text"] = "View History"
        self.logbookButton["command"] = (lambda: 
                                    self.controller.showFrame("LogbookPage"))
        self.logbookButton.place(x = 378, y = 200)
        
        self.userButton = ttk.Button(self) # user management button
        self.userButton["style"] = 'start.TButton'
        self.userButton["text"] = "User Management"
        self.userButton["command"] = (lambda: 
                                    self.controller.showFrame("UserPage")) 
        self.userButton.place(x = 378, y = 250)
        
        self.userButton = ttk.Button(self) # quit button
        self.userButton["style"] = 'start.TButton'
        self.userButton["text"] = "Quit"
        self.userButton["command"] = (lambda: self.controller.close()) 
        self.userButton.place(x = 378, y = 300)