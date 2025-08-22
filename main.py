import random
import uvicorn
from getTags import getTagsDict, getRecipesDict, populateTagDictWithRecipesDict
from seasons import get_season
from fastapi import FastAPI, UploadFile, Response, status
from typing import Union
from fastapi.staticfiles import StaticFiles

app = FastAPI()
app.mount("/static", StaticFiles(directory="public"), name="static")

@app.get("/getMenu")
def read_root():
    print("oklm")
    return makeWeekMenu()

@app.post("/loadFile")
async def  loadFileRoute(file: UploadFile, response: Response):
    if(file.filename.split('.')[-1]== 'rtk'):
        with open('recipes.rtk','wb') as f:
            f.write(file.file.read())
        return {"file_name": file.filename}
    else :
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {'erreur' : 'Veuillez uploader un fichier .rtk'}

dictionnaryOfTags = getTagsDict()
dictionnaryOfRecipes = getRecipesDict()
populateTagDictWithRecipesDict(dictionnaryOfTags, dictionnaryOfRecipes)


def filterFood(listOfRecipes, wantIt, listOfRecipiesToFilter):
    foodFiltered = []
    for i in listOfRecipes: 
        if wantIt:
            if i in listOfRecipiesToFilter:
                foodFiltered.append(i)
        else:
            if i not in listOfRecipiesToFilter:
                foodFiltered.append(i)
    return foodFiltered

def getNameOfRecipe(uuid):
    return dictionnaryOfRecipes[uuid]["title"].strip()

def makeMenu(meal, wantIt, bannedFood, vegetarian=False):
    currentSeason = get_season()
    listOfPossibleFood = filterFood(dictionnaryOfTags[meal], wantIt, bannedFood)
    listOfPossibleFood = filterFood(listOfPossibleFood, False, bannedFood)
    listOfPossibleFood = filterFood(listOfPossibleFood, True, dictionnaryOfTags[currentSeason])

    if vegetarian:
        listOfPossibleFood = filterFood(listOfPossibleFood, True, dictionnaryOfTags['Végétarien'])

    chosenFood = random.choice(listOfPossibleFood)
    bannedFood.append(chosenFood)
    print(dictionnaryOfRecipes[chosenFood])
    return {
        "id": chosenFood,
        "ingredients": dictionnaryOfRecipes[chosenFood]["ingredients"]
    }

def makeWeekMenu():
    bannedFood = []
    lundiMardiMidi = makeMenu('Midi', False, bannedFood, vegetarian=True)
    lundiMardiSoir = makeMenu('Soir', False, bannedFood, vegetarian=True)
    mercrediJeudiMidi = makeMenu('Midi', False, bannedFood)
    mercrediJeudiSoir = makeMenu('Soir', False, bannedFood)
    vendrediSamediMidi = makeMenu('Midi', False, bannedFood, vegetarian=True)
    # vendrediSamediSoir = makeMenu('Soir', True, bannedFood, vegetarian=False)
    listeCourses = lundiMardiMidi["ingredients"] + '\n' + lundiMardiSoir["ingredients"] + ' \n' + mercrediJeudiMidi["ingredients"] + '\n' + mercrediJeudiSoir["ingredients"] + '\n' + vendrediSamediMidi["ingredients"] + '\n'



    return {'Lundi Mardi midi' : getNameOfRecipe(lundiMardiMidi["id"]), 
'Lundi mardi soir' : getNameOfRecipe(lundiMardiSoir["id"]),
'Mercredi Jeudi midi' : getNameOfRecipe(mercrediJeudiMidi["id"]),
'Mercredi Jeudi soir' : getNameOfRecipe(mercrediJeudiSoir["id"]),
'Vendredi Samedi midi' : getNameOfRecipe(vendrediSamediMidi["id"]),
# 'Vendredi Samedi soir' : getNameOfRecipe(vendrediSamediSoir["id"]),
'liste_courses': listeCourses}


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')