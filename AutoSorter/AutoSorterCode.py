from tkinter import *
import json
import sys
import os
import shutil


class Directories():

    def __init__(self):
        """Verifie les dossier enregistrés et remplace les dossiers non existants avec un dossier présent dans /AutoSorter
        """
        super().__init__()
        try:
            with open(f"{sys.path[0]}/directories.json") as file:
                self.options = json.load(file)

            if self.options["downDir"]["dir"] == None or not os.path.isdir(self.options["downDir"]["dir"]):
                self.options["downDir"]["dir"] = f"{sys.path[0]}/Téléchargements"
                if not os.path.isdir(f"{sys.path[0]}/Téléchargements"):
                    os.makedirs(f"{sys.path[0]}/Téléchargements")

            for fileType, directory in zip(self.options["directories"], ["Images", "Documents", "Audios", "Vidéos", "Unpack"]):
                if self.options["directories"][fileType]["dir"][0] == None or not os.path.isdir(self.options["directories"][fileType]["dir"][0]):
                    self.options["directories"][fileType]["dir"][0] = f"{sys.path[0]}/{directory}"
                    if not os.path.isdir(f"{sys.path[0]}/{directory}"):
                        os.makedirs(f"{sys.path[0]}/{directory}")
                
                for case in self.options["directories"][fileType]["specialConditions"]:
                    try:
                        if case[0] == None or not os.path.isdir(case[0]):
                            del self.options["directories"][fileType]["specialConditions"][case]
                    except:
                        del self.options["directories"][fileType]["specialConditions"][case]

            with open(f"{sys.path[0]}/directories.json", "w+") as file:
                json.dump(self.options, file, indent=4)
            
        except:
            self.createJSONFile()
            self.__init__()
    

    def createJSONFile(self):
        """Crée le fichier directories.json quand un erreur arrive pendant la lecture du fichier par __init__
        """
        baseText = {
            "downDir": {
                "dir": None,
                "exceptions": [],
                "exceptionsPrefix": [],
                "exceptionsSuffix": []
            },
            "directories": {
                "imageDir": {
                    "dir": [None, ".jpg", ".png"],
                    "specialConditions": {}
                },
                "docDir": {
                    "dir": [None, ".txt", ".doc", ".docx"],
                    "specialConditions": {}
                },
                "audioDir": {
                    "dir": [None, ".wav", ".mp3"],
                    "specialConditions": {}
                },
                "videoDir": {
                    "dir": [None, ".mp4", ".mov"],
                    "specialConditions": {}
                },
                "unpackDir": {
                    "dir": [None],
                    "specialConditions": {}
                },
            },
            "cycleTime": "2 minutes"
        }
        with open(f"{sys.path[0]}/directories.json", "w+") as file:
            json.dump(baseText, file, indent=4)


    def recognizeFileType(self):
        """Reconnais le type de fichier en utilisant les informations enregistrées dans le dictionnaire self.options
        ou dans les cas particuliers créés par l'utilisateur et deplace le fichier.
        """
        for file in os.listdir(self.options["downDir"]["dir"]):
            recognizedFile = False

            if file in self.options["downDir"]["exceptions"] or file.startswith(tuple(self.options["downDir"]["exceptionsPrefix"])) or file.endswith(tuple(self.options["downDir"]["exceptionsSuffix"])):
                pass
            else:
                for fileType in self.options["directories"]:
                    for fileExtension in self.options["directories"][fileType]["dir"][1:len(self.options["directories"][fileType]["dir"])]:
                        if file.endswith(fileExtension):

                            try:
                                for specialCase in self.options["directories"][fileType]["specialConditions"]:
                                    for specificCase in specialCase:
                                        if file.startswith(specificCase[1:len(specialCase)]):
                                            shutil.move(f'{self.options["downDir"]["dir"]}/{file}', f'{specialCase[0]}/{file}')
                                            recognizedFile = True
                                            break
                                    break
                                shutil.move(f'{self.options["downDir"]["dir"]}/{file}', f'{self.options["directories"][fileType]["dir"][0]}/{file}')
                            except:
                                shutil.move(f'{self.options["downDir"]["dir"]}/{file}', f'{self.options["directories"][fileType]["dir"][0]}/{file}')
                        if recognizedFile:
                            break
                    if recognizedFile:
                        break



