from Solenoid import Spire, SystemeSpires
import numpy
from matplotlib.pyplot import *
import json

max = 10.0
I = 0.5
solenoide = SystemeSpires(-max,max,-max,max)
solenoide.ajouter(Spire(1.0,0.0, I))
for k in range(1,5):
    zs = k*0.25
    solenoide.ajouter(Spire(1.0,zs, I))
    solenoide.ajouter(Spire(1.0,-zs, I))
            

figure(figsize=(7,7))
solenoide.plot_lignesB([[0.0,0.0], [0.15,0.0], [0.3,0.0], [0.45,0.0], [0.6,0.0],[0.75,0.0],[0.9,0.0]],'b')
iso = solenoide.lignesE([[0., 1.2], [0., 1.3], [0., 1.4], [0., 1.5], [0., 1.6], [0., 1.7], [0., 1.8], [0., 1.9], [0., 2],])
# iso = solenoide.lignesE([[0., 2]])
for curve in iso:
	plot(curve[0], curve[1], "g")
axis([-max,max,-max,max])
show()

# export 
with open("field.json", "w") as outfile:
	outfile.write(json.dumps(iso))