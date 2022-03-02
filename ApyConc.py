import sys
from time import time, sleep
from os.path import isdir, isfile, join
from PyQt5.QtCore import QThread
from PyQt5.QtCore import QObject, pyqtSignal

from analytisstools.gui.main import MyApp, ProgressBar
from analytisstools.gui.functions import updateMessage
from analytisstools.utils.io import read_ini

from apyconc.data import _INIFILE
from apyconc.process.main import updateConcentration


class CustomWorker(QObject):
    finished = pyqtSignal(bool)

    def __init__(self, methodpath, updatefilepath, parent=None):
        super(CustomWorker, self).__init__(parent)
        self.methodpath = methodpath
        self.updatefilepath = updatefilepath

    def task(self):
        self.endstatus = updateConcentration(self.methodpath, self.updatefilepath)
        self.finished.emit(self.endstatus)


class mainthread:
    def __init__(self, version, date, icone, methodpath, updatefilepath):
        self.myApp = MyApp()
        self.myProgressBar = ProgressBar(
            icone=icone,
            title=f"ApyConc version {version} ({date}) - Apychrom",
        )
        self.myProgressBar.show()
        self.myProgressBar.customclosevent.connect(self.brutalstop)
        self.thread = QThread()
        self.pyprocess = CustomWorker(methodpath, updatefilepath)
        self.pyprocess.moveToThread(self.thread)
        self.pyprocess.finished.connect(self.endApyConc)
        self.thread.started.connect(self.pyprocess.task)
        self.thread.start()

        self.myApp.launchQApp()

    def brutalstop(self, closing):
        if closing:
            updateMessage("Problème d'exécution, ApyConc va se terminer.")
            self.thread.exit()
            self.endApyConc(False)

    def endApyConc(self, cleanend):
        if cleanend:
            updateMessage("ApyConc correctement executé !")
        else:
            updateMessage("Problème d'exécution, ApyConc va se terminer.")

        sleep(2)

        self.thread.exit()
        self.myProgressBar.close()
        self.myApp.exit(cleanend)


if len(sys.argv) < 3:
    method = r"C:\Users\cletr\OneDrive - Analytiss\DevInformatique\Python\ApyConc\datatest\2021_PHTALATES_NEWLIST_méthode définitive"
    update = r"C:\Users\cletr\OneDrive - Analytiss\DevInformatique\Python\ApyConc\ToUpdate.csv"
    raise AttributeError(
        "Il manque des arguments pour le lancement du script ! Ce script doit être appelé : ApyConc.exe <CheminMethodeAMettreAJour> <CheminFichierCSVContenantLesDonneesAImporter>"
    )
else:
    method = sys.argv[1]
    update = sys.argv[2]

if not (
    isdir(method)
    and isfile(join(method, "DAMethod", "Quant", "quantitative.xml"))
    and method.lower().endswith(".d")
) or (
    isdir(method)
    and isfile(join(method, "5.1", "Method.mmx"))
    and isfile(join(method, "5.1", "Method.mmx.key"))
):
    raise TypeError(
        "La méthode fournie n'est ni une méthode MassHunter Quant, ni une méthode TraceFinder 5.1 : {}".format(
            method
        )
    )

if not update.lower().endswith(".csv"):
    raise TypeError(
        "Le fichier de données à mettre à jour est incorrect : {}".format(update)
    )

version = read_ini(_INIFILE, "GENERAL", "version")
date = read_ini(_INIFILE, "GENERAL", "date")
icone = read_ini(_INIFILE, "GENERAL", "icone")

ApyConc = mainthread(
    version=version,
    date=date,
    icone=icone,
    methodpath=method,
    updatefilepath=update,
)
