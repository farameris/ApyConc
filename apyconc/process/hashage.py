import base64
from codecs import encode, decode
from hashlib import sha1
from os.path import isfile


def getB64hash(toHashFile):
    if not isfile(toHashFile):
        raise FileNotFoundError(f"Le fichier fourni {toHashFile} n'existe pas !")

    with open(toHashFile, "br") as bFile:
        bFullFile = bFile.read()

    return encode(decode(sha1(bFullFile).hexdigest(), "hex"), "base64").decode()
