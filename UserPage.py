import tkinter as tk   
import tkinter.ttk as ttk

class UserPage(tk.Frame):
    def __init__(self, parent, controller):
        # init the user list
        logReader = open('history/users.txt', 'r')
        self.userList = []
        self.userNumber = 0      
        for line in logReader.readlines():
            userItem = eval(line)
            self.userList.append(userItem)
            self.userNumber += 1
        logReader.close()
        self.oldUserNumber = self.userNumber
        self.selectedUserIndex = 0
        # build GUI
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.creatWidgets()
        
    def getCurrentUser(self):
        return (self.selectedUserIndex)
        
    def refreshList(self):
        for i in range(self.oldUserNumber):
            self.userListWidget.delete('U' + str(i))
        if (self.userNumber != 0):
            for i in range(self.userNumber):
                self.userListWidget.insert('', i, iid="U" + str(i), values = (self.userList[i][0],self.userList[i][1]))        
        
    def acceptAdd(self, event):
        self.userList.append((self.nameEntry.get(), self.statusEntry.get()))
        self.userNumber = self.userNumber + 1
        self.refreshList()
        self.editUserBox.destroy()
        
    def acceptEdit(self, event):
        self.userList[self.selectedUserIndex] = (self.nameEntry.get(), self.statusEntry.get());
        self.refreshList()
        self.editUserBox.destroy()
        
    def cancelEdit(self, event):
        self.editUserBox.destroy()
        
    def selectUser(self, event):
        self.selectedUserItem = self.userListWidget.selection()[0]
        self.selectedUserIndex = int(self.selectedUserItem[1:len(self.selectedUserItem)])
        
    def setUser(self, event):
        self.selectedUserItem = self.userListWidget.selection()[0]
        self.selectedUserIndex = int(self.selectedUserItem[1:len(self.selectedUserItem)])
        user = self.userListWidget.item(self.selectedUserItem)['values'][0]
        self.userText['state'] = 'normal'
        self.userText.delete(1.0, tk.END)
        self.userText.insert(tk.END, user)
        self.userText['state'] = 'disabled'
        self.controller.user = user
        
    def showEditBox(self):
        # build message box
        self.editUserBox = tk.Toplevel()
        self.editUserBox.geometry("250x100")
        self.editUserFrame = tk.Frame(self.editUserBox)
        self.editUserFrame.pack(pady = 5)
        self.editButtonFrame = tk.Frame(self.editUserBox)
        self.editButtonFrame.pack(pady = 5)
        self.nameLabel = tk.Label(self.editUserFrame, text = "Name:")
        self.nameLabel.grid(row = 0, column = 0)
        self.statusLabel = tk.Label(self.editUserFrame, text = "Status:")
        self.statusLabel.grid(row = 1, column = 0)
        self.nameContent = tk.StringVar()
        self.statusContent = tk.StringVar()
        self.nameEntry = tk.Entry(self.editUserFrame, textvariable = self.nameContent)
        self.nameEntry.grid(row = 0, column = 1, padx = 5)
        self.statusEntry = tk.Entry(self.editUserFrame, textvariable = self.statusContent)
        self.statusEntry.grid(row = 1, column = 1, padx = 5) 
        self.buttonOK = ttk.Button(self.editButtonFrame, text = "OK")
        self.buttonOK.grid(row = 0, column = 0, padx = 10)
        self.buttonCancel = ttk.Button(self.editButtonFrame, text = "Cancel")
        self.buttonCancel.grid(row = 0, column = 1, padx = 10) 
        self.buttonCancel.bind("<Button-1>", self.cancelEdit)
        

    def addUser(self, event):
        self.oldUserNumber = self.userNumber
        self.showEditBox()
        self.nameContent.set("")
        self.statusContent.set("")
        self.buttonOK.bind("<Button-1>", self.acceptAdd)
        
    def editUser(self, event):
        self.selectedUserItem = self.userListWidget.selection()[0]
        user = self.userListWidget.item(self.selectedUserItem)['values'][0]
        if user == "Admin":
            return
        self.oldUserNumber = self.userNumber
        self.showEditBox()
        self.nameContent.set(self.userList[self.selectedUserIndex][0])
        self.statusContent.set(self.userList[self.selectedUserIndex][1])
        self.buttonOK.bind("<Button-1>", self.acceptEdit)
        
    def deleteUser(self, event):
        self.selectedUserItem = self.userListWidget.selection()[0]
        user = self.userListWidget.item(self.selectedUserItem)['values'][0]
        if user == "Admin":
            return
        self.oldUserNumber = self.userNumber
        self.userList.pop(self.selectedUserIndex)
        self.userNumber = self.userNumber - 1
        self.refreshList()
        if user == self.controller.user:
            user = 'Admin'
            self.userText['state'] = 'normal'
            self.userText.delete(1.0, tk.END)
            self.userText.insert(tk.END, user)
            self.userText['state'] = 'disabled'
            self.controller.user = user

    def creatWidgets(self):
        self.canvas = tk.Canvas(self)
        self.backgroundImage = Image.open("./background/background.jpg")
        self.backgroundImage = self.backgroundImage.resize((630, 415), Image.ANTIALIAS)
        self.backgroundImage = ImageTk.PhotoImage(self.backgroundImage)
        self.backgroundLabel = tk.Label(self, image=self.backgroundImage)
        self.backgroundLabel.place(x = 0, y = 0, relwidth = 1, relheight = 1) 
        
        self.userPageButtonStyle = ttk.Style() # style of the buttons
        self.userPageButtonStyle.configure('main.TButton', font=('Helvetica', 10), width = 14) 
        
        # user label
        self.activityLabel = tk.Label(self, text = "User:", 
                                          font = ('helvetica', 10),
                                      fg = 'white', bg = '#191A1C')
        self.activityLabel.place(x = 425, y = 35)
        
        # user text
        self.userText = tk.Text(self, height = 1, 
                                    width = 15, font=('Helvetica', 10))
        self.userText.insert(tk.END, self.controller.user)
        self.userText['state'] = 'disabled'
        self.userText.place(x = 495, y = 35)
        
        # build the frame
        self.userListFrame = tk.Frame(self)
        self.userListFrame.place(x = 380, y = 65)
        self.buttonFrame = tk.Frame(self)
        self.buttonFrame.place(x = 380, y = 300)
        # build user list
        #self.listInfoLabel = tk.Label(self.userListFrame, text = "DOUBLE CLICK to choose user",
        #                         font = ('Helvetica', 9))
        #self.listInfoLabel.pack(side = "top")
        self.userListWidget = ttk.Treeview(self.userListFrame, columns = ('name','status'),
                                           show = "headings")
        self.userListWidget.pack(side = "top")
        self.userListWidget.column('name', width = 120, anchor='center')
        self.userListWidget.column('status', width = 112, anchor='center')        
        self.userListWidget.heading('name', text='Name')
        self.userListWidget.heading('status', text='Status')
        self.userListWidget.bind("<Double-Button-1>", self.selectUser)
        # print list
        for i in range(0, self.userNumber, 1):
            self.userListWidget.insert('', i, iid="U" + str(i), values =
                                       (self.userList[i][0],self.userList[i][1]))
        
        # Place buttons
        self.addButton = ttk.Button(self.buttonFrame, text = "Add")
        self.addButton.bind("<Button-1>", self.addUser)
        self.addButton.grid(row = 0, column = 0, padx = 5, pady = 3, sticky = "w")
        self.addButton['style'] = 'main.TButton' 

        self.editButton = ttk.Button(self.buttonFrame, text = "Edit")
        self.editButton.bind("<Button-1>", self.editUser)
        self.editButton.grid(row = 1, column = 1, padx = 5, pady = 3, sticky = "w") 
        self.editButton['style'] = 'main.TButton' 
        
        self.setButton = ttk.Button(self.buttonFrame, text = "Set")
        self.setButton.bind("<Button-1>", self.setUser)
        self.setButton.grid(row = 1, column = 0, padx = 5, pady = 3, sticky = "w") 
        self.setButton['style'] = 'main.TButton' 
        
        self.deleteButton = ttk.Button(self.buttonFrame, text = "Delete")
        self.deleteButton.bind("<Button-1>", self.deleteUser)
        self.deleteButton.grid(row = 0, column = 1, padx = 5, pady = 3, sticky = "w")    
        self.deleteButton['style'] = 'main.TButton' 

        # back button
        self.backButton = ttk.Button(self, text="< back",
                    command = lambda: self.writeAndReturn())
        self.backButton['style'] = 'main.TButton'              
        self.backButton.place(x = 10, y = 375)
    
    def writeAndReturn(self):
        # write the users and return
        logWriter = open('history/users.txt', 'w')
        for each in self.userListWidget.get_children():
            userItem = self.userListWidget.item(each)['values']
            logWriter.write(str(tuple(userItem)) + '\n')
        logWriter.close()
        self.controller.showFrame("StartPage") 
    
