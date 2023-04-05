<p align="center">
  <a href="https://www.python.org/" target="blank"><img src="https://www.pngmart.com/files/7/Python-PNG-Image.png" width="200" alt="Nest Logo" /></a>
</p>

# Cuenta Bancaria V2

Es un proyecto de consola, el cual te permite realizar operaciones en una o más cuentas bancarias, crear una cuenta, depositar un una cuenta propia, retirar, depositar en una cuenta de terceros, salir del programa. El programa funciona con una base de datos en JSON.

El menú principal del programa es el siguiente:

1.- Crear una cuenta.

2.- Ingresar.

3.- Salir.

Al crear una cuenta el menú será:

1.- Tu nombre.

2.- Tu apellido.

3.- El número de cuenta se creadá automaticamente.


Al ingresar a una cuenta el menú será:

1.- Checa tu saldo.

2.- Deposita a tu cuenta.

3.- Deposita a terceros (te solicitará el número de cuenta al que desear realizar el deposito).

4.- Retiro.

5.- Salir.


El programa muestra mensjaes de bienvenida, formularios, errores y respedidas.

El archivo debe llamarse 'Banco_db.json', estar en el directorio donde se encuentre el archivo 'Banco.py' y su estructura debe ser la siguiente:

### Estructura de datos de 'Banco_bd.json'

```
[
    {
        "nombre": varchar,
        "apellido": varchar,
        "cuenta": varchar,
        "balance_de_cuenta": float
    }
]
```

Nota: la base de datos puede inicializarce simplemente creando el archivo JSON y solo poner los corchetes([]).