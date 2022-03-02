from os.path import isdir, isfile, join, basename
from time import sleep

from analytisstools.log.logging import Logging
from analytisstools.gui.functions import updateMessage, updateAll
from analytisstools.utils.io import writeFullJS

from apyconc.data import _LOGFILE, _EXPORTED


def updateConcentration(methodpath, csvfilepath):
    try:
        logClasse = Logging(_LOGFILE)
        writeFullJS(_EXPORTED, {})
        updateAll(
            0,
            f"Démarrage de la mise à jour des concentrations dans la méthode\n{basename(methodpath)}",
        )
        sleep(1)
        updateMessage(
            f"Vérification des données envoyées en cours\n({basename(methodpath)} & {basename(csvfilepath)})..."
        )
        sleep(1)
        logClasse.add(f"Début mise à jour : {methodpath}, {csvfilepath}", "info")

        if not (
            (
                isdir(methodpath)
                and isfile(join(methodpath, "DAMethod", "Quant", "quantitative.xml"))
                and methodpath.lower().endswith(".d")
            )
            or (
                isdir(methodpath)
                and isfile(join(methodpath, "5.1", "Method.mmx"))
                and isfile(join(methodpath, "5.1", "Method.mmx.key"))
            )
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
        sleep(1)

        updateMessage(
            f"Détection des fichiers XML à mettre à jour...",
        )
        sleep(1)

        if mode == "masshunter":
            xmlfile = join(methodpath, "DAMethod", "Quant", "quantitative.xml")
            keyfile = join(methodpath, "DAMethod", "Quant", "quantitative.xml")
        elif mode == "tracefinder":
            xmlfile = join(methodpath, "5.1", "Method.mmx")
            keyfile = join(methodpath, "5.1", "Method.mmx.key")
        else:
            raise NotImplementedError(f"Le mode {mode} n'a pas encore été implémenté !")

        logClasse.add(f"Mode : {mode}, XML = {xmlfile}, KEY = {keyfile}", "info")

        updateAll(
            10,
            f"Fichiers XML détectés\n({basename(xmlfile)} & {basename(keyfile)}) !",
        )
        sleep(1)

        updateAll(
            100,
            f"Finalisation de l'export des concentrations au mode {mode}...",
        )
        sleep(1)

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

        erreur = "Erreur lors de la mise à jour des concentrations."
        variablesstr = f"Dump Variables importantes :\n" + "\n".join(
            [f"{k} = {v}" for k, v in allvariables.items()]
        )
        updateMessage(erreur)
        sleep(1)

        logClasse.add(erreur, "Critical")
        logClasse.add(variablesstr, "Info")

        return False
