import pandas as pd
# res=pd.read_csv('C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\recipe dataset.csv', index_col=0)
# print(res)


df = pd.read_csv("C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\p.csv", usecols = ['TranslatedIngredients'])
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

    d2= d1[0].replace("/","").replace("teaspoon","").replace("tablespoon","").replace(" cup","").replace(" ","").replace("Water","").replace("to","").replace("kg","").replace("s","").replace("cup","").replace("gram","").replace("inch","").replace("pinch","").replace("नमक","").replace("-/","").replace("-/","").replace("-","").replace("/","").replace("Water","")
    d3=d2.split("(")
    # d4=d3.split(")")
    # print(d3)

    # am=[]
    icre_list.append(d3[0])
    # print(icre_list[0])
unique_list = []

for x in icre_list:
        if x  in unique_list:
            pass
        else:
            unique_list.append(x)
print("**********************************************************************************************unique",unique_list)

#================================item========================================================================================

df1 = pd.read_csv("C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\p.csv", usecols = ['TranslatedRecipeName'])
data1=df1.TranslatedRecipeName
# print(data)
import math
recipelist=[]
for i in data1:
    print(i,type(i),"--------------------")
    # recplist=[]

    try:
        a=i.split("-")
        b = a[0].replace(" ", "")
        recipelist.append(b)
    except:
        pass

# print(recipelist)

########################################################################################
df = pd.read_csv("C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\p.csv", usecols = ['TranslatedIngredients'])
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
print(mainlist)
print("--------------------------------------------------------")
ok=[]
for i in mainlist:
    d1=""
    print(i)
    for j in i:
        d1+=j.replace("/","").replace("teaspoon","").replace("tablespoon","").replace(" cup","").replace(" ","").replace("Water","").replace("-/","").replace("-","").replace("/","")     +","

    print(d1)
    ok.append(d1)


print("terererereer")
print("**************************************************************")
print(ok)

print("terererereer")
print("**************************************************************")
print(len(ok),len(recipelist))


print("**************************************************************")
# for i in ok:
#     print(i)

vectors=[]
print(unique_list)
for i in range(len(recipelist)):
    vv=[]
    for j in range(len(unique_list)):
        # print("-------------")
        p=ok[i].split(",")


        if unique_list[j] in p:
            print(unique_list[j],"======")
            vv.append(1)
        else:
            vv.append(0)
    vectors.append(vv)

print("*********************Vector")
print(vectors)




# --------------------------------------
print(len(unique_list),"llllllllllllllllllllllllllllllllllllllllll")
oo=vectors[0]
print(type(oo))
print(len(oo))


