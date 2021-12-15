
import random
import pandas as pd
import numpy as np
from flask import Blueprint
from flask import render_template,request
import time
import os
from flask import current_app as app

def addapt(rem:pd.core.series.Series, t:pd.core.series.Series):
    arr_cls = [69006,69002,69004,69001,69003,69007,69008,69009,69005]
    delta_standing = (rem.standing - t.standing) * 50000
    delta_arr = (arr_cls.index(rem.arrondissment) - arr_cls.index(t.arrondissment)) * -10000
    delta_sup = (rem.superficie - t.superficie) * -3000
    
    delta_prix = delta_standing + delta_arr +delta_sup

        
    return (rem.prix + delta_prix, t.prix - (rem.prix + delta_prix))

def algo_2(row: pd.core.series.Series, cas_c:pd.core.series.Series):
    weights ={
        "arrondissment" : 14,
        "standing": 15,
        "superficie":7,
        "nbr_chambre":6,
        "nbr_p":6,
        "etage":3
    }
    wted_avg = 0
    if row.arrondissment == cas_c.arrondissment:
        wted_avg += (weights["arrondissment"] * 1)
        if row.standing == cas_c.standing:
            wted_avg += (weights["standing"] * 1)
            if abs(row.superficie - cas_c.superficie) <=15:
                wted_avg += (weights["superficie"] * 1)
            else:
                wted_avg += (weights["superficie"] * (abs(1-(abs(row.superficie - cas_c.superficie))/max(row.superficie,cas_c.superficie))))
        else:
            wted_avg += (weights["standing"] * 0.2)
            if abs(row.superficie - cas_c.superficie) <=15:
                wted_avg += (weights["superficie"] * 1)
            else:
                wted_avg += (weights["superficie"] * (abs(1-(abs(row.superficie - cas_c.superficie))/max(row.superficie,cas_c.superficie))))
    else:
        wted_avg += (weights["arrondissment"] * 0.3)
        if row.standing == cas_c.standing:
            wted_avg += (weights["standing"] * 1)
            if abs(row.superficie - cas_c.superficie) <=15:
                wted_avg += (weights["superficie"] * 1)
            else:
                wted_avg += (weights["superficie"] * (abs(1-(abs(row.superficie - cas_c.superficie))/max(row.superficie,cas_c.superficie))))
        else:
            wted_avg += (weights["standing"] * 0.2)
            if abs(row.superficie - cas_c.superficie) <=15:
                wted_avg += (weights["superficie"] * 1)
            else:
                wted_avg += (weights["superficie"] * (abs(1-(abs(row.superficie - cas_c.superficie))/max(row.superficie,cas_c.superficie))))
    
    wted_avg += (weights["nbr_chambre"] * (1-abs(row.nbr_chambre - cas_c.nbr_chambre)/max(row.nbr_chambre,cas_c.nbr_chambre)))
    wted_avg += (weights["etage"] * (1-abs(row.etage - cas_c.etage)/max(row.etage,cas_c.etage)))
    wted_avg += (weights["nbr_p"] * (1-abs(row.nbr_p - cas_c.nbr_p)/max(row.nbr_p,cas_c.nbr_p)))
    return wted_avg/sum(list(weights.values()))
    

main= Blueprint('main',__name__)
@main.route('/')
def index():
    return render_template("index.html")



estimate= Blueprint('estimate',__name__)
@estimate.route('/estimate', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        data_appartement = os.path.join(app.static_folder, 'data_appartement.csv')
        form_data = request.form
        array_np=np.array([float(form_data["Arrondissment"]),float(form_data["Superficie"]),int(form_data["Chambres"]),int(form_data["Piece"]),int(form_data["Etage"]),int(form_data["Standing"]),0])
        df = pd.read_csv(data_appartement, index_col="ID")
        print(df.columns)
        names =['arrondissment', 'superficie', 'nbr_chambre', 'nbr_p','etage','standing', 'prix']
        test = pd.DataFrame([array_np],columns=names).iloc[0]   
        df["sim"] = df.apply(lambda row: algo_2(row,test),axis=1)
        df = df.sort_values(by=['sim'])
        most_similar = df.iloc[-1]
        suggested_price, difference_between = addapt(most_similar,test)
        print(suggested_price)

    return render_template("estimate.html",price=suggested_price, test=test, similar = most_similar)

