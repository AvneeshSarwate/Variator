'''
Created on Nov 18, 2012
git test
@author: avneeshsarwate
'''
import phrase
import string
import Tkinter
from Tkinter import *
import Levenshtein as lv
import random
#import PIL

class Variator(Tkinter.Tk):
    
    def __init__(self, parent):
        Tkinter.Tk.__init__(self, parent)
        self.parent = parent
        self.entries = []
        self.labels = []
        self.initialize()
        self.objects = {} #dictionary containing tuples (phrase, "key"), indexed by any string
        self.fastEntry = False
        self.minus = False
        self.fastroot = 0
        
        
    def initialize(self):
        hlt = 10
        bgc = "aquamarine"
        
        menu = Tkinter.Menu(self)
        self.config(menu=menu)
        filemenu = Tkinter.Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Load File", command=self.loaddialog)
        filemenu.add_command(label="Save File", command=self.savedialog)
#      
        self.config(bg=bgc)
        self.bind("<FocusIn>", self.focuscolor)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(3, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(2, weight=1)
        self.bind('<Control-c>', self.copy)
        self.bind('<Control-x>', self.cut)
        self.bind('<Control-v>', self.paste)
#        bkimg = Tkinter.PhotoImage(file="background.gif")
#        self.imglabel = Tkinter.Label(self, image=bkimg)
#        self.imglabel.place(x=0, y=0, relwidth=1, relheight=1)
#        
        self.objectLabel = Tkinter.Label(text="Object Editor", font=("Helvetica", 20))
        self.objectLabel.grid(column=0, row=0)
        self.labels.append(self.objectLabel)
        self.objectEntry = Tkinter.Text(self, highlightthickness=hlt, highlightbackground=bgc)
        self.objectEntry.grid(column=0,row=1)
        self.objectEntry.configure(bg="grey", bd=10)
        self.objectEntry.bind("<Button-1>", self.focuscolor)
        self.entries.append(self.objectEntry)
        #self.objectEntry.bind("<Control-v>", self.pasteObj)
        
        
        
        self.objectButton = Tkinter.Button(self,text=u"<= Input Objects", command=self.objButton, highlightbackground=bgc)
        self.objectButton.grid(column=1,row=1)
        
        self.codeLabel = Tkinter.Label(text="Code Here:", font=("Helvetica", 20))
        self.codeLabel.grid(column=0, row=2)
        self.labels.append(self.codeLabel)
        self.codeEntry = Tkinter.Text(self, highlightthickness=hlt, highlightbackground=bgc)
        self.codeEntry.grid(column=0,row=3)
        self.codeEntry.configure(bg="grey", bd=10)
        self.codeEntry.bind("<Button-1>", self.focuscolor)
        self.entries.append(self.codeEntry)
        
        
        self.codeButton = Tkinter.Button(self,text=u"<= Run Code", command=self.runButton, bd=20, highlightbackground=bgc)
        self.codeButton.grid(column=1,row=3)
        
        self.outputLabel = Tkinter.Label(text="Output:", font=("Helvetica", 20))
        self.outputLabel.grid(column=2, row=0)
        self.labels.append(self.outputLabel)
        self.outputEntry = Tkinter.Text(self, highlightthickness=hlt, highlightbackground=bgc)
        self.outputEntry.grid(column=2,row=1)
        self.outputEntry.configure(bg="grey", bd=0)
        self.outputEntry.bind("<Button-1>", self.focuscolor)
        self.entries.append(self.outputEntry)
        
       
        self.container = Tkinter.Frame(self)
        self.labels.append(self.container)
        self.container.grid(column=2, row=3, sticky="EW")
        self.container.rowconfigure(0, weight=1)
        self.container.rowconfigure(1, weight=1)
        self.container.columnconfigure(1, weight=1)
        
        self.inputtitle = Tkinter.Label(self.container, text="INPUT", font=("Helvetica", 30))
        self.inputtitle.grid(column = 0, row = 0, columnspan=2)
        self.labels.append(self.inputtitle)
        
        self.namelabel = Tkinter.Label(self.container, text="Var name:")
        self.namelabel.grid(column = 0, row = 1)
        self.labels.append(self.namelabel)
        self.nameinput = Tkinter.Entry(self.container, highlightbackground=bgc)
        self.nameinput.grid(column=1, row=1, stick='W')
        
        self.noteslabel = Tkinter.Label(self.container, text="Notes/chords:")
        self.noteslabel.grid(column = 0, row = 2)
        self.labels.append(self.noteslabel)
        self.notesinput = Tkinter.Entry(self.container, highlightbackground=bgc)
        self.notesinput.grid(column=1, row=2, sticky="EW")
        self.notesinput.bind("<Key>", self.fastKey)
        self.fastButton = Tkinter.Button(self.container, text=u"FastEntry", command=self.fastfil, highlightbackground=bgc)
        self.fastButton.grid(column=2, row=2)
        self.labels.append(self.fastButton)
        
        self.timeslabel = Tkinter.Label(self.container, text="Times:")
        self.timeslabel.grid(column = 0, row = 3)
        self.labels.append(self.timeslabel)
        self.timesinput = Tkinter.Entry(self.container, highlightbackground=bgc)
        self.timesinput.grid(column=1, row=3, sticky="EW")
        self.randButton = Tkinter.Button(self.container, text=u"Random!", command=self.randfill, highlightbackground=bgc)
        self.randButton.grid(column=2, row=3)
        self.labels.append(self.randButton)
        
        self.keynamelabel = Tkinter.Label(self.container, text="Key;Chord Root;Chord Name:")
        self.keynamelabel.grid(column = 0, row = 4)
        self.labels.append(self.keynamelabel)
        self.keynameinput = Tkinter.Entry(self.container, highlightbackground=bgc)
        self.keynameinput.grid(column=1, row=4, sticky="W")
        
        self.entrybutton = Tkinter.Button(self.container, text=u"Input phrase/chord", command=self.input, highlightbackground=bgc)
        self.entrybutton.grid(column=1, row=5)
        self.labels.append(self.entrybutton)
        
        self.difflabel = Tkinter.Label(self.container, text="lalala")
        self.difflabel.grid(column=1, row=6)
        self.labels.append(self.difflabel)
        self.timesinput.bind("<Key>", self.difupdate)
#        self.timesinput.bind("<Key>", self.container)
        
        for i in self.labels:
            i.configure(bg=bgc)
    
    def fastfil(self):
        notetext = self.getnotes()
        root = int(notetext[0])
        self.fastEntry = not self.fastEntry
        if(self.fastEntry): self.fastButton.config(highlightbackground="red")
        else: self.fastButton.config(highlightbackground="aquamarine")
         
    def difupdate(self, *args):
        notelen = len(self.getnotes())
        timelen = len(self.gettimes())
        if(notelen > timelen):
            self.difflabel.config(bg="red", text=str(notelen-timelen)+" fewer time values than notes")
        if(timelen > notelen):
            self.difflabel.config(bg="red", text=str(timelen-notelen)+" fewer notes than time values")
        if(notelen == timelen):
            self.difflabel.config(bg="aquamarine", text="")
    
    def fastKey(self, event):
        c = event.char
        self.difupdate()
        if not self.fastEntry:
            return
        if(c == "-"):
            self.minus = not self.minus
            return "break"
        if c in "123456789":
            notes = [int(i) for i in self.getnotes()]
            last = notes[len(notes)-1]
            if self.minus:
                self.notesinput.insert("end", str(last-int(c))+" ")
            else:
                self.notesinput.insert("end", str(last+int(c))+" ")
            self.minus = False
        return "break"
#            st = self.notesinput.get()
#            print st
#            st = st[0:len(st)-1]
#            print st
#            self.notesinput.delete("1.0", "end")
#            self.notesinput.insert("1.0", st)

    def focuscolor(self, event):
        for i in self.entries:
            i.configure(background="grey")
        if(event.widget in self.entries):    
            event.widget.configure(background="HotPink")
    
    def getnotes(self):
        notetext = self.notesinput.get().split(" ")
        blanks = []
        notes = []
        for i in range(len(notetext)):
            if len(notetext[i]) < 1:
                blanks.append(i)
                continue
            notes.append(notetext[i])
        blanks.sort(reverse=True)
        print blanks
        for i in blanks:
            notetext.pop(i)
        return notetext
    
    def gettimes(self):
        timetext = self.timesinput.get().split(" ")
        blanks = []
        notes = []
        for i in range(len(timetext)):
            if len(timetext[i]) < 1:
                blanks.append(i)
                continue
            notes.append(int(timetext[i]))
        blanks.sort(reverse=True)
        print blanks
        for i in blanks:
            timetext.pop(i)
        return timetext
        
    
    def randfill(self):
        self.timesinput.delete(0, "end")
        notetext = self.notesinput.get().split(" ")
        blanks = []
        notes = []
        for i in range(len(notetext)):
            if len(notetext[i]) < 1:
                blanks.append(i)
                continue
            notes.append(notetext[i])
        blanks.sort(reverse=True)
        print blanks
        for i in blanks:
            notetext.pop(i)
        times = [2, 4, 4, 8, 8, 16, 16]
        for i in range(len(notetext)):
            self.timesinput.insert("end", str(times[random.randint(0, 6)])+" ")
              
    
    def input(self):
        try:
            varname = self.nameinput.get()
            keyrootname = self.keynameinput.get().split(";")
            if len(keyrootname) > 1:
                keyrootname[1].replace(" ", "")
            notetext = self.notesinput.get().replace(",", "").split(" ")
            timetext = self.timesinput.get().replace(",", "").split(" ")
            notes = []
            blanks = []
            typ = ""
            if not self.notesinput.get().replace(" ", "").replace("-", "").isdigit(): #is prog
                for i in range(len(notetext)):
                    if len(notetext[i]) < 1:
                        blanks.append(i)
                        continue
                    notes.append(self.objects[notetext[i]][0])
                blanks.sort(reverse=True)
                for i in blanks:
                    notetext.pop(i)
                typ = "prog"
            else:
                for i in range(len(notetext)):
                    if len(notetext[i]) < 1:
                        blanks.append(i)
                        continue
                    notes.append(int(notetext[i]))
                blanks.sort(reverse=True)
                print blanks
                for i in blanks:
                    notetext.pop(i)
                print notetext
                timetext = self.timesinput.get().split(" ")
            if len(timetext) > 1:  #corner case - phrase of one note
                times = []
                blanks = []
                for i in range(len(timetext)):
                    if len(timetext[i]) < 1:
                        blanks.append(i)
                        continue
                    times.append(int(timetext[i]))
                blanks.sort(reverse=True)
                for i in blanks:
                    timetext.pop(i)
                if typ != "prog": typ = "phrase"
            else:
                typ = "chord"
            if typ == "phrase":
                obj = phrase.Phrase(notes, times)
                obj.key = keyrootname[0]
            if typ == "chord":
                obj = phrase.Chord(notes)
                if len(keyrootname) > 1:
                    if len(keyrootname[1]) > 0:
                        obj.root = int(keyrootname[1])
                    if len(keyrootname[2]) > 0:
                        obj.name = keyrootname[2]
            if typ == "prog":
                obj = phrase.Progression()
                obj.c = notes
                print str(obj.c[0]) + " should be a chord" 
                obj.t = times
                obj.names = notetext
            self.objects[varname] = (obj, keyrootname[0])
            print str(obj)
            if varname in self.objects.keys():
                objstr = self.objectEntry.get(1.0, "end").split("\n")
                matchind = -1
                for i in range(len(objstr)):
                    if varname in objstr[i]:
                        matchind = i
                newvarstr = "\n"+ varname+":"+keyrootname[0]+":"+str(obj).split("[")[0]
                objstr[matchind] = newvarstr
                nonempty = []
                for i in objstr:
                    if i != "":
                        nonempty.append(i)
                self.objectEntry.delete(1.0, "end")
                self.objectEntry.insert(1.0, "\n".join(nonempty))
                
            #slopily handled
            else: 
                self.objectEntry.insert("end","\n"+ varname+":"+keyrootname[0]+":"+str(obj).split("[")[0])
        except Exception as e:
            print "\nERROR in Input: Check formatting\n"
        
        
            
    
    def output(self, arg):
        if(arg == "clear"):
            self.outputEntry.delete(1.0, "end")
            return
        text = str(arg)
        print text
        self.outputEntry.insert("end", "\n"+text+"\n")
        
        
        ##input format:   varname: key: (note, time).(note, time)..... 
    def objButton(self):
        try:
            text = self.objectEntry.get(1.0, "end")
            lines = text.split("\n")
            linesplit = []
            print len(lines)
            print
            for i in range(len(lines)):
                lines[i].replace(" ", "")
                linesplit.append(lines[i].split(":"))
            for i in range(len(linesplit)):
                if(len(linesplit[i]) != 3):
                    continue
                print len(linesplit[i])
                print linesplit[i][2]
                if("." in linesplit[i][2] and linesplit[i][2][2].isdigit()):    #if its a phrase
                    notes = linesplit[i][2].split(".")
                    phr = phrase.Phrase()
                    for j in range(len(notes)):
                        phr.append(eval(notes[j]))
                    phr.key = linesplit[i][1]
                    self.objects[linesplit[i][0]] = (phr, linesplit[i][1]) #should be linesplit[i][1]
                if("." in linesplit[i][2] and linesplit[i][2][1].isalpha()): #is prog 
                    print "reaading prog"
                    decs = ""
                    for k in self.objects.keys():
                        decs += k + " = " + "self.objects['" + k + "'][0]\n"
                    exec(decs)
                    notes = linesplit[i][2].split(".")
                    prog = phrase.Progression()
                    for j in range(len(notes)):
                        prog.append(eval(notes[j]))
                        print notes[j].split(",")[0].replace("(", "")
                        prog.names.append(notes[j].split(",")[0].replace("(", ""))
                    print str(eval(notes[j])[0]) + "should be a chord here"
                    prog.key = linesplit[1]
                    self.objects[linesplit[i][0]] = (prog, linesplit[i][1])
                if not "." in linesplit[i][2]:
                    notes = eval( linesplit[i][2].replace("(", "[").replace(")", "]") )
                    chrd = phrase.Chord(notes)
                    self.objects[linesplit[i][0]] = (chrd, linesplit[1])
                    print "chord length" + str(len(chrd))
                #
            self.outputEntry.delete(1.0, "end")
            for i in self.objects.keys():
                print self.objects[i][0].type
                self.output(self.objects[i][0])
        except Exception as e:
            print "\nERROR in ObjectEditor: Check formatting\n"
            
    
    def runButton(self):
        text = self.codeEntry.get(1.0, "end")
        decs = ""
        for i in self.objects.keys():
            decs += i + " = " + "self.objects['" + i + "'][0]\n"
        exec(decs)
        text = text.replace("output(", "self.output(")
        #TODO: text = text.replace("play(", "phrase.play(")
        exec(text)
        
    def registerObjects(self):
        decs = ""
        for i in self.objects.keys():
            decs += i + " = " + "self.objects['" + i + "'][0]\n"
        exec(decs)
        
#    def pasteObj(self):
#        text = self.selection_get(selection='CLIPBOARD')
#        self.objectEntry.insert(INSERT, text)

    def copy(self, event=None):
        self.clipboard_clear()
        text = self.get("sel.first", "sel.last")
        self.clipboard_append(text)
    
    def cut(self, event):
        self.copy()
        self.delete("sel.first", "sel.last")

    def paste(self, event):
        text = self.selection_get(selection='CLIPBOARD')
        self.insert('insert', text)
        
    def save(self, fname):
        f = open(fname, "w+")
        f.write(self.objectEntry.get(1.0, "end"))
    
    def load(self, fname):
        try:
            f = open(fname)
        except Exception as e:
            print "\nERROR: file does not exist"
            return
        
        self.objectEntry.insert("end", "\n"+f.read())
    
    def loaddialog(self):
        d = Dialog(self, "load")
        self.wait_window(d)
        return
    
    def savedialog(self):
        d = Dialog(self, "save")
        self.wait_window(d)
        return

    
        
class Dialog(Tkinter.Toplevel):

    def __init__(self, parent, dialogtype, title = None):

        Tkinter.Toplevel.__init__(self, parent)
        self.transient(parent)
        self.dialogtype = dialogtype
        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = Tkinter.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden
        self.fnamelabel = Label(self, text="File Name:")
        self.fnamelabel.pack()
        self.fnameinput = Entry(self)
        self.fnameinput.pack()

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons
        
        box = Tkinter.Frame(self)

        w = Tkinter.Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = Tkinter.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):

        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):

        # put focus back to the parent window
        self.parent.focus_set()
        self.destroy()

    #
    # command hooks

    def validate(self):

        return 1 # override

    def apply(self):
        if(self.dialogtype == 'save'):
            self.parent.save(self.fnameinput.get())
        if(self.dialogtype == 'load'):
            self.parent.load(self.fnameinput.get())
        pass # override
        
        
if __name__ == "__main__":
    app = Variator(None)
    app.title('my application')
    app.mainloop()