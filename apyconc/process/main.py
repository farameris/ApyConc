from os.path import isdir, isfile, join
from time import sleep
from traceback import format_exc

from analytisstools.log.logging import Logging
from analytisstools.gui.functions import updateMessage, updateAll

from apyconc.data import _LOGFILE


def updateConcentration(methodpath, csvfilepath):
    try:
        logClasse = Logging(_LOGFILE)
        updateAll(
            0,
            f"Démarrage de la mise à jour des concentrations dans la méthode {methodpath}",
        )
        sleep(0.5)
        updateMessage(
            f"Vérification des données envoyées en cours ({methodpath} & {csvfilepath})..."
        )
        sleep(0.5)
        logClasse.add(f"Début mise à jour : {methodpath}, {csvfilepath}", "info")

        if not (
            isdir(methodpath)
            and isfile(join(methodpath, "DAMethod", "Quant", "quantitative.xml"))
            and methodpath.lower().endswith(".d")
        ) or (
            isdir(methodpath)
            and isfile(join(methodpath, "5.1", "Method.mmx"))
            and isfile(join(methodpath, "5.1", "Method.mmx.key"))
        ):
            raise TypeError(
                "La méthode fournie n'est ni une méthode MassHunter Quant, ni une méthode TraceFinder 5.1 : {}".format(
                    methodpath
                )
            )

        if not csvfilepath.lower().endswith(".csv"):
            raise TypeError(
                "Le fichier de données à mettre à jour est incorrect : {}".format(
                    csvfilepath
                )
            )

        if methodpath.lower().endswith(".d"):
            mode = "masshunter"
        else:
            mode = "tracefinder"

        updateAll(
            5,
            f"Vérification des données terminée ! Mode d'export des concentrations : {mode}",
        )
        sleep(0.5)

        updateMessage(
            f"Détection des fichiers XML à mettre à jour...",
        )
        sleep(0.5)

        if mode == "masshunter":
            xmlfile = join(methodpath, "DAMethod", "Quant", "quantitative.xml")
            keyfile = None
        elif mode == "tracefinder":
            xmlfile = join(methodpath, "5.1", "Method.mmx")
            keyfile = join(methodpath, "5.1", "Method.mmx.key")
        else:
            raise NotImplementedError(f"Le mode {mode} n'a pas encore été implémenté !")

        logClasse.add(f"Mode : {mode}, XML = {xmlfile}, KEY = {keyfile}", "info")

        updateAll(
            10,
            f"Fichiers XML détectés ({xmlfile} & {keyfile}) !",
        )
        sleep(0.5)

        updateAll(
            100,
            f"Finalisation de l'export des concentrations au mode {mode}...",
        )
        sleep(0.5)

        return True

    except:
        allvariables = {}
        if "methodpath" in locals():
            allvariables["methodpath"] = methodpath
        if "csvfilepath" in locals():
            allvariables["csvfilepath"] = csvfilepath
        if "mode" in locals():
            allvariables["mode"] = mode
        if "xmlfile" in locals():
            allvariables["xmlfile"] = xmlfile
        if "keyfile" in locals():
            allvariables["keyfile"] = keyfile

        erreur = "Erreur lors de la mise à jour des concentrations : {}".format(
            format_exc()
        )
        variablesstr = f"Dump Variables importantes :\n\n" + "\n\n".join(
            [f"{k} = {v}" for k, v in allvariables.items()]
        )
        updateMessage(erreur)

        logClasse.add(erreur, "Critical")
        logClasse.add(variablesstr, "Info")

        return False
