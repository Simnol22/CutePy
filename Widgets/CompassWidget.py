from Widgets.Widget import Widget
from PySide6 import QtGui
from PySide6.QtGui import QPen, QBrush, QPixmap, QPainter
from PySide6.QtWidgets import  QGraphicsScene, QGraphicsEllipseItem, QGraphicsView, QGraphicsPixmapItem, QWidget, QVBoxLayout
from PySide6.QtCore import QPointF, QRect, Qt
import math


from PIL import Image
from Modules.Tools.mask import compass_mask
from Modules.Tools.mapAPI import mapApi, check_internet

from Modules.Tools.geo import bearing, distance

class CompassWidget(Widget):

    def __init__(self,parent):
        super(CompassWidget, self).__init__(parent)

        self.verif = 0
        # Initialize the layout
        self.vlayout = QVBoxLayout()
        self.drawCompassWidget =  DrawCompassWidget(self)
        self.vlayout.addWidget(self.drawCompassWidget)
        self.layout.addLayout(self.vlayout)
        
        

        self.requiredData = ["rockets.anirniq.communication.gnss.lat", "rockets.anirniq.communication.gnss.lon"]


    def setData(self, data):
        if data.source == self.requiredData[0]:
            self.drawCompassWidget.setLatRocket(data.value)
            self.verif = self.verif + 1
        if data.source == self.requiredData[1]:
            self.drawCompassWidget.setLonRocket(data.value)
            self.verif = self.verif + 1
        if self.verif == 2:
                self.verif = 0
                self.update()
        

class DrawCompassWidget(QWidget):
    def __init__(self, parent=None):
        super(DrawCompassWidget, self).__init__(parent)
        #Initialisation des constantes
        self.center = QPointF(0,0)
        self.radius = 58
        self.radiusBille = 3
        self.range = 2000
        
        #Initialisation des variables
        self.angle = 0
        self.distance = 0
        

        #Latitude et longitude de la ground station en degré
        self.latGS = 45.539653
        self.lonGS = -73.548456

        #Second jeux de coordonnées de la GS (voir background)
        self.latGS2 = 0   
        self.lonGS2 = 0

        #Latitude et longitude de la rocket    
        self.latRocket = 45.539653
        self.lonRocket = -73.548456

        # Chargement de l'image de fond
        self.background_image = 0 #Image.open('Resources/map.png')
    
    def setLatRocket(self,latRocket_):
        self.latRocket = latRocket_
    
    def setLonRocket(self,lonRocket_):
        self.lonRocket = lonRocket_

        
    def paintEvent(self, event=None):
        width = self.width()
        height = self.height()

        # Dessiner la jauge
        painter = QPainter(self)
        # Dessiner le fond de la jauge
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.black, 1))
        painter.drawEllipse(1, 1, height-2, width-2)

        self.distance = distance(self.latGS,self.lonGS,self.latRocket,self.lonRocket)   #Calcul de la distance horizontale à la GS



        #On test si les coordoonées de la ground sation ont changé. 
        #Si oui on met à jour la carte en fond, sinon on ne fait rien
        #Cela permet de réduire le nombre de demande à l'API
        if self.latGS != self.latGS2 or self.lonGS != self.lonGS2:
            #Mise à jour des coordonnées de vérification
            self.latGS2 = self.latGS
            self.lonGS2 = self.lonGS

            if check_internet() == 1:
                #Mise à jour de la position de groud station
                mapApi(self.latGS,self.lonGS)
            else:
                self.background_image = Image.open('Resources/V1.png')

        else:
            pass

        if self.distance <= 1000:
            self.background_image = QPixmap('Resources/map1000.png')
            self.range = 1000
        elif 1000 < self.distance <= 2000:
            self.background_image = QPixmap('Resources/map2000.png')
            self.range = 2000
        elif 2000 < self.distance <= 3000:
            self.background_image = QPixmap('Resources/map3000.png')
            self.range = 3000
        elif 3000 < self.distance <= 4000:
            self.background_image = QPixmap('Resources/map4000.png')
            self.range = 4000
        elif self.distance > 4000:
            self.background_image = QPixmap('Resources/map5000.png')
            self.range = 5000
        else:
            print('Probleme choix photo')

        
        # #Ajoute un masque à la map pour fitter la forme du compas 
        # compass_mask(self.background_image)
        # #Convertion dans le bon format
        # self.background_image = QPixmap("Resources/image_compass_mask.png")

        # self.background_image = QPixmap("Resources/image_compass_mask.png")
        
        resized_image = self.background_image.scaled(width - 2, height - 2, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        target_rect = QRect(1, 1, width - 2, height - 2)  # Utiliser QRect pour spécifier la zone
        painter.drawPixmap(target_rect, resized_image)  # Correctement appelé avec QRect et QPixmap

        painter.drawLine(1, (height-2)/2 + 1, width - 1,(height-2)/2 + 1)
        painter.drawLine((width-2)/2 + 1, 1, (width-2)/2 + 1, height - 1)

        

        self.angle = bearing(self.latGS,self.lonGS,self.latRocket,self.lonRocket)       #Calcul du bearing
        if self.distance <= self.range:
            x = ((height-2)/2 +1) + self.distance/self.range * (height-2)/2 * math.cos(math.radians(self.angle-90))
            y = ((height-2)/2 +1) + self.distance/self.range * (height-2)/2 * math.sin(math.radians(self.angle-90))
        else: 
            x = ((height-2)/2 +1) + (height-2)/2 * math.cos(math.radians(self.angle-90))
            y = ((height-2)/2 +1) + (height-2)/2 * math.sin(math.radians(self.angle-90))

        # Dessiner la bille (ellipse) en rouge et remplie
        painter.setBrush(QBrush(Qt.red))  # Remplir avec une couleur rouge
        painter.setPen(QPen(Qt.black, 1))  # Contour noir
        painter.drawEllipse(x -self.radiusBille , y - self.radiusBille, 2*self.radiusBille, 2*self.radiusBille)

        painter.end()

        

