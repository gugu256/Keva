from flask import Flask, render_template, request
import json
import hashlib
import os 
import random

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route('/')
def index():
    return render_template("index.html")
    
@app.route('/gen')
def gen():
    chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    dbkey = ""
    for i in range(0, 16):
        dbkey += random.choice(chars)
    if dbkey + ".json" in os.listdir("databases"):
        return gen()
    else:
        json.dump({}, open("databases/" + dbkey + ".json", "w"))
        return render_template("newdb.html", dbkey=dbkey)

@app.route('/docs')
def documentation():
    return render_template("documentation.html")

# ERRORS


# ACTUAL DATABASE

@app.route('/get/<db_key>/<key>')
def get(db_key, key):
    try:
        db = json.loads(open("databases/" + db_key + ".json", "r").read())
        return {key:db[key]}
    except KeyError:
        return {"erorr":"key does not exist"}
    except FileNotFoundError:
        return {"error":"database does not exist"}
    except:
        return {"error":"unknown"}

@app.route('/get_entire/<db_key>')
def get_entire(db_key):
    try:
        db = json.loads(open("databases/" + db_key + ".json", "r").read())
        return db
    except FileNotFoundError:
        return {"error":"database does not exist"}
    except:
        return {"error":"unknown"}

@app.route('/get_keys/<db_key>')
def get_keys(db_key):
    try:
        db = json.loads(open("databases/" + db_key + ".json", "r").read())
        return list(db.keys())
    except FileNotFoundError:
        return {"error":"database does not exist"}
    except:
        return {"error":"unknown"}

@app.route('/set/<db_key>/<key>/<value>/<type>')
def set(db_key, key, value, type):
    try:
        db = json.loads(open("databases/" + db_key + ".json", "r").read())
        if type == "int":
            value = int(value)
        elif type == "float":
            value = float(value)
        elif type == "str":
            value = str(value)
        elif type == "dict" or type == "list" or type == "json" or type == "bool":
            value = json.loads(value)
        db[key] = value
        json.dump(db, open("databases/" + db_key + ".json", "w"))
        return {"status":"success"}
    except FileNotFoundError:
        return {"error":"database does not exist"}
    except:
        return {"error":"unknown"}

@app.route('/del/<db_key>/<key>')
def delete(db_key, key):
    try:
        db = json.loads(open("databases/" + db_key + ".json", "r").read())
        del db[key]
        json.dump(db, open("databases/" + db_key + ".json", "w"))
        return {"status":"success"}
    except KeyError:
        return {"error":"key does not exist"}
    except FileNotFoundError:
        return {"error":"database does not exist"}
    except:
        return {"error":"unknown"}

@app.route('/reset/<db_key>')
def reset(db_key):
    try:
        db = json.loads(open("databases/" + db_key + ".json", "r").read())
        db = {}
        json.dump(db, open("databases/" + db_key + ".json", "w"))
        return {"status":"success"}
    except KeyError:
        return {"error":"key does not exist"}
    except FileNotFoundError:
        return {"error":"database does not exist"}
    except:
        return {"error":"unknown"}

# END OF ACTUAL DATABASE

@app.route('/drop/<db_key>/')
def drop(db_key):
    try:
        os.remove("databases/" + db_key + ".json")
        return {"status":"database deleted successfully"}
    except FileNotFoundError:
        return {"error":f"database {db_key} does not exist"}
    except:
        return {"error":"unknown"}

app.run(host='0.0.0.0')