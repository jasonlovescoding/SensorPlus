import tkinter as tk

# an modifiable entry that pops up on double click event on a treeview
# designed to modify:
#    scores, which should range from 1 to 10
class ModifiableEntry(tk.Entry):
    def __init__(self, parent, row, column, statsName):
        ''' If relwidth is set, then width is ignored '''
        super().__init__(parent)
        self.parent = parent
        self.row = row
        self.column = column
        self.statsName = statsName
        
        text = parent.set(row, column)
        self.text = tk.StringVar()
        self.text.set(text)
        self['textvariable'] = self.text
        self['selectbackground'] = '#1BA1E2'
        self['exportselection'] = 0

        # keep focusing
        self.focus_force()
        # quit
        self.bind("<Escape>", lambda *ignore: self.destroy())
        self.bind("<FocusOut>", lambda *ignore: self.destroy())
        # select all
        self.bind("<Control-a>", self.selectAll)
        # update
        self.bind("<Return>", self.update)

    def selectAll(self, *ignore):
        ''' Set selection on the whole text '''
        self.selection_range(0, 'end')
        # returns 'break' to interrupt default key-bindings
        return 'break'
        
    def update(self, *ignore):
        newScore = self.text.get()
        if not newScore.isdigit():
            return
        newScore = int(newScore)
        if not (newScore >=1 and newScore <=10):
            return
        self.parent.set(self.row, self.column, str(newScore))
        statsFile = open(self.statsName, 'r+')
        stats = statsFile.readlines()
        if len(stats) != 0:
            if stats[-1].isdigit():
                stats[-1] = str(newScore)
            else:
                stats.append(str(newScore))
        statsFile.seek(0)
        statsFile.writelines(stats)
        statsFile.close()
        self.destroy()
        
    def close(self):
        self.destroy()