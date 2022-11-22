# Codigo Base https://dojopy.com/blog/python-automatizando-whatsapp-con-selenium
# Importar librerías
from selenium import webdriver
import time
import sys
import pandas as pd
import os

# from readXLSX import readXLS

# Defino path de Chromium luego de instalarlo
chromiumPath = 'C:/Users/MR/Desktop/SC/pythonTest/'
xlsPath = 'C:/Users/MR/PycharmProjects/botWA/src/'

'''
Leo archivo .xlsx desde el mismo directorio donde está el script
Las columnas tienen que ser NOMBRE y TELEFONO
Los teléfonos solo tienen que tener código de área (sin 0) y el número de teléfono (sin 15)
Ver ejemplo adjunto
'''


# Defino función para leer archivo .xlsx
def readXLS():
    # Defino nombre del archivo
    xls = 'contacts.xlsx'

    # Leo archivo
    try:
        data = pd.read_excel(xlsPath + xls, usecols=['NOMBRE', 'TELEFONO'])
    except:
        print("No se pueden cargar los contactos")

    # Convierto los tipos de dato a string
    data['TELEFONO'] = data['TELEFONO'].astype(str)
    data['NOMBRE'] = data['NOMBRE'].astype(str).str.title()

    # Adjunto caracteristica
    data['TELEFONO'] = '549' + data['TELEFONO'].astype(str)

    # Convierto DataFrame a lista (necesario para JSON)
    data = data.values.tolist()

    return data

def send_message_to_contact(self, contact, message):
    print("Buscando contacto")
    user_search = self.search_user_or_group(contact)
    if not (user_search or contact or message):
        return False
    message = message.strip()

    try:
        send_msg = WebDriverWait(self.browser, self.timeout).until(
            EC.presence_of_element_located(
            (By.XPATH, self.base_sent)))
    except Exception as e:
        print(e)
        return
    messages = message.split("\n")
    for msg in messages:
        send_msg.send_keys(msg)
        send_msg.send_keys(Keys.SHIFT + Keys.ENTER)
        sleep(1)
    send_msg.send_keys(Keys.ENTER)
    print('mensaje enviado.')
    return True

# Defino función para armado y envío de mensaje
def sendMessage(driver, target, msg):


    # Pausa obligatoria de ejecución (tiempo que tarde en responder selenium + sistema android)
    pause = 5

    # Reemplazo los espacios por %20 para armar la URL
    msg = msg.replace(' ', '%20')

    # Armado de URL para ejecutar en Chromium
    driver.get("https://web.whatsapp.com/send?phone=" + target + "&text=" + msg)
    time.sleep(pause)

    # Ejecución de boton "Send" en Chromium. El código de la clase HTML al momento es _1U1xa
    send = driver.find_element_by_class_name('_1U1xa')
    send.click()

    print(f'Mensaje enviado al número {target}.')
    time.sleep(pause / 2)


def main():
    # Defino lista vacia para controlar los contactos rechazados
    rechazados = list()

    # Ejecuto código
    try:
        print('Estableciendo conexión con Chrome (abriendo navegador)...')

        # Ejecutar el webdriver y la conexión al sitio
        driver = webdriver.Chrome(chromiumPath + 'chromedriver')
        driver.get("https://web.whatsapp.com/")

        # Lectura del código QR
        input(str('Escanee el código QR y presione enter para continuar.'))

        # Lectura de contactos
        print("Procesando contactos...")
        lista = readXLS()

        # Envío de mensajes
        print('Enviando mensajes...')
        for i in range(len(lista)):
            # Defino nombre del contacto y mensaje a enviar
            name = lista[i][0]
            msg = open("mensaje.txt", "r")
            msg = str(msg.read())
            msg = f'Hola {name}! ' + msg

            try:
                # Envío mensaje
                sendMessage(driver=driver, target=lista[i][1], msg=msg)
            except:
                # Si no se pudo enviar, guarda el log en un txt dentro del mismo directorio.
                print(f"No se pudo enviar mensaje al {lista[i][1]}")
                rechazados.append(lista[i])

        print('Se han enviado todos los mensajes.')

        # Paso rechazados a txt
        dfRechazados = pd.DataFrame(rechazados)
        print("Se generó un TXT con los rechazados")
        dfRechazados.to_csv('rechazados.txt', sep='\t', index=False)

        # Cierro Chromium
        print('La aplicación se cerrará.')
        time.sleep(5)
        driver.quit()
        sys.exit()

    except:
        # Si algo sale mal, cierro Chromium
        print('Error en conexión')
        driver.quit()
        print('La conexión fue cerrada')
        sys.exit()


if __name__ == '__main__':
    main()
