import pandas as pd

df = pd.read_excel ('C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\dataset\\sample_dataset.xlsx', index_col=0)
# print(df)

df = pd.read_excel("C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\dataset\\sample_dataset.xlsx", usecols = ['RECIPENAME'])
dataa=df.RECIPENAME
# print(dataa)
recipelist=[]
for i in dataa:
    # print(i)
    recipelist.append(i)
# print(recipelist)

###############################################################distict incredients---------------------------

dff = pd.read_excel("C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\dataset\\sample_dataset.xlsx", usecols = ['INGREDIENTS'])
data=dff.INGREDIENTS
# print(data)
inclist=[]
for i in data:

    try:
        d1=i.split(",")
        for inc in d1:
            # result = ''.join([i for i in inc if not i.isdigit()])
            inclist.append(inc)

    except:
        pass
unique_list = []
for x in inclist:
    if x in unique_list:
        pass
    else:
        unique_list.append(x)
# print("UNIQ------------",unique_list)





#--------------------------------url----------------------

dff = pd.read_excel("C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\dataset\\sample_dataset.xlsx", usecols = ['RECIPEURL'])
data=dff.RECIPEURL
print(data)
# urllist = []
# for i in data:
#     urllist.append(i)
# print(urllist)

#-------------------------------

dff = pd.read_excel("C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\dataset\\sample_dataset.xlsx",
                    usecols=['DESCRIPTION'])
data = dff.DESCRIPTION
print(data)
descriptionlist = []
for i in data:
    descriptionlist.append(i)
print(descriptionlist)
#----------------------------------


dff = pd.read_excel("C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\dataset\\sample_dataset.xlsx", usecols = ['INGREDIENTS'])
data=dff.INGREDIENTS

mainlist=[]
for i in data:
    inclist = []

    try:

        d1=i.split(",")
        for inc in d1:
            # result = ''.join([i for i in inc if not i.isdigit()])
            inclist.append(inc)
        mainlist.append(inclist)



    except:
        pass
# print(mainlist)
# print("--------------------------------------------------------")

ok=[]
for i in mainlist:
    d1=""
    print(i)
    for j in i:
        d1+=j

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




