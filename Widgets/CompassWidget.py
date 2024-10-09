from Widgets.Widget import Widget
from PySide6 import QtGui
from PySide6.QtGui import QPen, QBrush, QPixmap
from PySide6.QtWidgets import  QGraphicsScene, QGraphicsEllipseItem, QGraphicsView, QGraphicsPixmapItem
from PySide6.QtCore import QPointF, QRectF, Qt
from PySide6.QtCore import Signal
import math


from PIL import Image
from Modules.Tools.mask import compass_mask
from Modules.Tools.mapAPI import mapApi, check_internet

from Modules.Tools.geo import bearing, distance

class CompassWidget(Widget):
    updateCompass = Signal()

    def __init__(self,parent):
        super().__init__(parent)

        self.setWindowTitle("Compass Widget")

        #Création de la scene
        self.compass = QGraphicsScene(self)     

        #Couleur de fond
        self.compass.setBackgroundBrush(QBrush(QtGui.QColor(229, 229, 229)))

        #Initialisation des constantes
        self.center = QPointF(0,0)
        self.radius = 58
        self.radiusBille = 3
        self.range = 2000
        
        #Initialisation des variables
        self.angle = 0
        self.distance = 0
        self.verif = 0

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

        #Création du compas
        self.drawBackground()
        self.drawCompass()
        

        #Création de la vue
        self.view = QGraphicsView(self.compass)
        self.view.setStyleSheet("border: none;")

        #Ajout du compas au layout 
        self.layout.addWidget(self.view)
        
        self.requiredData = ["rockets.anirniq.communication.gnss.lat", "rockets.anirniq.communication.gnss.lon"]

        # Connecter le signal au slot 
        self.updateCompass.connect(self.updateCompassSlot)
        self.updateCompass.emit() 

    
    def drawBackground(self):
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
                self.background_image = Image.open('Resources/map.png')   
            else:
                self.background_image = Image.open('Resources/V1.png')
            #Ajoute un masque à la map pour fitter la forme du compas 
            compass_mask(self.background_image)
            #Convertion dans le bon format
            self.background_image = QPixmap("Resources/image_compass_mask.png")
            self.background_item = QGraphicsPixmapItem(self.background_image)
            #Positionnement de la map
            self.background_item.setPos(self.center.x() - self.radius, self.center.y() - self.radius)
            self.background_item.setScale(2 * self.radius / self.background_image.width())
            # Ajout de l'élément pour l'image de fond à la scène
            self.compass.addItem(self.background_item)
        else:
            pass
    
    def drawCompass(self):
        #Ajout du cercle
        self.circle = QGraphicsEllipseItem(
            QRectF(self.center.x()-self.radius, self.center.y()-self.radius, 2*self.radius, 2*self.radius) 
        )
        self.circle.setPen(QPen(Qt.black))
        self.compass.addItem(self.circle)

        #Ajout de la target
        self.compass.addLine(self.center.x(),self.radius,self.center.x(),-self.radius)
        self.compass.addLine(-self.radius,self.center.y(),self.radius,self.center.y())

        #Ajout de la bille
        self.bille = QGraphicsEllipseItem(
            QRectF(-self.radiusBille,-self.radiusBille, 2*self.radiusBille, 2*self.radiusBille)
        )
        self.bille.setBrush(QBrush(Qt.red))
        self.compass.addItem(self.bille)
    
    def setData(self, data):
        if data.source == self.requiredData[0]:
            self.latRocket = data.value
            self.verif = self.verif + 1
        if data.source == self.requiredData[1]:
            self.lonRocket = data.value
            self.verif = self.verif + 1
        if self.verif == 2:
                self.verif = 0
                self.updateCompass.emit()   #On émet le signal
   
   #Méthode d'uptade du compas
    def updateCompassSlot(self):            #Si un signal est émit
        self.angle = bearing(self.latGS,self.lonGS,self.latRocket,self.lonRocket)       #Calcul du bearing
        self.distance = distance(self.latGS,self.lonGS,self.latRocket,self.lonRocket)   #Calcul de la distance horizontale à la GS
        if self.distance <= self.range:
            x = self.center.x() + self.distance/self.range * self.radius * math.cos(math.radians(self.angle-90))
            y = self.center.y() + self.distance/self.range * self.radius * math.sin(math.radians(self.angle-90))
        else: 
            x = self.center.x() + self.radius * math.cos(math.radians(self.angle-90))
            y = self.center.y() + self.radius * math.sin(math.radians(self.angle-90))
        
        self.bille.setRect(x-self.radiusBille, y-self.radiusBille, 2*self.radiusBille, 2*self.radiusBille)

