import math
class Constantes:
    G = 9.81
class Tuberia:
    def __init__(self, coeficiente_friccion, longitud, diametro, *args, caudal = 0, z1 = 0, z2 = 0, material = "N/D"):
        self.diametro = diametro
        self.longitud = longitud
        self.coeficiente_friccion = coeficiente_friccion
        self.caudal = caudal
        self.material = material
        self.area = math.pi*(diametro**2)/4
        self.velocidad = 0
        self.z2 = z2
        self.z1 = z1
        self.pendiente = (self.z2 - self.z1)/longitud
        self.energia_entrada = 0
        self.args = args

    def set_caudal(self, caudal_nuevo):
        self.caudal = caudal_nuevo
        self.velocidad = self.caudal/self.area

    def e_cinetica(self):
        return (self.velocidad**2)/2*Constantes.G

    def perdida(self, x):
        return (self.coeficiente_friccion*x/self.diametro)*self.e_cinetica()

    def presion(self, x):
        z = self.z1+(self.pendiente*x)
        perdida_objetos = 0
        for elemento in self.args:

            if elemento.posicion < x:
                perdida_objetos += elemento.perdida(self.e_cinetica())
            
        return self.energia_entrada - z - self.e_cinetica() - self.perdida(x) - perdida_objetos

    def set_energia_entrada(self, setear):
        self.energia_entrada = setear

    def __str__(self):
        return f"Diámetro: {self.diametro}\nLongitud: {self.longitud}\nCoeficiente de fricción: {self.coeficiente_friccion}\nMaterial: {self.material}\nCaudal: {self.caudal}\n"
    

class Reservorio: 
    def __init__(self,posicion, nivel, k_embocadura = 0, k_desembocadura = 0):
        self.posicion = posicion
        self.nivel = nivel
        self.k_embocadura = k_embocadura
        self.k_desembocadura = k_desembocadura
        self.perdida_embocadura = 0
        self.perdida_desembocadura = 0

    def set_perdida_embocadura(self, e_cinetica):
        self.perdida_embocadura = self.k_embocadura*e_cinetica

class Valvula:
    def __init__(self, posicion, k_valvula = 0):
        self.k_valvula = k_valvula
        self.posicion = posicion
        self.energia_entrada = 0
        self.energia_salida = 0

    def perdida(self, e_cinetica):
        return self.k_valvula*e_cinetica

class Nodo:
    def __init__(self, i):
        self.i = i
        self.presion_aguas_arriba = 0
        self.presion_aguas_abajo = 0


    

valvula1 = Valvula(150, 0.5)
valvula2 = Valvula(200, 0.8)
reservorio1 = Reservorio(0, 100, .05)
tuberia1 = Tuberia(0.018, 300, 1, valvula1,valvula2, material= "Acero")
tuberia1.set_caudal(1)
reservorio1.set_perdida_embocadura(tuberia1.e_cinetica())
tuberia1.set_energia_entrada(reservorio1.nivel-reservorio1.perdida_embocadura)

for i in range (11):
    print(f"La presion en la progresiva {i*30} es {tuberia1.presion(i*30)} m")



