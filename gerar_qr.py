import qrcode
import os

def gerar_qr(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    # Gera a imagem do QR code
    img = qr.make_image(fill='black', back_color='white')

    # Salva o arquivo na pasta 'static'
    img_path = os.path.join('static', f"{data}_qr.png")
    img.save(img_path)
