from flask import Flask, render_template, request
import qrcode
import PIL.Image

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def generate_qr():
    if request.method == 'POST':
        inputText = request.form['order_input']
        inputName = request.form['name_input']
        if len(inputText) != 0:
            data = getData(inputText, inputName)
            img = generateQRwithLogo(data)
            img.save('static/qr.png')
            return render_template('index.html', image="static/qr.png")
        else:
            return 'Ingresá un número de orden, por favor'
    else:
        return render_template('index.html')


def getData(order, name):
    telephone = "5493884701268"
    if name == "":
        baseMessage = f"Hola! Mi pedido es el {order}."
    else:
        baseMessage = f"Soy {name}! Mi pedido es el {order}."

    message = baseMessage.replace(" ", "%20")

    data = f"https://wa.me/{telephone}?text={message}"

    return data


def generateQRwithLogo(data):
    logo = PIL.Image.open('static/logo.png').convert('RGBA')
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

    gen_img.paste(logo, position, logo)
    return gen_img


if __name__ == '__main__':
    app.run(debug=True)
