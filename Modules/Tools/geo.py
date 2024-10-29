import math
#Permet de calculer la distance et le bearing de la fusée par rapport à la groundstation

#Calcul du bearing:
def bearing(lat1, lon1, lat2, lon2):
    #Passage en radian
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    lon1 = math.radians(lon1)
    lon2 = math.radians(lon2)
    
    dLon = lon2 - lon1
    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) \
        - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
    return math.degrees(math.atan2(y, x))

def distance(lat1, lon1, lat2, lon2):   #Distance en mètres entre deux points en fonctions de leurs coordonnées géographiques
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)
    lon1 = math.radians(lon1)
    lon2 = math.radians(lon2)

    R = 6371 * 1000 #Rayon de la terre en m

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return(int(R*c))

def new_Latitude(lat,distance): #Calcul la nouvelle latitude d'un point en fonction de la distance par rapport à un autre point
    meridien = 20012000         #Explications:  https://www.youtube.com/watch?v=1FmidzSdZdE
    new_lat = lat - distance * 180/meridien
    return new_lat

     
  