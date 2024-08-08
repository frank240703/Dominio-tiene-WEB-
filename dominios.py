import requests
from bs4 import BeautifulSoup

def verificar_dominios(lista_dominios):
    dominios_activos = []
    dominios_inactivos = []
    headers = {'User-Agent': 'Mozilla/5.0'}

    for entrada in lista_dominios:
        # Extraer el dominio del correo electrónico si existe
        if '@' in entrada:
            dominio = entrada.split('@')[1]
            correo = entrada
        else:
            dominio = entrada
            correo = None

        url = f"http://{dominio}"
        try:
            respuesta = requests.get(url, allow_redirects=True, timeout=10, headers=headers)
            if respuesta.status_code == 200:
                soup = BeautifulSoup(respuesta.content, 'html.parser')
                title = soup.find('title')
                links = soup.find_all('a', href=True)
                internal_links = [link for link in links if dominio in link['href']]
                
                if (title and not any(x in title.text.lower() for x in ['cpanel', 'parked', 'under construction', 'default'])) or len(internal_links) > 5:
                    print(f"El dominio {dominio} tiene una página web activa.")
                    dominios_activos.append(dominio)
                else:
                    print(f"El dominio {dominio} parece no tener una página web activa.")
                    if correo:
                        dominios_inactivos.append(correo)
                    else:
                        dominios_inactivos.append(dominio)
            else:
                print(f"El dominio {dominio} no tiene una página web activa, código de estado: {respuesta.status_code}.")
                if correo:
                    dominios_inactivos.append(correo)
                else:
                    dominios_inactivos.append(dominio)
        except requests.exceptions.RequestException as e:
            print(f"No se pudo conectar con el dominio {dominio}: {e}")
            if correo:
                dominios_inactivos.append(correo)
            else:
                dominios_inactivos.append(dominio)

    return dominios_activos, dominios_inactivos

# Rutas de archivos
ruta_archivo = r'C:\Users\Frankshesco\Desktop\script-vereficar paginas web\dominios.txt'
ruta_archivo_activos = r'C:\Users\Frankshesco\Desktop\script-vereficar paginas web\dominios_paginaweb.txt'
ruta_archivo_inactivos = r'C:\Users\Frankshesco\Desktop\script-vereficar paginas web\dominios_sinWeb.txt'

# Lectura de la lista de dominios del archivo
with open(ruta_archivo, 'r') as archivo:
    lista_dominios = [linea.strip() for linea in archivo]

# Verificación de los dominios
dominios_activos, dominios_inactivos = verificar_dominios(lista_dominios)

# Guardar los dominios activos en un archivo
with open(ruta_archivo_activos, 'w') as archivo_activos:
    for dominio in dominios_activos:
        archivo_activos.write(f"{dominio}\n")

# Guardar los dominios inactivos en un archivo
with open(ruta_archivo_inactivos, 'w') as archivo_inactivos:
    for dominio in dominios_inactivos:
        archivo_inactivos.write(f"{dominio}\n")
