#!/usr/bin/env python3
""" developer by Dojopy """
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

chromiumPath = 'C:/Users/MR/Desktop/SC/pythonTest/driver2/'
driverPath = chromiumPath+'chromedriver'

def readXLS():
    # Defino nombre del archivo
    xlsPath = 'C:/Users/MR/PycharmProjects/botWAv2/src/'
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


class BotWhatsapp:
    def __init__(self):
        self.path_driver = driverPath
        self.base_url = 'https://web.whatsapp.com/'
        self.timeout = 30
        self.set_paths()

    def set_paths(self):
        self.base_input = '._1awRl'
        #self.first_contact = '//*[@id="pane-side"]/div[1]/div/div/div[1]'
        self.first_contact =  '//*[@id="pane-side"]/div[1]/div/div/div[2]'
        #self.first_contact = 'eJ0yJ' #eJ0yJ' #_2kHpK #_210SC
        self.base_sent = '/html/body/div/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]'

    def start_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--profile-directory=Default')
        options.add_argument("--disable-plugins-discovery")
        options.add_argument('--user-data-dir='+chromiumPath)   # setear ruta local path

        self.browser = webdriver.Chrome(executable_path=self.path_driver,
                                        options=options)
        self.browser.get(self.base_url)
        try:
            WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located(
                (By.CSS_SELECTOR, self.base_input)))
            return True
        except Exception as e:
            print(e)
            return False

    def open_browser(self):
        start = self.start_browser()
        if not start:
            return False

    def send_message_to_contact(self, contact, message):
        print("Comienza funcion de mensaje")
        user_search = self.search_user_or_group(contact)
        print("Se armó user_search")
        print(user_search)
        if not (user_search or contact or message):
            print("No se encontró contacto")
            return False
        print("Se inserta mensaje")
        message = message.strip()
        print("Se insertó mensaje")
        try:
            print("Mando mensaje")
            send_msg = WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, self.base_sent)))
        except Exception as e:
            print("Devuelvo error")
            print(e)
            return
        print("Spliteo mensaje")
        messages = message.split("\n")
        for msg in messages:
            send_msg.send_keys(msg)
            send_msg.send_keys(Keys.SHIFT + Keys.ENTER)
            sleep(1)
        send_msg.send_keys(Keys.ENTER)
        print('Mensaje enviado.')
        return True

    def search_user_or_group(self, contact):
        search = self.browser.find_element_by_css_selector(self.base_input)
        search.clear()
        print("Buscando contacto")
        search.send_keys(contact)
        print("Se insertó numero")
        try:
            vali_ = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, self.first_contact)))
            print("Se selecciono primer contacto")
            print("Se valida")
            if vali_.is_displayed():
                print("Se inserta enter")
                search.send_keys(Keys.ENTER)
                print("Se insertó enter")
                return True

        except Exception as e:
            print(e)
            print('No se encontró contacto.')

        return False


def main():
    # Defino objeto
    obj = BotWhatsapp()

    # Defino lista vacia para controlar los contactos rechazados
    rechazados = list()

    # Proceso contactos
    print("Procesando contactos...")
    lista = readXLS()

    print("Abriendo navegador.")
    # Abro Chromium
    obj.start_browser()

    print('Enviando mensajes...')
    for i in range(len(lista)):
        # Defino nombre del contacto y mensaje a enviar
        name = lista[i][0]
        msg = open("mensaje.txt", "r")
        msg = str(msg.read())
        msg = f'Hola {name}! ' + msg

        try:
            # Envío mensaje
            obj.send_message_to_contact(lista[i][1], msg)
        except:
            # Si no se pudo enviar, guarda el log en un txt dentro del mismo directorio.
            print(f"No se pudo enviar mensaje al {lista[i][1]}")
            rechazados.append(lista[i])

    # Paso rechazados a txt
    dfRechazados = pd.DataFrame(rechazados)
    print("Se generó un TXT con los rechazados")
    dfRechazados.to_csv('rechazados.txt', sep='\t', index=False)

    print('Se han enviado todos los mensajes.')


if __name__ == '__main__':
    main()
