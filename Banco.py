import os
import re
import json
from uuid import uuid4

# Leer Base de Datos
def leer_bd():
    bd = open("./Banco_bd.json", "r") 
    data = json.load(bd) 

    bd.close()
    return data

# Guardar en Base de Datos
def guardar_bd(persona, metodo, cuenta = ""):
    data = leer_bd()
    with open("./Banco_bd.json", "w") as bd:
        match metodo:
            case "guardar":
                data.append(persona)
                json.dump(data, bd)                
                bd.close()
            case "actualizar":
                lista_a_actualizar = list(filter(lambda x: x["cuenta"] != cuenta, data))
                lista_a_actualizar.append(persona)
                json.dump(lista_a_actualizar, bd)                
                bd.close()

# Clase Persona
class Persona():
    is_nombre = False

    def __init__(self, nombre, apellido) -> None:
        self.nombre = nombre
        self.apellido = apellido
        self.nombre_completo = f"{self.nombre} {self.apellido}"
        self.verificar_nombre_de_usuario()
    
    def verificar_nombre_de_usuario(self):
        # Ejemplo de Nombre = Juan Perez
        self.is_nombre = bool( 
            re.fullmatch( 
                "[A-Za-z]{2,25}( [A-Za-z]{2,25})?", 
                self.nombre_completo  
            ) 
        )

# Clase Cliente
class Cliente():
    cuenta = None
    balance_de_cuenta = 0

    def __init__(self, persona) -> None:
        self.persona = persona
    
    def crear_cuenta(self):
        if self.persona.is_nombre:
            data = leer_bd()

            for persona in data:
                if self.persona.nombre == persona["nombre"] and self.persona.apellido == persona["apellido"]:
                    print("El usuario ya existe")
                    input("\nEnter para continuar")
                    return False

            nueva_cuenta = str(uuid4()).split("-")
            self.cuenta = nueva_cuenta[-1] + nueva_cuenta[-2]

            nueva_persona = {
                "nombre": self.persona.nombre, 
                "apellido": self.persona.apellido,
                "cuenta": self.cuenta,
                "balance_de_cuenta": self.balance_de_cuenta 
            }

            guardar_bd(nueva_persona, "guardar")
            print(f"Tu numero de cuenta es: {self.cuenta}")

            input("\nEnter para continuar")
            return True 
        else:
            print("Los datos ingresados son incorrectos")
            input("\nEnter para continuar")
            return False

    def detalles_de_cuenta():
        pass

# Clase banco - logica del banco
class Banco():
    usuario = ""

    def __init__(self, cuenta_numero = "") -> None:
        self.cuenta = cuenta_numero


    # Buscar al usaurio
    def buscar_usuario(self, cuenta):
        data = leer_bd()
        res = list(filter(lambda x: x["cuenta"] == cuenta, data))

        if len(res) != 0:
            return res
        
        print("No se ha encontrado al usuario")
        input("\nEnter para continuar")
        return False
    
    # Crear cuenta
    def crear_cuenta(self, nombre, apellido):
        nueva_persona = Persona(nombre, apellido)
        nuevo_cliente = Cliente(nueva_persona)
        nuevo_cliente.crear_cuenta()
        
    # Revisar Balance
    def revisar_balance(self):
        # Busca al Usuario
        self.usuario = self.buscar_usuario(self.cuenta)[0]
        print("Cuenta en pesos:")
        print(f"${self.usuario['balance_de_cuenta']} MXN")
        input("\nEnter para continuar")
        pass

    # Depositar a Cuenta Propia
    def depositar_cuenta_propia(self, cantidad):
        # Busca al usuario
        self.usuario = self.buscar_usuario(self.cuenta)[0]

        if cantidad > 0: 
            self.usuario["balance_de_cuenta"] += cantidad
            # Salvar en la base de datos
            guardar_bd(self.usuario, "actualizar", self.cuenta)
            print(f"Has depositado {cantidad} pesos a tu cuenta")
            input("\nEnter para continuar")
        else:
            print("Cantidad incorrecta o no valida")
            input("\nEnter para continuar")
        
    
    # Deposito a Cuenta de Terceros
    def deposito_terceros(self, cuenta_terceros, cantidad):
        usuario_objetivo = self.buscar_usuario(cuenta_terceros)[0]
        
        if cantidad > 0: 
            usuario_objetivo["balance_de_cuenta"] += cantidad 
            # Actualizar en Base de Datos
            guardar_bd(usuario_objetivo, "actualizar", cuenta_terceros)
            print(f"Has depositado {cantidad} pesos a cuenta de terceros")
            input("\nEnter para continuar")
        else:
            print("Cantidad incorrecta o no valida")
            input("\nEnter para continuar")

    # Retirar
    def withdrawals(self, cantidad):
        self.usuario = self.buscar_usuario(self.cuenta)[0]

        if cantidad > 0 and cantidad < self.usuario["balance_de_cuenta"]:
            self.usuario["balance_de_cuenta"] -= cantidad
            guardar_bd(self.usuario, "actualizar", self.cuenta)
            print(f"Has retirado {cantidad}.")
            print(f"Tu saldo total es de: {self.usuario['balance_de_cuenta']}")
            input("\nEnter para continuar")
        else: 
            print("Cantidad incorrecta o no valida")
            input("\nEnter para continuar")


