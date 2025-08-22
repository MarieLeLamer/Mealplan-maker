from recipesImporter import importCle

def getTagsDict():
    tags = {}
    importedTags = importCle('tags.json')
    for i in importedTags:
        tags[i['title']] = [] 
    return tags

def getRecipesDict():
    uuidRecipes = {}
    recipes = importCle("recipes_0.json")
    for i in recipes: 
        if {'title': 'Plat'} in i['categories'] :
            uuidRecipes[i["uuid"]] = i 
    return uuidRecipes

def populateTagDictWithRecipesDict(tagDict, recipesDict):
    for i in recipesDict: #
        for tags in recipesDict[i]["tags"]: 
            tagDict[tags["title"]].append(i) #

if __name__ == "__main__":
    dictionnaryOfTags = getTagsDict()
    dictionnaryOfRecipes = getRecipesDict()

    populateTagDictWithRecipesDict(dictionnaryOfTags, dictionnaryOfRecipes)
    print(dictionnaryOfTags) 