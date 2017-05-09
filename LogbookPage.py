import tkinter as tk
import tkinter.ttk as ttk
import time
class LogbookPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.recordDict = {}
        self.feedbackLog = {}
        self.createWidgets()

    def createWidgets(self):
        self.canvas = tk.Canvas(self)
        self.backgroundImage = Image.open("./background/background.jpg")
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
                                      fg = 'white', bg = '#191A1C')
        self.activityLabel.place(x = 420, y = 35)
        
        # user text
        self.userText = tk.Text(self, height = 1, 
                                    width = 15, font=('Helvetica', 10))
        self.userText.insert(tk.END, self.controller.user)
        self.userText['state'] = 'disabled'
        self.userText.place(x = 490, y = 35)
        
        # activity label and combobox
        # activity label
        self.activityLabel = tk.Label(self, text = "Activity:", 
                                          font = ('helvetica', 10),
                                      fg = 'white', bg = '#191A1C')
        self.activityLabel.place(x = 420, y = 65)
        
        # activity combobox
        self.activity = tk.StringVar()
        self.activities = ['Punch', 'Shove']
        self.activity.set(self.activities[0])
        self.activityBox = ttk.Combobox(self, height = 12, width = 16)  
        self.activityBox['textvariable'] = self.activity
        self.activityBox['values'] = self.activities
        self.activityBox.place(x = 490, y = 65)
        self.activity.trace_variable('w', self.updateTreeview)       
        for each in self.activities: # create the record log and feedback log
            self.recordDict[each] = []
            self.feedbackLog[each] = []

        # data frame
        self.dataFrame = tk.Frame(self)
        self.dataFrame.place(x = 287, y = 100)
        # row 4: classification display tree       
        classifications = ('Time Stamp', 'Type', 'Oops', 'Fair', 'Great')
        self.classificationTree = ttk.Treeview(self.dataFrame, 
                                               columns = classifications,
                                               height = 12)
        # hide the first column
        self.classificationTree['show'] = 'headings' 
        # configurate the columns
        self.classificationTree.column('Time Stamp', width = 120, anchor = 'center') 
        self.classificationTree.heading('Time Stamp', text = 'Time Stamp') 
        self.classificationTree.column('Type', width = 70, anchor = 'center') 
        self.classificationTree.heading('Type', text = 'Type') 
        self.classificationTree.column('Oops', width = 45, anchor = 'center') 
        self.classificationTree.heading('Oops', text = 'Oops') 
        self.classificationTree.column('Fair', width = 37, anchor = 'center') 
        self.classificationTree.heading('Fair', text = 'Fair') 
        self.classificationTree.column('Great', width = 45, anchor = 'center') 
        self.classificationTree.heading('Great', text = 'Great')        
        self.classificationTree.bind("<Double-1>", self.updateFeedback)
        # scrollbar
        scrollbar = ttk.Scrollbar(self.dataFrame)
        scrollbar.config(command = self.classificationTree.yview)
        self.classificationTree.configure(yscrollcommand = scrollbar.set)
        scrollbar.pack( side = 'right', fill='y' )
        self.classificationTree.pack()
        
        # feedback  
        self.feedbackFrame = ttk.LabelFrame(self, text="Feedback", height = 200,
                                            width = 100)
        s = ttk.Style()
        s.configure('classify.TLabelframe.Label', font=('Helvetica', 10, 'bold'))
        s.configure('classify.TLabelframe.Label', foreground ='black')
        self.feedbackFrame['style'] = "classify.TLabelframe"
        self.feedbackFrame.place(x = 10, y= 100)
        self.feedbackText = tk.Text(self.feedbackFrame, height = 15, 
                                    width = 38, font=('Helvetica', 10),
                                    state = 'disabled')        
        self.feedbackText.pack()
        
        # bottom row: back button and clear button
        # back button
        self.backButton = ttk.Button(self, text="< back",
                    command = lambda: self.controller.showFrame("StartPage"))
        self.backButton['style'] = 'main.TButton'              
        self.backButton.place(x = 10, y = 375)
    
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
    
    def refreshData(self):
        self.userText['state'] = 'normal'
        self.userText.delete(1.0, tk.END)
        self.userText.insert(tk.END, self.controller.user)
        self.userText['state'] = 'disabled'
        self.classificationTree.delete(*self.classificationTree.get_children())
        for activity in self.activities:
            self.feedbackLog[activity] = []
            try:
                reader = open('history/{}+{}.txt'.format(
                              self.controller.user, activity))
            except:
                continue
            feedback = ''
            line = ''
            while True:
                line = reader.readline()
                if not line:
                    if feedback:
                        self.feedbackLog[activity].append(feedback) 
                        feedback = '' 
                    break
                try:
                    item = eval(line)  
                    self.recordDict[activity].append(item)
                    if feedback:
                        self.feedbackLog[activity].append(feedback) 
                        feedback = ''                                     
                    self.classificationTree.insert('', 0, values = item)                    
                except:
                    feedback += line
            reader.close()
                    
                
        