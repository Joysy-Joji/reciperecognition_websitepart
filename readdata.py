import pandas as pd
# res=pd.read_csv('C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\recipe dataset.csv', index_col=0)
# print(res)


df = pd.read_csv("C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\recipedataset _ orginal.csv", usecols = ['TranslatedIngredients'])
data=df.TranslatedIngredients
# print(data)
inclist=[]
for i in data:
    # print(i.split(","))
    try:
        d1=i.split(",")
        for inc in d1:
            result = ''.join([i for i in inc if not i.isdigit()])
            inclist.append(result)

    except:
        pass
icre_list=[]
for i in inclist:

    d1 = i.split("-")

    d2= d1[0].replace("/","").replace("teaspoon","").replace("tablespoon","").replace("cup","").replace(" ","").replace("Water","").replace("to","").replace("kg","").replace("s","").replace("cup","").replace("gram","").replace("inch","").replace("pinch","").replace("नमक","")
    d3=d2.split("(")
    # d4=d3.split(")")
    print(d3)

    # am=[]
    # icre_list.append(d3[0])
    # print(icre_list[0])
unique_list = []

for x in icre_list:
        if x  in unique_list:
            pass
        else:
            unique_list.append(x)
        # print("**********************************************************************************************",unique_list)

#================================item========================================================================================

df1 = pd.read_csv("C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\recipedataset _ orginal.csv", usecols = ['TranslatedRecipeName'])
data1=df1.TranslatedRecipeName
# print(data)
recipelist=[]
for i in data1:
    # print(i)
    # recplist=[]
    a=i.split("-")
    b = a[0].replace(" ", "")
    recipelist.append(b)
# print(recipelist)

########################################################################################
df = pd.read_csv("C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\recipedataset _ orginal.csv", usecols = ['TranslatedIngredients'])
data=df.TranslatedIngredients
# print(data)
mainlist=[]
for i in data:
    inclist = []
    # print(i.split(","))
    try:
        # print(i)
        d1=i.split(",")
        for inc in d1:
            result = ''.join([i for i in inc if not i.isdigit()])
            inclist.append(result)
        mainlist.append(inclist)



    except:
        pass
# print(mainlist)
print("--------------------------------------------------------")
for i in mainlist:

    print(i)
    # d1 = i.split(",")
    d2= d1[0].replace("/","").replace("teaspoon","").replace("tablespoon","").replace("cup","").replace(" ","").replace("Water","")

    # print(d2)