def app():

    OPCIONES = [
        "[0] - Crea una cuenta",
        "[1] - Ingresar",
        "[q] - Salir"
    ]

    OPCIONES_BANCA = [
        "[0] - Checa tu saldo",
        "[1] - Deposita a tu cuenta",
        "[2] - Deposita a terceros",
        "[3] - Retiro",
        "[q] - Salir",
    ]

    while True:

        os.system("clear" or "cls")
        print("-----------------------------------")
        print("  Bienvenido al Banco del El Neto  ")
        print("-----------------------------------")

        for opcion in OPCIONES:
            print(opcion)
        
        print("\n")
        entrada_usuario = input("Escoge una opción: ")

        match entrada_usuario:
            case "0":
                os.system("clear" or "cls")
                print("--------------")
                print("  Formulario  ")
                print("--------------")
                
                nombre = str(input("Cuál es tu nombre?: "))
                apellido = str(input("Cuál es tu apellido?: "))

                os.system("clear" or "cls")
                Banco().crear_cuenta(nombre, apellido)
            case "1":
                while True:
                    cuenta = str(input("Ingresa el numero de tu cuenta: "))
                    usuario_cuenta = Banco().buscar_usuario(cuenta)
                    
                    if not usuario_cuenta:
                        break 

                    usuario_cuenta = Banco(cuenta)
                
                    while True:
                        os.system("clear" or "cls")
                        print("-------------------------")
                        print("  Bienvenido a tu Banca  ")
                        print("-------------------------")
                        for opcion_banca in OPCIONES_BANCA:
                            print(opcion_banca)
                        print("\n")
                        seleccion_opcion_banca = input("Escoge una opción: ")   

                        match seleccion_opcion_banca:
                            case "0":
                                os.system("clear" or "cls")
                                usuario_cuenta.revisar_balance()
                            case "1":
                                os.system("clear" or "cls")
                                cantidad = float(input("Cuanto dinero quieres ingresar: "))
                                usuario_cuenta.depositar_cuenta_propia(cantidad)
                            case "2":
                                os.system("clear" or "cls")
                                cuenta_terceros = str(input("Numero de cuenta del beneficiario: "))
                                cantidad = float(input("Cuanto dinero quieres depositar: "))
                                usuario_cuenta.deposito_terceros(cuenta_terceros, cantidad)
                            case "3":
                                os.system("clear" or "cls")
                                cantidad = float(input("Cuanto dinero quieres retirar: "))
                                usuario_cuenta.withdrawals(cantidad)
                            case "q":
                                break
                            case otra:
                                print(f"{otra} no es valido")
                                input("\nEnter para continuar")
                    break
            case "q":
                os.system("clear" or "cls")
                print("--------------------------------------------")
                print("  Gracias por preferir el Banco de El Neto  ")
                print("--------------------------------------------")
                break
            case otra:
                print(f"{otra} no es valido")
                input("\nEnter para continuar")
    pass

    
def inicio():
    app()
    

inicio()