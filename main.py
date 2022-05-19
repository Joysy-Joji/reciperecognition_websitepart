import tensorflow as tf, sys
import pandas as pd
from flask import Flask, render_template, request, session, jsonify
from DBConnection import Db
from sklearn.ensemble import RandomForestClassifier
app=Flask(__name__)
app.secret_key="kk"
staticpath="C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\"

@app.route('/admin_index')
def admin_index():
    return render_template('admin/admin_index.html')

@app.route('/admin_home')
def admin_home():
    return render_template('admin/admin_home.html')


@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/store_index')
def store_index():
    return render_template('store/store_index.html')

@app.route('/Login')
def login():
    return render_template('Login.html')

@app.route('/login_post',methods=['post'])
def login_post():
    name=request.form['textfield']
    password=request.form['textfield2']
    db=Db()
    qry="select * from login where username='"+name+"' and password='"+password+"'"
    res=db.selectOne(qry)
    if res!=None:
        session["lid"]=res["login_id"]
        if res['type']=='admin':
            return adminhome()
        elif res['type']=='store':
            return storehome()
        else:
            return '''<script> alert('User not allowed'); window.location='/' </script>'''
    else:
        return '''<script> alert('Invalid username or password'); window.location='/' </script>'''
        
            
    
#----------------------------------Android
@app.route('/userregister_post',methods=['post'])
def userlogin_post():
    type = "user"
    name = request.form['name']
    place = request.form['place']
    post = request.form['post']
    pin = request.form['pin']
    housename = request.form['housename']
    email = request.form['email']
    mobileno = request.form['mobileno']
    password = request.form['password']
    q = "insert into login(username,password,type)values('" + name + "','" + password + "','" + type + "')"
    db = Db()
    lid = db.insert(q)
    qry = "insert into user_register(name,place,post,pin,house_name,email,mobile_no,password,login_id)values('" + name + "','" + place + "','" + post+ "','" + pin + "','" + housename + "','" + email + "','" + mobileno + "','" + password + "','" +str(lid) + "')"
    res = db.insert(qry)
    return jsonify(status="ok")

@app.route('/product_store',methods=['post'])
def product_store():
    db = Db()
    qry = "SELECT product.image AS p_image,product.name AS p_name,`product`.*, storeregister.name AS s_name,`storeregister`.* FROM `storeregister` INNER JOIN `product` ON `product`.`store_id`=`storeregister`.`login_id`"
    res = db.select(qry)

    # print(res)
    return jsonify(status="ok",data=res)
@app.route('/search_product',methods=['post'])
def search_product():
    db = Db()
    s=request.form['product']
    print(s)
    qry = "SELECT product.image AS p_image,product.name AS p_name,`product`.*, storeregister.name AS s_name,`storeregister`.* FROM `storeregister` INNER JOIN `product` ON `product`.`store_id`=`storeregister`.`login_id`  AND product.name='"+s+"'"
    res = db.select(qry)

    # print(res)
    return jsonify(status="ok",data=res)

@app.route('/search_recipe',methods=['post'])
def search_recipe():
    dff = pd.read_excel("C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\dataset\\sample_dataset.xlsx",
                        usecols=['RECIPENAME'])
    data = dff.RECIPENAME
    # print(data)
    namelist = []
    for i in data:
        namelist.append(i)

    # print("------------------------------------0000---------------------------",namelist)
    df = pd.read_excel("C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\dataset\\sample_dataset.xlsx",
                        usecols=['RECIPEURL'])
    dataa = df.RECIPEURL
    # print(data)
    urllist = []
    for i in dataa:
        urllist.append(i)
    dff = pd.read_excel("C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\dataset\\sample_dataset.xlsx",
                           usecols=['INGREDIENTS'])

    data = dff.INGREDIENTS
    inglist=[]
    for i in data:
        inglist.append(i)
    dfff = pd.read_excel("C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\dataset\\sample_dataset.xlsx",
                        usecols=['DESCRIPTION'])
    dataaa = dfff.DESCRIPTION
    deslist=[]
    for i in dataaa:
        deslist.append(i)
    s = []
    for ss in range(0,len(namelist)):
        s.append({"recipe":namelist[ss],"ingredients":inglist[ss],"url":urllist[ss],"desc":deslist[ss]})
        print("------------------",inglist[ss])
    return jsonify(status="ok",k=namelist,ress=namelist,ingds=inglist,urls=urllist,descs=deslist,mydata=s)




