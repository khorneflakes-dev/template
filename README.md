# Instalacion del Template

- paso 1: crear un entorno virtual, flask emula un servidor en su entorno local asi que este paso es obligatorio

```
py -m venv template
```

- paso 2: clonar la repo o descargarla y descomprimirla dentro del entorno virtual

```
git clone https://github.com/khorneflakes-dev/template
```

- paso 3: abrir cmd, terminal o shell desde la carpeta, o dirigirse a la carpeta donde crearon el entorno virtual e iniciarlo

- paso 4: dirigirse a la carpeta que clonaron e instalar todas las dependencias necesarias
```
pip install -r .\requirements.txt
```
- paso 5: iniciar la aplicacion corriendo el script
```
py .\app.py
```
- paso 6: si hicieron todo bien hasta este punto, deberian ver esto en su terminal
![image](./eg%20server.png)

- ultimo paso: para poder ver el resultado en su navegador solo se dirigen a la direccion que les indica la terminal

```
http://127.0.0.1:8050
```
tambien sirve localhost
```
localhost:8050
```
y entrando a cualquiera de esas direcciones deberian poder ver esto
![image](./eg%20deploy.png)