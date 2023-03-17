import numpy as np 
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import adjusted_rand_score
from sklearn import preprocessing
import json

def ia_funcional(peso,talla,tipo):
    if(tipo=="nino"):
      datos=pd.read_csv("peso_talla.csv")
      x=datos.drop(["valoracion"],axis=1)
      y=datos.valoracion
      
    else:
      datos=pd.read_csv("peso_talla_ninas.csv")
      x=datos.drop(["valoracion"],axis=1)
      y=datos.valoracion
      
    X_train,X_test,y_train,y_test=train_test_split(x,y, test_size=0.05, random_state=2 )
    tree=DecisionTreeClassifier()
    tree.fit(X_train,y_train)
    tree_pred=tree.predict(X_test)
    tree_score=adjusted_rand_score(y_test,tree_pred)
    tree_pred=tree.predict([[peso,talla]])
    resultado_final=tree_pred[0]
    return resultado_final