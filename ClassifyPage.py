exec(open('ClassifyAlg.py', 'r').read())
import os, time
import tkinter as tk   
import tkinter.ttk as ttk
import subprocess, threading
from PIL import Image, ImageTk

class ClassifyPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recordDict = {}
        self.feedbackLog = {}
        self.createWidgets()

    def createWidgets(self):
        self.canvas = tk.Canvas(self)
        self.backgroundImage = Image.open("./background/background2.jpg")
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
        self.activityLabel.place(x = 384, y = 25)
        
        # user text
        self.userText = tk.Text(self, height = 1, 
                                    width = 18, font=('Helvetica', 10))
        self.userText.insert(tk.END, self.controller.user)
        self.userText['state'] = 'disabled'
        self.userText.place(x = 470, y = 25)
        
        # row 1: activity label and combobox
        # activity label
        self.activityLabel = tk.Label(self, text = "Activity:", 
                                          font = ('helvetica', 10),
                                      fg = 'white', bg = '#454545')
        self.activityLabel.place(x = 380, y = 55)
        
        # activity combobox
        self.activity = tk.StringVar()
        self.activities = ['Punch', 'Shove']
        self.activity.set(self.activities[0])
        self.activityBox = ttk.Combobox(self, height = 12, width = 16)  
        self.activityBox['textvariable'] = self.activity
        self.activityBox['values'] = self.activities
        self.activityBox.place(x = 470, y = 55)
        self.activity.trace_variable('w', self.updateTreeview)       
        for each in self.activities: # create the record log and feedback log
            self.recordDict[each] = []
            self.feedbackLog[each] = []

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
        self.myo1connectCheckbutton.place(x = 380, y = 83)
        
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
        self.myo2connectCheckbutton.place(x = 545, y = 83)
        
        # row 3: start button and stop button
        # start button
        self.startButton = ttk.Button(self, text="start", command = self.startCapture)
        self.startButton['style'] = 'main.TButton' 
        self.startButton['state'] = 'disabled'     
        self.startButton.place(x = 370, y = 112)
        
        # stop button
        self.stopButton = ttk.Button(self, text="stop", command = self.stopCapture)
        self.stopButton['style'] = 'main.TButton' 
        self.stopButton['state'] = 'disabled'
        self.stopButton.place(x = 500, y = 112)
        
        # data frame
        self.dataFrame = tk.Frame(self)
        self.dataFrame.place(x = 10, y = 133)
        # row 4: classification display tree       
        classifications = ('Time Stamp', 'Type', 'Oops', 'Fair', 'Great')
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
        self.classificationTree.column('Oops', width = 45, anchor = 'center') 
        self.classificationTree.heading('Oops', text = 'Oops') 
        self.classificationTree.column('Fair', width = 42, anchor = 'center') 
        self.classificationTree.heading('Fair', text = 'Fair') 
        self.classificationTree.column('Great', width = 45, anchor = 'center') 
        self.classificationTree.heading('Great', text = 'Great') 
        self.classificationTree.pack()
        self.classificationTree.bind("<Double-1>", self.updateFeedback)
               
        # feedback  
        self.feedbackFrame = ttk.LabelFrame(self, text="Feedback", height = 200,
                                            width = 100)
        s = ttk.Style()
        s.configure('classify.TLabelframe.Label', font=('Helvetica', 10, 'bold'))
        s.configure('classify.TLabelframe.Label', foreground ='black')
        self.feedbackFrame['style'] = "classify.TLabelframe"
        self.feedbackFrame.place(x = 355, y= 145)
        self.feedbackText = tk.Text(self.feedbackFrame, height = 12, 
                                    width = 36, font=('Helvetica', 10),
                                    state = 'disabled')        
        self.feedbackText.pack()

        # bottom row: back button and clear button
        # back button
        self.backButton = ttk.Button(self, text="< back",
                    command = lambda: self.storeAndReturn())
        self.backButton['style'] = 'main.TButton'              
        self.backButton.place(x = 10, y = 375)
        
        # delete button
        self.clearButton = ttk.Button(self, text="delete",
                                          command = self.deleteItem)
        self.clearButton['style'] = 'main.TButton'              
        self.clearButton.place(x = 370, y = 375)
        #clear button
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
        # MAYTODO: use returncode to decide whether to run the classification
        returncode = self.activityCaptureProcess.wait()
        self.startButton['state'] = 'active'
        self.stopButton['state'] = 'disabled'
        self.classify()
        
    def stopCapture(self): # compulsorily terminate the capture
        self.activityCaptureProcess.kill()
                           
    def classify(self): # classify the activity quality and keep the record
        localTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        activityName = self.activity.get()
        localTime = localTime[2:]
        activityClass, activityType, feedback = classifyAlg(activityName, self.logWriter)
        record = [localTime, activityType, '', '', '']
        record[activityClass+1] = 'X'
        self.classificationTree.insert('', 0, values = record)  
        self.feedbackText['state'] = 'normal'
        self.feedbackText.delete(1.0, tk.END)
        self.feedbackText.insert(tk.END, feedback)
        self.feedbackText['state'] = 'disabled'
        # keep the record
        self.recordDict[activityName].append(record)
        self.feedbackLog[activityName].append(feedback)       
        
    def deleteItem(self):
        activityName = self.activity.get()
        # get selected item
        for selectedItem in self.classificationTree.selection(): 
            idx = self.classificationTree.index(selectedItem)
            self.recordDict[activityName].pop(-1-idx)
            self.feedbackLog[activityName].pop(-1-idx)
            self.classificationTree.delete(selectedItem)
            
    def clearTreeview(self):
        # clear the entire treeview and the feedback log
        activityName = self.activity.get()
        self.classificationTree.delete(*self.classificationTree.get_children())
        self.recordDict[activityName][:] = []
        self.feedbackLog[activityName][:] = []
        self.feedbackText['state'] = 'normal'
        self.feedbackText.delete(1.0, tk.END)
        self.feedbackText['state'] = 'disabled'
        
    def updateTreeview(self, *ignore): 
        # update the treeview and the feedback box with a new activity
        # the strange dummys are required for tracing, otherwise it won't compile
        activityName = self.activity.get()
        self.classificationTree.delete(*self.classificationTree.get_children())
        for each in self.recordDict[activityName]:
            self.classificationTree.insert('', 0, values = each)
        self.feedbackText['state'] = 'normal'
        self.feedbackText.delete(1.0, tk.END)
        self.feedbackText['state'] = 'disabled'
        
    def updateFeedback(self, event):
        ''' Executed when a row is double-clicked'''   
        # what row and column was clicked on
        row = self.classificationTree.identify_row(event.y)
        column = self.classificationTree.identify_column(event.x)
        # get column position info
        try:
            x, y, width, height = self.classificationTree.bbox(row, column)
        except: # clicked on invalid space
            return
        # update the text
        activity = self.activity.get()
        idx = - self.classificationTree.index(row) - 1
        feedback = self.feedbackLog[activity][idx]
        self.feedbackText['state'] = 'normal'
        self.feedbackText.delete(1.0, tk.END)
        self.feedbackText.insert(tk.END, feedback)
        self.feedbackText['state'] = 'disabled'

    def storeAndReturn(self):
        # write the history for this user
        self.logWriter = open('./history/{}+{}.txt'.format(
                              self.controller.user, self.activity.get()), 'a')
        for eachActivity in self.activities:
            for record, feedback in \
                list(zip(self.recordDict[eachActivity], self.feedbackLog[eachActivity])):
                self.logWriter.write(str(record)+'\n')
                self.logWriter.write(str(feedback)+'\n')                     
        self.logWriter.close()
        self.controller.showFrame("StartPage") 
    
    def refreshUser(self):
        self.userText['state'] = 'normal'
        self.userText.delete(1.0, tk.END)
        self.userText.insert(tk.END, self.controller.user)
        self.userText['state'] = 'disabled'