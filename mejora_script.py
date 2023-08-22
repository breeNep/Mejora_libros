import os
import requests
from bs4 import BeautifulSoup
import shutil

# Crear la carpeta "libros" si no existe
if not os.path.exists("libros"):
    os.makedirs("libros")

# Crear la carpeta "temporal" si no existe
if not os.path.exists("temporal"):
    os.makedirs("temporal")

# Crear subcarpetas con los nombres almacenados
valid_links = []

# URL base
base_url = "https://www.conaliteg.sep.gob.mx/"

# URL de la página principal
main_url = "https://www.conaliteg.sep.gob.mx/primaria.html"

# Realizar solicitud HTTP a la página principal
response = requests.get(main_url)
soup = BeautifulSoup(response.content, "html.parser")

# Encontrar y almacenar enlaces
links = soup.find_all("a", href=True)

for link in links:
    if "2023/" in link["href"] and link["href"].endswith(".htm"):
        file_name = link["href"].split("/")[-1]
        folder_name = file_name.split(".")[0][-5:]
        valid_links.append(folder_name)

# Crear subcarpetas con los nombres almacenados
for folder_name in valid_links:
    subfolder_path = os.path.join("libros", folder_name)
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)

# URL base de las imágenes
image_base_url = "https://www.conaliteg.sep.gob.mx/2023/c/{}/{}.jpg"

# Descargar y guardar las imágenes en la carpeta "temporal"
for folder_name in valid_links:
    subfolder_path = os.path.join("libros", folder_name)
    for image_number in range(401):
        image_download_url = image_base_url.format(folder_name, str(image_number).zfill(3))
        image_response = requests.get(image_download_url)
        if image_response.status_code == 200:
            image_path = os.path.join(subfolder_path, "{}_{:03d}.jpg".format(folder_name, image_number))
            with open(image_path, "wb") as f:
                f.write(image_response.content)

print("Descargas completadas")

# No se requiere cambiar la función move_files_to_folders
