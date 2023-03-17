from flask import Flask,jsonify,request
from ia_unica import ia_funcional
from ia_multi import llamar
import json
from os import getcwd


PATH_FILE=getcwd()+"/files/"

app= Flask(__name__)

@app.route('/unico',methods=["POST"])
def hello():
    peso=request.json['peso']
    talla=request.json['talla']
    genero=request.json['genero']
    resultado=int(ia_funcional(peso,talla,genero))
    return jsonify({"resultado":resultado})
    



@app.route('/multi', methods=["POST"])
def hacer_multi():
    archivo=request.files["file"]
    url=PATH_FILE + archivo.filename
    archivo.save(url)

    llamar(url)
    return "se ejecuto"



if __name__=='__main__':
    app.run(debug=True, port=4000)











