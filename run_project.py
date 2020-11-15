"""
    PROIECT MOZAIC
"""

# Parametrii algoritmului sunt definiti in clasa Parameters.
from parameters import *
from build_mosaic import *

# numele imaginii care va fi transformata in mozaic
image_path = "C:\\Users\\antoa\\Desktop\\lab1\\Tema1\\tema1\\data\\imaginiTest\\liberty.jpg"

params = Parameters(image_path)

# directorul cu imagini folosite pentru realizarea mozaicului
params.small_images_dir = "C:\\Users\\antoa\\Desktop\\lab1\\Tema1\\tema1\\data\\colectie"
# tipul imaginilor din director
params.image_type = 'png'
# numarul de piese ale mozaicului pe orizontala
# pe verticala vor fi calcultate dinamic a.i. sa se pastreze raportul
params.num_pieces_horizontal = 25
# afiseaza piesele de mozaic dupa citirea lor
params.show_small_images = False
# modul de aranjarea a pieselor mozaicului
# optiuni: 'aleator', 'caroiaj'
params.layout = 'caroiaj'
# criteriul dupa care se realizeaza mozaicul
# optiuni: 'aleator', 'distantaCuloareMedie'
params.criterion = 'distantaCuloareMedie'
# daca params.layout == 'caroiaj', sa se foloseasca piese hexagonale
params.hexagon = False
#pentru subpunctul c)-vecini diferiti
params.different_neigh=False

img_mosaic = build_mosaic(params)
cv.imwrite("C:\\Users\\antoa\\Desktop\\lab1\\Tema1\\tema1\\output\\liberty.png", img_mosaic)