class Application:

    timeList = [
        "10 secondes", "30 secondes", "1 minute", "2 minutes", "5 minutes", "10 minutes", "30 minutes"
    ]

    def timer(self, time):
        directory.recognizeFileType()
        self.afterID = self.timerFrame.after(time, self.newCycle)


    def verifyTime(self):
        if directory.options["cycleTime"] == "10 secondes":
            return self.timer(10000)
        
        elif directory.options["cycleTime"] == "30 secondes":
            return self.timer(30000)
        
        elif directory.options["cycleTime"] == "1 minute":
            return self.timer(60000)
        
        elif directory.options["cycleTime"] == "2 minutes":
            return self.timer(120000)
        
        elif directory.options["cycleTime"] == "5 minutes":
            return self.timer(300000)
        
        elif directory.options["cycleTime"] == "10 minutes":
            return self.timer(600000)
        
        elif directory.options["cycleTime"] == "30 minutes":
            return self.timer(1800000)
        
        else:
            messagebox.showerror("Erreur", "Le programme n'a pas pu\ntrouver la durée du cycle.")


    def newCycle(self):
        try:
            self.timerFrame.after_cancel(self.afterID)
            self.verifyTime()
            self.frame.after_cancel(self.eraseWait)
            self.infoBar.config(text="Nouveau cycle commencé!", fg="green")
            self.eraseWait = self.frame.after(5000, self.eraseInfoBar)
        except:
            self.frame.after_cancel(self.eraseWait)
            self.timerFrame.after_cancel(self.afterID)
            self.infoBar.config(text="Le cycle n'a pas pu commencer.", fg="red")
            self.eraseWait = self.frame.after(5000, self.eraseInfoBar)
    

    def stopCycleFunc(self):
        try:
            self.timerFrame.after_cancel(self.afterID)
            self.frame.after_cancel(self.eraseWait)
            self.infoBar.config(text="Cycle arrêté!", fg="green")
            self.eraseWait = self.frame.after(5000, self.eraseInfoBar)
        except:
            self.frame.after_cancel(self.eraseWait)
            self.infoBar.config(text="Le cycle n'a pas pu s'arrêter.", fg="red")
            self.eraseWait = self.frame.after(5000, self.eraseInfoBar)
    

    def singleFire(self):
        try:
            directory.recognizeFileType()
            self.frame.after_cancel(self.eraseWait)
            self.infoBar.config(text="Fichiers rangés!", fg="green")
            self.eraseWait = self.frame.after(5000, self.eraseInfoBar)
        except:
            self.frame.after_cancel(self.eraseWait)
            self.infoBar.config(text="Les fichiers n'ont pas pu être rangés.", fg="red")
            self.eraseWait = self.frame.after(5000, self.eraseInfoBar)

    
    def changeDictionaryTimeCycle(self, event):
        directory.options["cycleTime"] = self.time.get()
        with open(f"{os.getcwd()}/directories.json", "w+") as file:
            json.dump(directory.options, file, indent=4)


    def __init__(self):
        root = Tk()
        root.title("AutoSorter")

        # ***********************
        
        self.frame = Frame(root, bg="gray20")
        self.frame.pack(fill=BOTH, expand=TRUE)

        self.eraseInfoBar = lambda: self.infoBar.config(text="", fg="gray80")

        # ***********************

        self.timerFrame = Frame(root)

        self.timer(1000)
        self.timerFrame.after_cancel(self.afterID)
        self.eraseWait = self.frame.after(5000, self.eraseInfoBar)

        # ***********************

        self.time = StringVar()
        self.time.set(directory.options["cycleTime"])
        timeWaitSelect = OptionMenu(self.frame, self.time, *self.timeList)
        timeWaitSelect.configure(
            bg="gray20", fg="gray80", activebackground="gray17", activeforeground="gray80",
            font=("Futura", 15), relief=FLAT
        )
        timeWaitSelect.bind("<Configure>", self.changeDictionaryTimeCycle)
        timeWaitSelect.grid(row=0, columnspan=2, pady=10)
 
        # ***********************

        self.infoBar = Label(self.frame, text="", height=1, bg="gray20", fg="gray80", font=("Futura", 10, "bold"))
        self.infoBar.grid(row=1, columnspan=2)

        # ***********************

        newCycle = Button(
            self.frame, text="Mettre à jour le cycle", command=self.newCycle,
            bg="gray20", fg="gray80", activebackground="gray17", activeforeground="gray80",
            width=17, font=("Futura", 10), relief=FLAT
        )
        newCycle.grid(row=2, padx=5, pady=5)

        # ***********************

        stopCycle = Button(
            self.frame, text="Arreter le cycle actuel", command=self.stopCycleFunc,
            bg="gray20", fg="gray80", activebackground="red", activeforeground="gray80",
            width=17, font=("Futura", 10), relief=FLAT
        )
        stopCycle.grid(row=2, column=1, padx=5, pady=5)

        # ***********************

        oneTimeFire = Button(
            self.frame, text="Ranger les fichiers", command=self.singleFire,
            bg="gray20", fg="gray80", activebackground="gray17", activeforeground="gray80",
            width=17, font=("Futura", 10), relief=FLAT
        )
        oneTimeFire.grid(row=3, column=0, padx=5, pady=5)

        # ***********************

        root.mainloop()



if __name__ == "__main__":
    directory = Directories()
    app = Application()
