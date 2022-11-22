#!/usr/bin/env python3
""" developed by Dojopy """
import time
import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait


# Defino variables
chromiumPath = "C:/Users/MR/Desktop/SC/pythonTest/driver2/"
driverPath = chromiumPath + 'chromedriver'
searchBar = '._1awRl'

# Defino variables para contactos
xlsPath = "C:/Users/MR/PycharmProjects/botWAv2/src/"
xls = "contacts.xlsx"

# Log de envío
dfLog = pd.DataFrame(columns=['Status', 'Name', 'Phone', 'Msg'])


def messageFormatted(name):
    '''
    Función del mensaje
    '''
    msg = open("mensaje.txt", "r")
    msg = str(msg.read())
    msg = f'Hola {name}! ' + msg

    return msg


def readXLSasDF(path, name):
    '''
    Leo archivo de contactos del excel y transformo los campos a Strings para su uso posterior.
    '''

    try:
        data = pd.read_excel(path + name, usecols=['NOMBRE', 'TELEFONO'])
    except:
        print("No se pueden leer el archivo")

    # Convierto los tipos de dato a string
    data['TELEFONO'] = data['TELEFONO'].astype(str)
    data['NOMBRE'] = data['NOMBRE'].astype(str).str.title()

    # Adjunto caracteristica (opcional, deberian venir con)
    # data['TELEFONO'] = '549' + data['TELEFONO'].astype(str)

    return data


def dfToExcel(df, filename):
    '''
    Importo Dataframe a excel en mismo path
    '''
    if os.path.isfile(filename):
        os.remove(filename)
    writer = pd.ExcelWriter(filename)
    df.to_excel(writer, 'Hoja', index=False)
    writer.save()


class BotWhatsapp:
    def __init__(self):
        self.path_driver = driverPath
        self.base_url = 'https://web.whatsapp.com/'
        self.timeout = 300
        self.set_paths()

    def set_paths(self):
        self.base_input = searchBar
        self.first_contact = '//*[@id="pane-side"]/div[1]/div/div/div[2]'
        self.base_sent = '/html/body/div/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]'

    def start_browser(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument('--profile-directory=Default')
        options.add_argument("--disable-plugins-discovery")
        options.add_argument('--user-data-dir=' + chromiumPath)

        self.browser = webdriver.Chrome(executable_path=self.path_driver,
                                        options=options)
        self.browser.get(self.base_url)
        try:
            WebDriverWait(self.browser, self.timeout).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.base_input)))
            return True
        except Exception as e:
            print(e+"No se pudo iniciar Whatsapp Web")
            return False

    def open_browser(self):
        start = self.start_browser()
        if not start:
            print("No pudo iniciarse el navegador")
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
            time.sleep(1)
        send_msg.send_keys(Keys.ENTER)
        print('Mensaje enviado.')

        return True

    def search_user_or_group(self, contact):
        search = self.browser.find_element_by_css_selector(self.base_input)
        search.clear()
        search.send_keys(contact)
        try:
            vali_ = WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.XPATH, self.first_contact)))
            if vali_.is_displayed():
                search.send_keys(Keys.ENTER)
                return True

        except Exception as e:
            print(e)
            print(f'No se pudo encontrar el contacto {contact}')

        return False

    def validate_contacts(self, contacts):
        '''
        Recibo df de contactos, en primer lugar nombre, en segundo apellido y armo listas de existentes e inexistentes
        :param contacts:
        :return:
        '''
        trueContacts = pd.DataFrame(columns=['NOMBRE', 'TELEFONO'])
        falseContacts = pd.DataFrame(columns=['NOMBRE', 'TELEFONO'])

        search = self.browser.find_element_by_css_selector(self.base_input)

        # Recorro la lista de contactos
        for index, row in contacts.iterrows():
            search.clear()
            search.send_keys(row['TELEFONO'])
            time.sleep(1)
            print(f"Validando número de {row['NOMBRE']}.")
            try:
                vali_ = WebDriverWait(self.browser, 5).until(
                    EC.presence_of_element_located((By.XPATH, self.first_contact)))
                if vali_.is_displayed():
                    print("Existe.")
                trueContacts = trueContacts.append({'NOMBRE': row['NOMBRE'],
                                                    'TELEFONO': row['TELEFONO']},
                                                   ignore_index=True)
                dfToExcel(trueContacts, 'ContactosExistentes.xlsx')
            except Exception as e:
                # print(e)
                print('No existe.')
                falseContacts = falseContacts.append({'NOMBRE': row['NOMBRE'],
                                                      'TELEFONO': row['TELEFONO']},
                                                     ignore_index=True)
                dfToExcel(falseContacts, 'ContactosARevisar.xlsx')
        print("Se grabaron los excels correspondientes")


def main():
    # Defino objeto
    obj = BotWhatsapp()

    try:
        print("Abriendo Whatsapp web.")
        obj.start_browser()
    except Exception as e:
        print("No se pudo abrir WhatsApp web. ")
        print(e)

    option = ''

    while option != '0':
        option = input(str("Elija una opción:\n"
                           "1 - Controlar contactos\n"
                           "2 - Enviar mensaje a contactos existentes\n"
                           "3 - Controlar y enviar\n"
                           "0 - Cerrar\n"))

        if option == '1':
            # Descargo contactos
            print("Descarga y control de contactos.")
            contactosOriginales = readXLSasDF(path=xlsPath, name=xls)

            # Controlar lista de contactos para ver si existe
            obj.validate_contacts(contacts=contactosOriginales)

        elif option == '2':
            # Leo Dataframe y Envio mensajes
            print('Leyendo DF')
            contactos = readXLSasDF(path=xlsPath, name='ContactosExistentes.xlsx')
            print('Enviando mensajes')

            for index, row in contactos.iterrows():
                obj.send_message_to_contact(row['TELEFONO'], messageFormatted(row['NOMBRE']))

        elif option == '3':
            # Descargo contactos
            print("Descargando contactos.")
            contactosOriginales = readXLSasDF(path=xlsPath, name=xls)
            # Abro Chromium

            # Controlar lista de contactos para ver si existe
            print('Controlando contactos...')
            obj.validate_contacts(contacts=contactosOriginales)

            # Leo Dataframe y Envio mensajes
            print('Leyendo DF')
            contactos = readXLSasDF(path=xlsPath, name='ContactosExistentes.xlsx')
            print('Enviando mensajes')

            # Itero Dataframe y envío mensajes
            for index, row in contactos.iterrows():
                obj.send_message_to_contact(row['TELEFONO'], messageFormatted(row['NOMBRE']))


if __name__ == '__main__':
    main()
