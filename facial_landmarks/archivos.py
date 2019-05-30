import os

directorios = []
for name in os.listdir("."):
    if os.path.isdir(name):
        directorios.append(os.path.abspath(name)+'/0.Hombres')
        directorios.append(os.path.abspath(name)+'/1.Mujeres')
        print (os.path.abspath(name)+"/0.Hombres")
        print (os.path.abspath(name)+"/1.Mujeres")
        print (os.path.dirname(name))
#print [ for name in os.listdir(".") if os.path.isdir(name)]
