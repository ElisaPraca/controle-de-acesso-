import qrcode

def gerar_qr(nome):
    # Gerar a URL de aprovação para o convidado
    url = f"http://localhost:5000/approve/{nome}"  # Usando localhost, mas substitua pela URL de produção
    qr = qrcode.make(url)  # Gera o QR Code com a URL
    qr.save(f"{nome}_qr.png")  # Salva o QR Code com o nome do convidado
    print(f"QR Code gerado para {nome}: {nome}_qr.png")
