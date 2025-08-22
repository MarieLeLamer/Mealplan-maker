from zipfile import ZipFile
import json

def openZippedFile(unFichierRtk, uneCle):
    with unFichierRtk.open(uneCle) as jsonFile:
        return json.load(jsonFile)
    
    
def importCle(uneCle):
    with ZipFile('recipes.rtk', 'r') as myzip:
        return openZippedFile(myzip, uneCle)

if __name__ == "__main__":
    print(importCle('tags.json'))