@app.route('/image_post',methods=['post'])
def image_post():

    image = request.form['img']
    import time , datetime
    from encodings.base64_codec import base64_decode
    import base64

    a = base64.b64decode(image)
    fh = open("C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\vegetabletest\\abc.jpg", "wb")

    fh.write(a)
    fh.close()
    print("...")

    print("mmmm")
    fn = "C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\vegetabletest\\abc.jpg"
    image_data = tf.gfile.FastGFile(fn, 'rb').read()
    label_lines = [line.rstrip() for line
                   in tf.gfile.GFile(
            "C:\\Users\\user\\PycharmProjects\\reciperecognation\\logs\\output_labels.txt")]
    print("started")
    # Unpersists graph from file
    with tf.gfile.FastGFile(
            "C:\\Users\\user\\PycharmProjects\\reciperecognation\\logs\\output_graph.pb",
            'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')

    with tf.Session() as sess:
        # Feed the image_data as input to the graph and get first prediction
        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

        predictions = sess.run(softmax_tensor, \
                               {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
        print("OOOOOOOOOOOOO")
        print(predictions)
        print("topk", top_k)
        human_string = []
        s=[]
        for node_id in top_k:
            score = predictions[0][node_id] * 100
            score = round(score)

            print("score---",score,predictions[0][node_id],node_id)

            s.append(label_lines[node_id])
            print("s--",s)

            if score > 20.0:
                # self.lb3.setText("the alphabet is  " + human_string)
                # QMessageBox.about(self,"Classification", "The alphabet is-"+human_string+"," +str(score) + "")

                print('%s.\n\nAlgorithm confidence = %.5f' % (human_string, score))

                # human_string.append(label_lines[node_id])

                val=label_lines[node_id]
                print("human_string", human_string)
                result = ""
                if val == "1":
                    result = "raw banana"
                    human_string.append(result)
                if val == "2":
                    result = "beans"
                    human_string.append(result)
                if val == "3":
                    result = "beetroot"
                    human_string.append(result)
                if val == "4":
                    result = "bitter gourd"
                    human_string.append(result)
                if val == "5":
                    result = "brinjal"
                    human_string.append(result)
                if val == "6":
                    result = "brocoli"
                    human_string.append(result)
                if val == "7":
                        result = "cabbage"
                        human_string.append(result)
                if val == "8":
                    result = "capsicum"
                    human_string.append(result)
                if val== "9":
                        result = "carrot"
                        human_string.append(result)
                if val == "10":
                    result = "cauliflower"
                    human_string.append(result)
                if val == "18":
                        result = "lady finger"
                        human_string.append(result)
                if val == "19":
                    result = "onion"
                    human_string.append(result)
                if val == "20":
                        result = "potato"
                        human_string.append(result)
                if val == "21":
                    result = "pumpkin"
                    human_string.append(result)
                if val == "25":
                        result = "tomato"
                        human_string.append(result)






    print(human_string)
    resqq=[]
    for i in human_string:
        resqq.append(i.lower())
        print(resqq)


    print(resqq,"*****************")
    resq=""
    for i in human_string:
        resq = resq + "\n " + i
    print(resq, "*****************")


    #--------------------------RECIPE URL------------------
    dff = pd.read_excel("C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\dataset\\sample_dataset.xlsx",
                        usecols=['RECIPEURL'])
    data = dff.RECIPEURL
    # print(data)
    urllist = []
    for i in data:

        urllist.append(i)
    print(urllist)



    #-----------------------RECIPE DESCRIPTION-----------------
    dff = pd.read_excel("C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\dataset\\sample_dataset.xlsx",
                        usecols=['DESCRIPTION'])
    data = dff.DESCRIPTION
    descriptionlist = []
    for i in data:
        descriptionlist.append(i)
    print(descriptionlist)






    dff = pd.read_excel("C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\dataset\\sample_dataset.xlsx",
                        usecols=['INGREDIENTS'])
    data = dff.INGREDIENTS
    # print(data)
    inclist = []
    for i in data:
        try:
            d1 = i.split(",")
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
    print("UNIQ------------", unique_list)

    vectorstest = []
    print(unique_list)

    vv = []
    for j in range(len(unique_list)):
        # print("-------------")
        # p = res.split(",")

        if unique_list[j] in resq:
            print(unique_list[j], "======")
            vv.append(1)
        else:
            vv.append(0)
    vectorstest.append(vv)
    print("_________________vectortest",resq)
    print(vectorstest)
    # #______________________________Recepie list______________________________________
    df = pd.read_excel("C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\dataset\\sample_dataset.xlsx",
                       usecols=['RECIPENAME'])
    data1 = df.RECIPENAME
    # print(data)
    import math
    recipelist = []
    for i in data1:
        print(i, type(i), "--------------------")
        # recplist=[]

        try:
            a = i.split("-")
            b = a[0]
            recipelist.append(b)
        except:
            pass
    print(recipelist)
    # #_______________________________________________________recepie list end___________________
    # #______________________________________________________traning icrediance vector_______________________
    dff = pd.read_excel("C:\\Users\\user\\PycharmProjects\\reciperecognation\\static\\dataset\\sample_dataset.xlsx",
                        usecols=['INGREDIENTS'])
    data = dff.INGREDIENTS

    # print(data)
    mainlist = []
    for i in data:
        inclist = []
        # print(i.split(","))
        try:
            # print(i)
            d1 = i.split(",")
            for inc in d1:
                result = ''.join([i for i in inc if not i.isdigit()])
                inclist.append(result)
            mainlist.append(inclist)



        except:
            pass


    lst=[]
    recid=[]
    ingd=[]
    urls=[]
    descs=[]
    # c=0
    for i in range(len(recipelist)):
        c = 0
        recipe=recipelist[i]
        myinc=mainlist[i]
        ur=urllist[i]
        dd=descriptionlist[i]
        print("recipe",recipe,"myinc",myinc)

        for i in myinc:
            if i in resq:
                c=c+1
        if c>0:
            lst.append(c)
            recid.append(recipe)
            ingd.append(myinc)
            urls.append(ur)
            descs.append(dd)

    print(lst)
    print("cntrrrrr")
    for i in range(len(recid)):
        for j in range(len(recid)):
            if lst[i]> lst[j]:
                temp=recid[i]
                recid[i]=recid[j]
                recid[j]=temp

                temp=lst[i]
                lst[i]=lst[j]
                lst[j]=temp

                temp=ingd[i]
                ingd[i]=ingd[j]
                ingd[j]=temp

                temp = urls[i]
                urls[i] = urls[j]
                urls[j] = temp

                temp = descs[i]
                descs[i] = descs[j]
                descs[j] = temp

    s=[]
    for ss in range(len(recid)):
        a={"recipe":recid[ss],"ingredients":ingd[ss],"url":urls[ss],"desc":descs[ss]}
        s.append(a)

    print(s)
    ing_v=str(ingd)
    print("-------9999------",ing_v)


    return jsonify(status="ok",res=recid,ingds=ingd,ress=resq,urls=urls,descs=descs,mydata=s)

@app.route('/user_viewprofile',methods=['post'])
def user_viewprofile():
     lid=request.form["lid"]
     db=Db()
     qry="select * from user_register where login_id='"+lid+"'"
     res=db.selectOne(qry)

     return jsonify(status="ok",name=res['name'],place=res['place'],post=res['post'],pin=res['pin'],house_name=res['house_name'],mobile_no=res['mobile_no'],email=res['email'])

@app.route('/userlogin_post1', methods=['post'])
def userlogin_post1():
    name = request.form['name']
    password = request.form['password']
    db = Db()
    qry = "select * from login where username='" + name + "' and password='" + password + "'"
    res = db.selectOne(qry)
    if res != None:
        # session["lid"] = res["login_id"]
        if res['type'] == 'user':
            return jsonify(status="ok",lid=res["login_id"])
    else:
        return jsonify(status="invalid")


@app.route('/adminhome')
def adminhome():
    return render_template('admin/admin_home.html')


@app.route('/storehome')
def storehome():
    return render_template('store/store_main_home.html')



@app.route('/deleteVegetables/<id>')
def deleteVegetables(id):
    db=Db()
    qry="delete from vegetable where veg_id='"+str(id)+"'"
    res=db.delete(qry)
    return 'ok'

@app.route('/SearchVegetables',methods=['post'])
def SearchVegetables():
    n=request.form['textfield']
    db = Db()
    qry = "select * from vegetable where name like '%"+n+"%' "
    res = db.select(qry)
    return render_template('admin/ViewVegetables.html', data=res)

@app.route('/Reply')
def reply():
    return render_template('admin/Reply.html')

# @app.route('/Reply_post',methods=['post'])
# def Reply_post():
#     reply = request.form['textarea']
#
#     db=Db()
#     qry="insert into complaint(reply)values('"+reply+"')"
#     res=db.insert(qry)
#     return 'ok'

@app.route('/AddVegetables')
def AddVegetables():
   return render_template('admin/AddVegetables.html')
@app.route('/AddVegetables_post',methods=['post'])
def AddVegetables_post():
    name = request.form['textfield']

    image = request.files['file']
    # storelid=session["lid"]
    import datetime
    dt=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    image.save(staticpath+"veg\\"+dt+".jpg")
    path="/static/veg/"+dt+".jpg"
    db=Db()
    qry="insert into vegetable(name,image)values('"+name+"','"+path+"')"
    res=db.insert(qry)
    return 'ok'
@app.route('/EditVegetables/<id>')
def EditVegetables(id):
    db=Db()
    qry="select * from vegetable where veg_id='"+str(id)+"'"
    res=db.selectOne(qry)
    return render_template('admin/EditVegetables.html',data=res)
@app.route('/EditVegetables_post',methods=['post'])
def EditVegetables_post():
    id = request.form['id']
    veg_name = request.form['textfield']
    veg_color = request.form['textfield2']
    veg_shape = request.form['textfield3']
    veg_size = request.form['textfield4']
    veg_texture = request.form['textfield5']
    image = request.files['file']
    import datetime
    dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    image.save(staticpath + "veg\\" + dt + ".jpg")
    path = "/static/veg" + dt + ".jpg"
    db = Db()
    qry = "update vegetable set name='" + veg_name + "', color='" + veg_color + "',shape='" + veg_shape + "',size='" + veg_size + "',texture='" + veg_texture + "',image='" + path + "' where veg_id='"+str(id)+"' "
    res = db.update(qry)
    return 'ok'
@app.route('/EditProduct/<id>')
def EditProduct(id):
    db=Db()
    qry="select * from product where product_id='"+str(id)+"'"
    res=db.selectOne(qry)
    return render_template('store/EditProduct.html',data=res)
@app.route('/EditProduct_post',methods=['post'])
def EditProduct_post():
    id = request.form['id']
    product_name = request.form['textfield']
    product_price = request.form['textfield2']
    prodcut_stock = request.form['textfield3']
    product_madedate = request.form['textfield4']
    image = request.files['file']
    # import datetime
    # dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    # image.save(staticpath + "store\\" + dt + ".jpg")
    # path = "/static/store" + dt + ".jpg"
    # db = Db()
    # qry = "update product set name='" + product_name + "', price='" + product_price + "',stock='" + prodcut_stock + "',made_date='" + product_madedate + "',image='" + path + "' where product_id='"+str(id)+"' "
    # res = db.update(qry)
    storeid = session["lid"]

    if 'file' in request.files:
        image = request.files['file']
        if image.filename != '':
            import datetime
            dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            image.save(staticpath + "store\\" + dt + ".jpg")
            path = "/static/store/" + dt + ".jpg"
            db = Db()
            qry = "update product set name='" + product_name + "',price='" + product_price + "',stock='" +prodcut_stock + "',made_date='" + product_madedate + "',image='" + path + "'where product_id='" + str(id) + "'"
            res = db.update(qry)
            return '''<script>alert('Updated');window.location='/ViewProduct'</script>'''
        else:
            db = Db()
            qry = "update product set name='" + product_name + "',price='" + product_price + "',stock='" + prodcut_stock + "',made_date='" + product_madedate + "'where product_id='" + str(id) + "'"
            res = db.update(qry)
            return '''<script>alert('Updated');window.location='/ViewProduct'</script>'''
    else:
        db = Db()
        qry = "update product set name='" + product_name + "',price='" + product_price + "',stock='" + prodcut_stock + "',made_date='" + product_madedate +  "' where product_id='" + str(id) + "'"
        res = db.update(qry)
        return '''<script>alert('Updated');window.location='/ViewProduct'</script>'''


@app.route('/EditRecipe/<id>')
def EditRecipe(id):
    db=Db()
    qry="select * from recipe where recipe_id='"+str(id)+"'"
    res=db.selectOne(qry)
    return render_template('admin/edit_recipe.html',data=res)
@app.route('/EditRecipe_post',methods=['post'])
def EditRecipe_post():
    id = request.form['id']
    recipe_name = request.form['textfield']
    recipe_description = request.form['textarea']
    recipe_ingredients = request.form['textarea2']

    image = request.files['file']
    import datetime
    dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    image.save(staticpath + "recipe\\" + dt + ".jpg")
    path = "/static/recipe" + dt + ".jpg"
    db = Db()
    qry = "update recipe set name='" + recipe_name + "', description='" + recipe_description + "',ingredients='" + recipe_ingredients + "'where recipe_id='"+str(id)+"' "

    res = db.update(qry)

    return 'ok'




@app.route('/Reply')
def Reply():
    return render_template('admin/Reply.html')
@app.route('/Reply_post',methods=['post'])
def Reply_post():
    reply = request.form['textarea']
    db = Db()
    qry = "insert into complaint(reply)values('" + reply + "')"
    res = db.insert(qry)





    return 'ok'
@app.route('/deleteRecipe/<id>')
def deleteRecipe(id):
    db = Db()
    qry = "delete from recipe where recipe_id='" + str(id) + "'"
    res = db.delete(qry)
    return 'ok'

@app.route('/SearchRecipe',methods=['post'])
def SearchRecipe():
    n=request.form['textfield']
    db = Db()
    qry = "select * from recipe where name like '%"+n+"%'"
    res = db.select(qry)
    return render_template('admin/ViewRecipe.html', data=res)


@app.route('/UploadRecipe')
def UploadRecipe():
    return render_template('admin/UploadRecipe.html')
@app.route('/UploadRecipe_post',methods=['post'])
def UploadRecipe_post():
    name = request.form['textfield']
    description = request.form['textarea']
    ingredients = request.form['textarea']
    image = request.files['file']
    import datetime
    dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    image.save(staticpath + "recipe\\" + dt + ".jpg")
    path = "/static/recipe" + dt + ".jpg"
    db = Db()
    qry = "insert into recipe(name,description,ingredients,image)values('" + name + "','" + description + "','" + ingredients + "','"+ path + "')"
    res = db.insert(qry)
    return 'ok'

@app.route('/SearchComplaints',methods=['post'])
def SearchComplaints():
    n = request.form['f_date']
    m = request.form['t_date']
    print(n,m)
    db = Db()
    qry = "select * from review INNER JOIN `user_register` ON `user_register`.`login_id`=`review`.`user_id` where date between '"+n+"' and '"+m+"'"
    res = db.select(qry)
    return render_template('admin/ViewComplaints.html', data=res)

@app.route('/ViewComplaints')
def ViewComplaints():
    db = Db()
    qry = "SELECT * FROM  review INNER JOIN `user_register` ON `user_register`.`login_id`=`review`.`user_id`"
    res = db.select(qry)
    ls = []
    for i in res:
        ss = i['date']
        yy = str(ss)
        cc = yy.split("-")
        print(cc)
        so_date = cc[2] + "-" + cc[1] + "-" + cc[0]
        print(so_date)
        ls.append(
            {"name": i['name'], "date": so_date, "email": i['email'],
             "mobile_no": str(i['mobile_no']), "content": i['content'],"place": i['place']})
    return render_template('admin/ViewComplaints.html', data=ls)


# return render_template('admin/ViewComplaints.html',data=res)
@app.route('/ViewUsers')
def ViewUsers():
    db = Db()
    qry = "SELECT * FROM  user_register INNER JOIN `login` ON `login`.`login_id`=`user_register`.`login_id`"
    res = db.select(qry)
    return render_template('admin/viewusers.html',data=res)
@app.route('/ViewStoredetails')
def ViewStoredetails():
    db = Db()
    qry = "SELECT * FROM  storeregister INNER JOIN `login` ON `login`.`login_id`=`storeregister`.`login_id`"
    res = db.select(qry)
    return render_template('admin/viewstoredetails.html',data=res)
@app.route('/ViewComplaints_post',methods=['post'])
def ViewComplaints_post():
    return 'ok'


@app.route('/ViewRecipe')
def ViewRecipe():
    db = Db()
    qry = "select * from recipe"
    res = db.select(qry)
    return render_template('admin/ViewRecipe.html', data=res)


@app.route('/ViewRecipe_post',methods=['post'])
def ViewRecipe_post():
    name = request.form['textfield']
    return 'ok'


@app.route('/SearchStore',methods=['post'])
def SearchStore():
    n=request.form['textfield']
    a = request.form['textfield2']
    db = Db()
    qry = "select * from storeregister where name like '%"+n+"%' and place like '%"+a+"%'"
    res = db.select(qry)
    return render_template('admin/vvstore.html', data=res)

@app.route('/Searchuser',methods=['post'])
def Searchuser():
    n=request.form['textfield']
    a = request.form['textfield2']
    db = Db()
    qry = "select * from user_register where name like '%"+n+"%' and place like '%"+a+"%'"
    res = db.select(qry)
    return render_template('admin/viewusers.html', data=res)

@app.route('/SearchStore_approved',methods=['post'])
def SearchStore_approved():
    n=request.form['textfield']
    a = request.form['textfield2']
    db = Db()
    qry = "select * from storeregister where name like '%"+n+"%' and place like '%"+a+"%' and status='approved'"
    res = db.select(qry)
    return render_template('admin/ViewStoresapproved.html', data=res)

@app.route('/ViewStore')
def ViewStore():
    db = Db()
    qry = "select * from storeregister  order by store_id desc"
    res = db.select(qry)
    print(qry)
    return render_template('admin/vvstore.html',data=res)

@app.route('/ViewStore_approved')
def ViewStore_approved():
    db = Db()
    qry = "select * from storeregister where status='approved' order by store_id desc"
    res = db.select(qry)
    print(qry)
    return render_template('admin/ViewStoresapproved.html',data=res)
@app.route('/reject_store/<id>')
def reject_store(id):
    db = Db()
    qry = "update storeregister set status='rejected' where store_id ='"+id+"'"
    res = db.update(qry)
    print(qry)
    return '''<script>alert('success');window.location='/ViewStore'</script>'''
@app.route('/approve_store/<id>')
def approve_store(id):
    db = Db()
    qry = "update storeregister set status='approved' where store_id ='"+id+"'"
    res = db.update(qry)
    print(qry)
    return '''<script>alert('success');window.location='/ViewStore'</script>'''

@app.route('/ViewStore_post',methods=['post'])
def ViewStore_post():
    name = request.form['textfield']
    address = request.form['textfield2']
    return 'ok'



@app.route('/ViewVegetables')
def ViewVegetables():
    db=Db()
    qry="select * from vegetable"
    res=db.select(qry)

    return render_template('admin/ViewVegetables.html',data=res)





@app.route('/ViewVegetables_post',methods=['post'])
def ViewVegetables_post():
    name = request.form['textfield']
    return 'ok'





@app.route('/AcceptStore')
def AcceptStore():
    return 'ok'
@app.route('/RejectStore/<id>')
def RejectStore(id):
    db = Db()
    qry = "delete from storeregister where store_id='" + str(id) + "'"
    res = db.delete(qry)
    return 'ok'

@app.route('/Storeregistration')
def Storeregistration():
    return render_template('store/Storeregistration.html')


@app.route('/Storeregistration_post',methods=['post'])
def Storeregistration_post():
    type="store"
    name = request.form['textfield']
    place = request.form['textfield2']
    post = request.form['textfield3']
    pin = request.form['textfield4']
    mobilenumber = request.form['textfield5']
    email = request.form['textfield6']
    password = request.form['textfield7']
    image = request.files['file']

    import datetime
    dt=datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    image.save(staticpath+"store\\"+dt+".jpg")
    path="/static/store/"+dt+".jpg"
    db=Db()
    q="insert into login(username,password,type)values('"+name+"','"+password+"','"+type+"')"
    lid = db.insert(q)
    qry="insert into storeregister(name,place,post,pin,mobilenumber,email,password,image,login_id)values('"+name+"','"+place+"','"+post+"','"+pin+"','"+mobilenumber+"','"+email+"','"+password+"','"+path+"','"+str(lid)+"')"
    res=db.insert(qry)

    # return render_template('store/store_index.html')
    return '''<script> alert('Registered Succusfully '); window.location='/Login'</script>'''

@app.route('/deleteProduct/<id>')
def deleteProduct(id):
    db = Db()
    qry = "delete from product where product_id='" + str(id) + "'"
    res = db.delete(qry)

    return ViewProduct()




@app.route('/ViewProfile')
def ViewProfile():
    db = Db()
    qry = "select * from storeregister where login_id='"+str(session["lid"])+"'"
    res = db.selectOne(qry)
    return render_template('store/ViewProfile.html',data=res)

@app.route('/edit_profile/<id>')
def edit_profile(id):
    db=Db()
    qry="select * from storeregister where store_id='"+id+"'"
    res=db.selectOne(qry)

    return render_template('store/edit_profile.html',data=res)

@app.route('/edit_profile_post',methods=['post'])
def edit_profile_post():
    s_id = request.form['s_id']
    name = request.form['textfield']
    place = request.form['textfield2']
    post = request.form['textfield3']
    pin = request.form['textfield4']
    mobilenumber = request.form['textfield5']
    email = request.form['textfield6']

    if 'file' in request.files:
        image = request.files['file']
        if image.filename!='':
            import datetime
            dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            image.save(staticpath + "store\\" + dt + ".jpg")
            path = "/static/store/" + dt + ".jpg"
            db = Db()
            qry = "update storeregister set name='" + name + "',place='" + place + "',post='" + post + "',pin='" + pin + "',mobilenumber='" + mobilenumber + "',email='" + email + "',image='" + path + "'where store_id='" + str(s_id) + "'"
            res = db.update(qry)
            return '''<script>alert('Updated');window.location='/ViewProfile'</script>'''
        else:
            db = Db()
            qry = "update storeregister set name='" + name + "',place='" + place + "',post='" + post + "',pin='" + pin + "',mobilenumber='" + mobilenumber + "',email='" + email + "' where store_id='" + str(s_id) + "'"
            res = db.update(qry)
            return '''<script>alert('Updated');window.location='/ViewProfile'</script>'''
    else:
        db = Db()
        qry = "update storeregister set name='" + name + "',place='" + place + "',post='" + post + "',pin='" + pin + "',mobilenumber='" + mobilenumber + "',email='" + email + "' where store_id='" + str(s_id) + "'"
        res = db.update(qry)
        return '''<script>alert('Updated');window.location='/ViewProfile'</script>'''




@app.route('/AddProduct')
def AddProduct():
    c=Db()
    qry="SELECT CURDATE() AS cur"
    res=c.selectOne(qry)
    return render_template('store/AddProduct.html',cur=res['cur'])
@app.route('/AddProduct_post',methods=['post'])
def AddProduct_post():

    name = request.form['textfield']
    price = request.form['textfield2']
    stock = request.form['textfield3']
    made_date = request.form['textfield4']
    image = request.files['file']
    # storelid = session["lid"]
    import datetime
    dt = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    dte = datetime.datetime.now().strftime('%d-%m-%Y')
    # import datetime
    # dt = datetime.date.strftime(made_date,"%m/%d/%y")

    image.save(staticpath + "store\\" + dt + ".jpg")
    path = "/static/store/"+ dt + ".jpg"
    db = Db()
    storeid = session["lid"]
    qry = "insert into product(name,price,stock,made_date,image,store_id,adddate)values('" + name + "','" + price + "','" + stock + "','" + made_date + "','" + path + "','" + str(storeid) + "','"+str(dte)+"')"
    res = db.insert(qry)
    return '''<script> alert('Added Succusfully '); window.location='/AddProduct'</script>'''



@app.route('/SearchProduct',methods=['post'])
def SearchProduct():
    n=request.form['textfield']
    db = Db()
    qry = "select * from product where name like '%"+n+"%' and store_id='"+str(session["lid"])+"'"
    res = db.select(qry)

    return render_template('store/ViewProduct.html', data=res)

@app.route('/ViewProduct')
def ViewProduct():
    db=Db()
    qry="select * from product where store_id='"+str(session["lid"])+"'"
    res=db.select(qry)
    ls=[]
    for i in res:
        ss=i['made_date']
        yy=str(ss)
        cc=yy.split("-")
        print(cc)
        so_date=cc[2]+"-"+cc[1]+"-"+cc[0]
        print(so_date)
        ls.append({"name":i['name'],"price":i['price'],"stock":i['stock'],"made_date":so_date,"image":i['image'],"product_id":str(i['product_id']),"adddate":i['adddate']})
    return render_template('store/ViewProduct.html',data=ls)





@app.route('/ViewProduct_post',methods=['post'])
def ViewProduct_post():
    name = request.form['textfield']
    return 'ok'
@app.route('/review',methods=['post'])
def revirew():
    con = request.form['content']
    llid=request.form['lid']
    q = "insert into review(content,date,user_id)values('" + con + "',curdate(),'"+llid+"')"

    db = Db()
    lid = db.insert(q)

    return jsonify(status="ok")












if __name__=='__main__':
   app.run(debug=True, host="0.0.0.0", port=1234)