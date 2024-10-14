import math
import requests
import os
from Modules.Tools.geo import new_Latitude
from Modules.Tools.mask import compass_mask
from PIL import Image

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

def radiusEarth(B):
    B=math.radians(B) #Conversion en radian
    a = 6378.137  #Rayon au niveau de la mer à l'équateur
    b = 6356.752  #Rayon au pôles
    c = (a**2*math.cos(B))**2
    d = (b**2*math.sin(B))**2
    e = (a*math.cos(B))**2
    f = (b*math.sin(B))**2
    R = math.sqrt((c+d)/(e+f))
    return R

def mapApi(lat,lon):
    print("Requêtes Google API :")
    latlon = [lat, lon]
    earthP = radiusEarth(latlon[0])
    radius = 2
    zoom = math.floor(math.log2(earthP *2 *200 / (256*radius)))+1

    GOOGLE_API_KEY = 'AIzaSyCsStFUVvYqNj2tJoXLGbCt29DCcg1CtAw'

    

    for i in range(5): 
        distance = 1000 + i * 1000
        if distance == 1000:
            size = "148x148"
        elif distance == 2000:
            size = "294x294"
        elif distance == 3000:
            size = "447x447"
        elif distance == 4000:
            size = "597x597"
        elif distance == 5000:
            size = "373x373"
            zoom = 12
        else: 
            print("probleme")

        #Calcul de la latitude à "distance mètres" au dessus et en dessous de centre de la carte
        #afin de calibrer sa taille pour que le point représentant la roquette corresponde à la réalitée.
        #Pour se faire, modifier la size de la carte pour que les deux lignes vertes n'apparraissent plus (garder une carte carrée)
        repere_haut = new_Latitude(lat,-distance)
        repere_bas = new_Latitude(lat,distance)
        api_url = "https://maps.googleapis.com/maps/api/staticmap?"
        #URL de la requête 
        api_url = api_url + ("center=" + str(latlon[0]) + "," + str(latlon[1]) + 
                            "&zoom="+str(zoom) + 
                            "&path=color:0x00ff00ff|weight:1|" + str(repere_haut) + "," + str(latlon[1]-0.1) + "|" + str(repere_haut) + "," + str(latlon[1]+0.1) +
                            "&path=color:0x00ff00ff|weight:1|" + str(repere_bas) + "," + str(latlon[1]-0.1) + "|" + str(repere_bas) + "," + str(latlon[1]+0.1) +  
                            "&size="+ size + "&maptype=satellite&key=" + GOOGLE_API_KEY
                            )
        response = requests.get(api_url)
        
        #Status code = 200 -> out est ok
        if response.status_code != 200:
            print("Error:", response.status_code)
        else:
            print("Cartes reçues: " + str(i+1) +"/5")
            # Sauvegarde de l'image dans le dossier 'Resources'
            file_path = os.path.join("Resources","map" + str(distance) + ".png")
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            # Ouvrir l'image avec PIL
            image = Image.open(file_path)
            # Appliquer un masque
            image = compass_mask(image)
            # Sauvegarder l'image avec masque
            masked_file_path = os.path.join("Resources","map" + str(distance) + ".png")
            image.save(masked_file_path)
    print("Toutes les cartes ont été enregistrées.")

