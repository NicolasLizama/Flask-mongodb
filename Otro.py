
#Esta api si me conecto finalmento por el orto 

import hashlib
import datetime
from flask import Flask, request, jsonify, render_template, url_for, redirect
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

app = Flask(__name__)
jwt = JWTManager(app)

app.config['JWT_SECRET_KEY']= "ALSKJDLASKJDLASKJDLKASJDLKASJDL"
app.config['JWT_ACCESS_TOKEN_EXPIRES']=datetime.timedelta(days=1)

uri = "mongodb+srv://NicolasL:OrquTXx3VkV2O6Nu@carloh.m0iuqqj.mongodb.net/?retryWrites=true&w=majority&appName=Carloh"


client = MongoClient(uri, server_api=ServerApi('1'))
db =  client["demoUnab"]
user_collection =db["users"]

@app.route("/api/v1/users", methods=["POST"])
def create_user():
    new_user= request.get_json()
    new_user["password"] =  hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest()
    doc =  user_collection.find_one({"username" : new_user["username"]})
    if not doc:
         user_collection.insert_one(new_user)
         return jsonify({"status" : "Usuario creado con exito"})
    else:
         return jsonify({"status" : "Usuario ya existe"})

@app.route("/api/v1/login", methods=["POST"])
def login():
     login_details = request.get_json()
     user = user_collection.find_one({"username" : login_details["username"]})
     if user:
          enc_pass = hashlib .sha256(login_details['password'].encode("utf-8")).hexdigest()
          if enc_pass ==user["password"]:
               access_token= create_access_token(identity=user["username"])
               return jsonify(access_token= access_token),200

     return jsonify({'msg':'Credenciales incorrectas'}),401


@app.route("/api/v1/usersAll",methods=["GET"])
#@jwt_required()
def get_all_users():
     users = user_collection.find()
     data=[]
     for user in users:
          user["_id"] = str(user["_id"])
          data.append(user) 
     return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)


#Delete Route
#@app.post("/<id>/delete/")
#def delete(id): #delete function by targeting a todo document by its own id
#    todos.delete_one({"_id":ObjectId(id)}) #deleting the selected todo document by its converted id
#    return redirect(url_for('index')) # again, redirecting you to the home page 

@app.route("/login", methods=["POST"])
def crear():
    if request.method == "POST":   # if the request method is post, then insert the todo document in todos collection
        username = request.form['username']
        password = request.form['password']
        doc =  user_collection.find_one({"username" : request.form['username']})
        if not doc:
             user_collection.insert_one({'username': username, 'password': password})
             return render_template('login.html')
        else:
              return jsonify({"status" : "Usuario ya existe"})
        

             
        
        
    #all_todos = user_collection.find()    # display all todo documents
    #return render_template('login.html', todos = all_todos) # render home page template with all todos


#doc =  user_collection.find_one({"username" : new_user["username"]})
    #if not doc:
     #    user_collection.insert_one(new_user)
      #   return jsonify({"status" : "Usuario creado con exito"})
    #else:
     #    return jsonify({"status" : "Usuario ya existe"})


@app.route("/", methods=['GET'])
def index():
    return render_template('index.html')