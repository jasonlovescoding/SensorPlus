exec(open('ModifiableEntry.py', 'r').read())
exec(open('ScoreAlg.py', 'r').read())
exec(open('ModelTrainer.py', 'r').read())
exec(open('ImageGenerator.py', 'r').read())

import os, time
import tkinter as tk   
import tkinter.ttk as ttk
import subprocess, threading
from PIL import Image, ImageTk

class ScorePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recordDict = {}
        self.createWidgets()

    def createWidgets(self):
        self.canvas = tk.Canvas(self)
        self.backgroundImage = Image.open("./background/background3.jpg")
        self.backgroundImage = self.backgroundImage.resize((630, 415), Image.ANTIALIAS)
        self.backgroundImage = ImageTk.PhotoImage(self.backgroundImage)
        self.backgroundLabel = tk.Label(self, image=self.backgroundImage)
        self.backgroundLabel.place(x = 0, y = 0, relwidth = 1, relheight = 1)
        
        classifyButtonStyle = ttk.Style() # style of the buttons
        classifyButtonStyle.configure('main.TButton', font=('Helvetica', 10),
                                  width = 1, fg = 'white', bg = '#454545')
        
        # user label
        self.activityLabel = tk.Label(self, text = "User:", 
                                          font = ('helvetica', 10),
                                      fg = 'white', bg = '#454545')
        self.activityLabel.place(x = 384, y = 22)
        
        # user text
        self.userText = tk.Text(self, height = 1, 
                                    width = 15, font=('Helvetica', 10))
        self.userText.insert(tk.END, self.controller.user)
        self.userText['state'] = 'disabled'
        self.userText.place(x = 470, y = 22)
        
        # row 1: activity label and combobox
        # activity label
        self.activityLabel = tk.Label(self, text = "Activity:", 
                                          font = ('helvetica', 10),
                                      fg = 'white', bg = '#454545')
        self.activityLabel.place(x = 380, y = 51)
        
        # activity combobox
        self.activity = tk.StringVar()
        self.activities = ['Punch', 'Shove']
        self.activity.set(self.activities[0])
        self.activityBox = ttk.Combobox(self, height = 12, width = 16)  
        self.activityBox['textvariable'] = self.activity
        self.activityBox['values'] = self.activities
        self.activityBox.place(x = 470, y = 51)
        self.activity.trace_variable('w', self.updateTreeview)       
        for each in self.activities: # create the record log and feedback log
            self.recordDict[each] = []

        # row 2: myo1 connection checkbutton and myo2 connection checkbutton
        # myo1 connection checkbutton
        self.myo1connect = tk.IntVar()
        self.myo1connectCheckbutton = tk.Checkbutton(self)
        self.myo1connectCheckbutton['text'] = 'myo1'
        self.myo1connectCheckbutton['variable'] = self.myo1connect
        self.myo1connectCheckbutton['state'] = 'disabled'
        self.myo1connectCheckbutton['bg'] = '#4C4C4C'
        self.myo1connectCheckbutton['disabledforeground'] = 'white'
        self.myo1connectCheckbutton['foreground'] = 'white'
        self.myo1connectCheckbutton['bd'] = 0
        self.myo1connectCheckbutton.place(x = 380, y = 78)
        
        # myo2 connection checkbutton
        self.myo2connect = tk.IntVar()
        self.myo2connectCheckbutton = tk.Checkbutton(self)
        self.myo2connectCheckbutton['text'] = 'myo2'
        self.myo2connectCheckbutton['variable'] = self.myo2connect
        self.myo2connectCheckbutton['state'] = 'disabled'
        self.myo2connectCheckbutton['bg'] = '#141615'
        self.myo2connectCheckbutton['disabledforeground'] = 'white'
        self.myo2connectCheckbutton['foreground'] = 'white'
        self.myo2connectCheckbutton['bd'] = 0
        self.myo2connectCheckbutton.place(x = 545, y = 78)
        
        # row 3: start button and stop button
        # start button
        self.startButton = ttk.Button(self, text="start", command = self.startCapture)
        self.startButton['style'] = 'main.TButton' 
        self.startButton['state'] = 'disabled'     
        self.startButton.place(x = 370, y = 105)
        
        # stop button
        self.stopButton = ttk.Button(self, text="stop", command = self.stopCapture)
        self.stopButton['style'] = 'main.TButton' 
        self.stopButton['state'] = 'disabled'
        self.stopButton.place(x = 500, y = 105)
        
        # data frame
        self.dataFrame = tk.Frame(self)
        self.dataFrame.place(x = 345, y = 138)
        # row 4: classification display tree       
        classifications = ('Time Stamp', 'Type', 'Score')
        self.classificationTree = ttk.Treeview(self.dataFrame, 
                                               columns = classifications,
                                               height = 10)
        # hide the first column
        self.classificationTree['show'] = 'headings' 
        # configurate the columns
        self.classificationTree.column('Time Stamp', width = 120, anchor = 'center') 
        self.classificationTree.heading('Time Stamp', text = 'Time Stamp') 
        self.classificationTree.column('Type', width = 70, anchor = 'center') 
        self.classificationTree.heading('Type', text = 'Type') 
        self.classificationTree.column('Score', width = 80, anchor = 'center') 
        self.classificationTree.heading('Score', text = 'Score (*/10)') 
        self.classificationTree.pack()
        self.classificationTree.bind("<Double-1>", self.updateStats)
        
        # activity stats
        s = ttk.Style()
        s.configure('score.TLabelframe.Label', font=('Helvetica', 10, 'bold'))
        s.configure('score.TLabelframe.Label', foreground ='black')

        self.statsFrame = ttk.LabelFrame(self, text="Statistics", 
                                              height = 260, width = 200)
        self.statsFrame['style'] = 'score.TLabelframe'
        self.statsFrame.place(x = 15, y= 135)
        self.image= Image.open("./background/blankdata.jpg")
        self.image = self.image.resize((300, 200), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)        
        self.imageButton = ttk.Button(self.statsFrame)
        self.imageButton.image = self.image
        self.imageButton.configure(image=self.image)
        self.imageButton.pack()

        
        # bottom row: back button and clear button
        # back button
        self.backButton = ttk.Button(self, text="< back",
                    command = lambda: self.trainAndReturn())
        self.backButton['style'] = 'main.TButton'              
        self.backButton.place(x = 10, y = 375)
        
        # delete button
        self.clearButton = ttk.Button(self, text="delete",
                                          command = self.deleteItem)
        self.clearButton['style'] = 'main.TButton'              
        self.clearButton.place(x = 370, y = 375)
        
        # clear button
        self.clearButton = ttk.Button(self, text="clear",
                                          command = self.clearTreeview)
        self.clearButton['style'] = 'main.TButton'              
        self.clearButton.place(x = 500, y = 375)
        
    def updateConnect(self): # update the connection status
        status = os.system('CheckConnection.exe') 
        if status == 3: # both connected
            self.myo1connect.set(1)
            self.myo2connect.set(1)
            self.startButton['state'] = 'active' 
        elif status == 2: # myo2 connected
            self.myo1connect.set(0)
            self.myo2connect.set(1)
            self.startButton['state'] = 'active' 
        elif status == 1: # myo1 connected
            self.myo1connect.set(1)
            self.myo2connect.set(0)
            self.startButton['state'] = 'active' 
        else: # none connected
            self.myo1connect.set(0)
            self.myo2connect.set(0)
            self.startButton['state'] = 'active' 
            #self.startButton['state'] = 'disabled'    
        # check the connection every 5s
        self.updateConnectedProcess = self.after(100000, self.updateConnect)
        
    def startCapture(self): # start the activity capture and recording
        self.startButton['state'] = 'disabled'
        self.stopButton['state'] = 'active'
        self.activityCaptureThread = threading.Thread(target = 
                                                      self.activityCapture)
        # terminate subprocesses in the end
        self.activityCaptureThread.daemon = True
        # set as a thread 
        self.activityCaptureThread.start()
        
    def activityCapture(self):
        # the recorder
        self.logWriter = open('./data/~record.txt', 'w+')
        # set a subprocess for the activity capturer
        self.activityCaptureProcess = subprocess.Popen('CaptureActivity.exe', 
                                                       stdout = self.logWriter)
        # MAYTODO: use returncode to decide whether to run the scoring
        returncode = self.activityCaptureProcess.wait()
        self.startButton['state'] = 'active'
        self.stopButton['state'] = 'disabled'        
        self.score()
        
    def stopCapture(self): # compulsorily terminate the capture
        self.activityCaptureProcess.kill()
                           
    def score(self): # score the activity quality and keep the record
        localTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        localTime = localTime[2:]
        activityName = self.activity.get()
        activityScore, activityType = scoreAlg(activityName, self.logWriter)
        record = [localTime, activityType, activityScore]
        self.classificationTree.insert('', 0, values = record)        
        # keep the record
        self.recordDict[activityName].append(record)
        
        # change the time to avoid illegal chars 
        localTime = localTime.replace(':', '%')
        # make the image
        imageName = '{}+{}+{}+{}.jpg'.format(
                 self.controller.user, localTime, activityName, activityType)
        os.chdir(".\\img")   
        generateImage(self.logWriter, imageName)
        # generate the correct name to extract the correct image
        self.image = Image.open(imageName)
        self.image = self.image.resize((300, 200), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)
        self.imageButton.image = self.image
        self.imageButton.configure(image=self.image)
        self.imageButton.grid(row = 5, column = 0, columnspan = 2)
        os.chdir("..")        
                           
        # store the file
        self.logWriter.close()
        os.chdir(".\\data")    
        os.rename('~record.txt', '{}+{}+{}+{}.txt'.format(
                 self.controller.user, localTime, activityName, activityType))
        os.chdir("..")
        
    def deleteItem(self):
        # get selected item
        for selectedItem in self.classificationTree.selection():
            localTime, activityType, activityScore = \
                        self.classificationTree.item(selectedItem)['values']
            # delete the record
            localTime = localTime.replace(':', '%')
            statsName = './data/{}+{}+{}+{}.txt'.format(
                                          self.controller.user, localTime, 
                                          self.activity.get(), activityType)           
            self.classificationTree.delete(selectedItem)
            os.remove(statsName)
        
    def clearTreeview(self):
        # delete the records
        for eachActivity in self.activities:
            for localTime, activityType, activityScore in self.recordDict[eachActivity]:
                localTime = localTime.replace(':', '%')
                statsName = './data/{}+{}+{}+{}.txt'.format(
                                      self.controller.user, localTime, 
                                      eachActivity, activityType)
                os.remove(statsName)
        # clear the entire treeview and the feedback log
        activityName = self.activity.get()
        self.classificationTree.delete(*self.classificationTree.get_children())
        self.recordDict[activityName][:] = []
            
    def updateTreeview(self, *ignore): 
        # update the treeview and the feedback box with a new activity
        # the strange dummys are required for tracing, otherwise it won't compile
        activityName = self.activity.get()
        self.classificationTree.delete(*self.classificationTree.get_children())
        for each in self.recordDict[activityName]:
            self.classificationTree.insert('', 0, values = each)
    
    def updateImage(self, event):
        # generate the correct name to extract the correct image
        record = self.classificationTree.focus()
        activityName = self.activity.get()
        localTime, activityType, activityScore = self.classificationTree.item(record)['values']
        localTime = localTime.replace(':', '%')
        imageName = '{}+{}+{}+{}.jpg'.format(
                 self.controller.user, localTime, activityName, activityType)
        os.chdir('.\\img')
        self.image = Image.open(imageName)
        self.image = self.image.resize((300, 200), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(self.image)
        self.imageButton.image = self.image
        self.imageButton.configure(image=self.image)
        self.imageButton.pack() 
        os.chdir('..')
            
    def updateStats(self, event):        
        ''' Executed, when a row is double-clicked. Opens 
        read-only EntryPopup above the item's column, so it is possible
        to select text '''   
        # close previous entries
        if hasattr(self, 'modifyEntry'):
            self.modifyEntry.close()   
        # what row and column was clicked on
        row = self.classificationTree.identify_row(event.y)
        column = self.classificationTree.identify_column(event.x)
        # get column position info
        try:
            x, y, width, height = self.classificationTree.bbox(row, column)
        except: # clicked on invalid space
            return
        self.updateImage(event)
        # cannot modify anything other than the score column
        if column != '#3':
            return
        # y-axis offset
        pady = height // 2   
        # place Entry popup properly         
        localTime, activityType, activityScore = self.classificationTree.item(row)['values']
        localTime = localTime.replace(':', '%')
        statsName = './data/{}+{}+{}+{}.txt'.format(
                                      self.controller.user, localTime, 
                                      self.activity.get(), activityType)
        self.modifyEntry = ModifiableEntry(self.classificationTree, row, column, 
                                           statsName)
        self.modifyEntry.place( x=x, y=y+pady, anchor='w')
    
    def trainAndReturn(self):
        ''' when exiting this page, we store the current data 
        and train the model '''
        statsList = []
        for eachActivity in self.activities:
            for localTime, activityType, activityScore in self.recordDict[eachActivity]:
                localTime = localTime.replace(':', '%')
                statsName = './data/{}+{}+{}+{}.txt'.format(
                                      self.controller.user, localTime, 
                                      eachActivity, activityType)
                statsList.append(statsName)
        self.trainThread = threading.Thread(target = trainModel(statsList))
        self.trainThread.start()
        self.controller.showFrame("StartPage") 
        
    def refreshUser(self):
        self.userText['state'] = 'normal'
        self.userText.delete(1.0, tk.END)
        self.userText.insert(tk.END, self.controller.user)
        self.userText['state'] = 'disabled'