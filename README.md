# ReadConnect - Plataforma de Gestión de Libros

## Descripción
Este proyecto consiste en la creación de una plataforma de gestión de libros, que permite a los usuarios llevar un registro de los libros que han leído, los que desean leer, calificarlos y ver las calificaciones de otros usuarios. Además, los usuarios tienen la opción de seguir a otros usuarios para mantenerse al tanto de sus actualizaciones. El proyecto utiliza varias tecnologías, incluyendo Django para el backend y Next.js para el frontend.

![Django Logo](https://portfolio-mparraf.herokuapp.com/static/img/django.png)

## Pasos

### Configuración Inicial
1. Navega al directorio del proyecto.
2. Crea un entorno virtual con Pipenv:
   ```bash
   pipenv shell

3. Instala las bibliotecas de Django y django-dotenv:
   ```bash
   pipenv install django django-dotenv

4. Crea un archivo de requisitos para almacenar los paquetes básicos del proyecto:
   ```bash
   pip freeze > requirements.txt

5. Crea un proyecto Django:
   ```bash
   django-admin startproject project_name

6. Aplica las primeras migraciones para los módulos de administración, autenticación, tipos de contenido y sesiones:
   ```bash
   python manage.py migrate</code>

7. Crea archivos .env y .gitignore en el directorio raíz del proyecto:
   ```bash
   touch .env .gitignore</code>

Configuración de Variables de Entorno
1. Para almacenar variables de entorno, hemos creado los archivos .env y .gitignore. Además, instalamos la biblioteca "python-dotenv" para gestionar la importación de estas variables.

2. En el archivo de configuración (settings.py), cambia la ubicación de la clave SECRET_KEY para almacenarla en el archivo .env:
<pre>
```python
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
SECRET_KEY = os.environ['SECRET_KEY']
```
</pre>

3. Almacena la clave en el archivo .env:
<pre>
```makefile
SECRET_KEY="Inserta aquí la clave de Django para este proyecto"
```
</pre>

4. Agrega el archivo .env al archivo .gitignore para evitar que se incluya en el repositorio de GitHub:
<pre>
```bash
.env
```
</pre>

### Esquema de Directorios y Archivos Estáticos
En este proyecto, hemos definido una estructura de directorios para plantillas y archivos estáticos en el directorio raíz. Para crear estos directorios, ejecuta los siguientes comandos en la línea de comandos:
   
<pre>
```bash
mkdir templates
mkdir static
cd static
mkdir css
mkdir js
```
</pre>

## Instalación
Para comenzar a trabajar en el proyecto, sigue estos pasos:

1. Clona el proyecto en tu directorio local con el siguiente comando:
<pre>
```bash
git clone git@github.com:maaferna/ReadConnect.git
```
</pre>
(Utiliza el protocolo SSH) O
<pre>
```bash
git clone https://github.com/maaferna/project_base_django.git
```
</pre>
(Utiliza el protocolo HTTPS)

2. Crea un entorno virtual con la herramienta pipenv. Pipenv debe estar instalado con Python 3.11 y Django 4.2.3. También puedes utilizar el archivo de requisitos para instalar las bibliotecas necesarias:
<pre>
```bash
pipenv shell
pip install -r requirements.txt
```
</pre>

3. Realiza las migraciones de la base de datos y crea un superusuario:
<pre>
```bash
python manage.py migrate
python manage.py createsuperuser
```
</pre>