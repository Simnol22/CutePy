import math
import requests
import os
from Modules.Tools.geo import new_Latitude

import requests

def check_internet():
    try:
        # Tente d'envoyer une requête HTTP GET à google.com avec un délai de 5 secondes
        response = requests.get("http://www.google.com", timeout=5)
        print("Internet connection available")
        return 1
    except requests.ConnectionError:
        print("No internet connection available")
        return 0

def radiusEarth (B):
    B=math.radians(B) #converting into radians
    a = 6378.137  #Radius at sea level at equator
    b = 6356.752  #Radius at poles
    c = (a**2*math.cos(B))**2
    d = (b**2*math.sin(B))**2
    e = (a*math.cos(B))**2
    f = (b*math.sin(B))**2
    R = math.sqrt((c+d)/(e+f))
    return R

def mapApi(lat,lon):

    GOOGLE_API_KEY = 'AIzaSyCsStFUVvYqNj2tJoXLGbCt29DCcg1CtAw'

    api_url = "https://maps.googleapis.com/maps/api/staticmap?"

    latlon = [lat, lon]
    radius = 2

    earthP = radiusEarth(latlon[0])

    zoom = math.floor(math.log2(earthP *2 *200 / (256*radius)))+1

    #Calcul de la latitude à "distance mètres" au dessus et en dessous de centre de la carte
    #Afin de calibrer sa taille pour que le point représentant la roquette corresponde à la réalitée
    #Pour se faire, modifier la size de la carte pour que les deux lignes vertes n'apparraissent plus (garder une carte carrée)
    distance = 2000
    repere_haut = new_Latitude(lat,-distance)
    repere_bas = new_Latitude(lat,distance)

    #URL de la requête 
    api_url = api_url + ("center=" + str(latlon[0]) + "," + str(latlon[1]) + 
                         "&zoom="+str(zoom) + 
                         "&path=color:0x00ff00ff|weight:1|" + str(repere_haut) + "," + str(latlon[1]-0.1) + "|" + str(repere_haut) + "," + str(latlon[1]+0.1) +
                         "&path=color:0x00ff00ff|weight:1|" + str(repere_bas) + "," + str(latlon[1]-0.1) + "|" + str(repere_bas) + "," + str(latlon[1]+0.1) +  
                         "&size=294x294&maptype=satellite&key=" + GOOGLE_API_KEY
                         )
    response = requests.get(api_url)
    
    #Status code = 200 -> out est ok
    if response.status_code != 200:
        print("Error:", response.status_code)
    else:
        #Sauvegarde de l'image dans le dossier 'Resources'
        file_path = os.path.join("Resources","map.png")
        with open(file_path, 'wb') as f:
            f.write(response.content)
