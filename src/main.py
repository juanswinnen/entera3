"""
Simple QR Generator with user input for sending WhatsApp messages.

credits: https://pythonguides.com/python-qr-code-generator/
"""
from tkinter import *
from tkinter import messagebox
import tkinter.font as font
import qrcode
import PIL.Image


def getData(order):
    telephone = "5493884701268"
    baseMessage = f"Buenas! Mi pedido es el {order}."
    message = baseMessage.replace(" ", "%20")

    data = f"https://wa.me/{telephone}?text={message}"

    return data


def main():
    # front parameters
    winBg = "#fdfeff"
    customFont = "Comfortaa"

    window = Tk()
    window.geometry("650x750")
    window.title("Generador de QR - Cafe by Paula")
    window.config(bg=winBg)

    # generate qr code
    def generate_qr():
        inputText = user_input.get()
        if len(inputText) != 0:
            # Data to be encoded
            data = getData(inputText)

            # regular process
            global qr, img
            img = generateQRwithLogo(data)
        else:
            messagebox.showwarning(title='Ojaldre', message='Sin número de pedido no hay QR!')

        try:
            display_code()
        except:
            pass

    # show qr code
    def display_code():
        img_lbl.config(image=img)
        output.config(text=f"Escaneate el QR del pedido {user_input.get()}.",
                      font=font.Font(family=customFont))

    # title label
    lbl = Label(
        window,
        text="Indicá el número de pedido:",
        font=font.Font(family=customFont, size=20),
        bg=winBg
    )
    lbl.pack(pady=10)

    # user input
    user_input = StringVar()
    entry = Entry(
        window,
        justify="center",
        font=font.Font(family=customFont),
        textvariable=user_input
    )
    entry.pack(pady=10)

    # button to initiate
    button = Button(
        window,
        font=font.Font(family=customFont, size=12),
        text="Vamoo!",
        width=10,
        command=generate_qr
    )
    button.pack(pady=10)

    # foot label
    img_lbl = Label(
        window,
        bg=winBg)
    img_lbl.pack()

    # empty space for future qr
    output = Label(
        window,
        text="",
        bg=winBg
    )
    output.pack()

    # exec without closing
    window.mainloop()


def generateQRwithLogo(data):

    logo = PIL.Image.open('logo.png')
    basic = 100
    width_percentage = (basic / float(logo.size[0]))
    height_size = int((float(logo.size[1]) * float(width_percentage)))
    logo = logo.resize((basic, height_size), PIL.Image.Resampling.LANCZOS)

    qrc = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qrc.add_data(data)
    qrc.make()
    gen_img = qrc.make_image(
        fill_color='#35363a',
        bg_color="#fdfeff"
    ).convert('RGBA')

    position = ((gen_img.size[0] - logo.size[0]) // 2, (gen_img.size[1] - logo.size[1]) // 2)

    gen_img.paste(logo, position)
    gen_img.save('myqr.png')

    qrWithLogo = PhotoImage(file="myqr.png")

    return qrWithLogo


if __name__ == "__main__":
    main()
