import numpy as np 
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import adjusted_rand_score
from sklearn import preprocessing
import json




def ia_funcional(dataset,tipo):
    if(tipo=="ninos"):
      data=pd.read_csv("peso_talla.csv")
      x=data.drop(["valoracion"],axis=1)
      y=data.valoracion
      x.head()
      prueba=dataset
      muestreo=prueba[prueba["sexo"]=="M"]
      prueba1=muestreo.drop(["nombre","id","sexo"],axis=1)
    else:
      data=pd.read_csv("peso_talla_ninas.csv")
      x=data.drop(["valoracion"],axis=1)
      y=data.valoracion
      x.head()
      prueba=dataset
      muestreo=prueba[prueba["sexo"]=="F"]
      prueba1=muestreo.drop(["nombre","id","sexo"],axis=1)


    

    prueba1.head()

    X_train,X_test,y_train,y_test=train_test_split(x,y, test_size=0.05, random_state=2 )
    tree=DecisionTreeClassifier()
    tree.fit(X_train,y_train)
    tree_pred=tree.predict(X_test)
    tree_score=adjusted_rand_score(y_test,tree_pred)
    print(f"el modelo tree tiene un score de {tree_score}")
    print("*"*60)
    tree_pred=tree.predict(prueba1)
    print(tree_pred)

    encoder=preprocessing.LabelEncoder()
    encoder.fit(["0:Peso adecuado para la talla","1:Riesgo de desnutrición","2:Desnutricion Aguda Moderada",
                "3:Desnutricion aguda severa","4:Obesidad","5:Riesgo de Sobrepeso","6:Sobrepeso"
                ])
    print(list(encoder.inverse_transform(tree_pred)))
    valoraciones=list(encoder.inverse_transform(tree_pred))
    df=pd.DataFrame(muestreo)
    df["valoracion"]=valoraciones
    df.head()
    return(df)


def llamar(url):
    dataset=pd.read_excel(f"{url}")
    valoracion_ninas=ia_funcional(dataset,"ninas")
    valoracion_ninos=ia_funcional(dataset,"ninos")

    resultado_total=pd.concat([valoracion_ninas,valoracion_ninos])
    resultado_total.valoracion=resultado_total.valoracion.replace(["0:Peso adecuado para la talla"],["Peso adecuado para la talla"])
    resultado_total.valoracion=resultado_total.valoracion.replace(["1:Riesgo de desnutrición"],["Riesgo de desnutrición"])
    resultado_total.valoracion=resultado_total.valoracion.replace(["2:Desnutricion Aguda Moderada"],["Desnutricion Aguda Moderada"])
    resultado_total.valoracion=resultado_total.valoracion.replace(["3:Desnutricion aguda severa"],["Desnutricion aguda severa"])
    resultado_total.valoracion=resultado_total.valoracion.replace(["4:Obesidad"],["Obesidad"])
    resultado_total.valoracion=resultado_total.valoracion.replace(["5:Riesgo de Sobrepeso"],["Riesgo de Sobrepeso"])
    resultado_total.valoracion=resultado_total.valoracion.replace(["6:Sobrepeso"],["Sobrepeso"])
    
    resultado_total=resultado_total.sort_values(by=["id"],ascending=[True])
    resultado_total=resultado_total.drop(["id"],axis=1)
    resultado_total.head()

    resultado_total.to_json("peso_talla_completo.json",orient = "records", date_format = "epoch", double_precision = 10, force_ascii = True, date_unit = "ms", default_handler = None)