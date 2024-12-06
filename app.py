from flask import Flask, request, render_template
import requests  # Para fazer requisições HTTP
import pandas as pd
import os
from gerar_qr import gerar_qr  # Importa a função para gerar o QR Code

app = Flask(__name__)

# URL da sua nova API SheetDB
sheetdb_url = "https://sheetdb.io/api/v1/f3rydy81bjomo"

# Verifica se o arquivo convidados.xlsx existe, se não cria
if not os.path.exists('convidados.xlsx'):
    df = pd.DataFrame(columns=['Nome', 'Status'])
    df.to_excel('convidados.xlsx', index=False)

@app.route('/')
def home():
    return "Bem-vindo ao sistema de QR Code! Acesse /generate para criar um QR Code."

@app.route('/generate', methods=['GET', 'POST'])
def generate_qr_code():
    if request.method == 'POST':
        data = request.form.get('data')  # Nome enviado pelo formulário
        if data:
            # Chama a função de gerar QR Code
            gerar_qr(data)  # Chama o código para gerar o QR Code
            
            # Salva o nome na planilha
            df = pd.read_excel('convidados.xlsx')
            df = df.append({'Nome': data, 'Status': 'Pendente'}, ignore_index=True)
            df.to_excel('convidados.xlsx', index=False)

            # Exibe a imagem do QR Code gerado a partir da pasta 'static'
            return f"QR Code gerado para {data}! <br><img src='/static/{data}_qr.png' width='200'>"
        return "Nenhum dado enviado!"
    
    return '''
        <form method="post">
            Nome do convidado: <input type="text" name="data">
            <button type="submit">Gerar QR Code</button>
        </form>
    '''

# Rota para ler o QR Code e redirecionar para a página de aprovação
@app.route('/read_qr/<nome>')
def read_qr(nome):
    return render_template('approve.html', nome=nome)

# Rota para aprovação do convidado
@app.route('/approve/<nome>', methods=['GET', 'POST'])
def approve_convidado(nome):
    if request.method == 'POST':
        try:
            # Envia a requisição para atualizar o status do convidado para "Aprovado"
            response = requests.put(f"{sheetdb_url}/Nome/{nome}", json={"data": {"Status": "Aprovado"}})

            # Verifica se a requisição foi bem-sucedida
            if response.status_code == 200:
                return f"{nome} foi aprovado e o status foi atualizado para 'Aprovado'!"
            else:
                return f"Erro ao atualizar o status de {nome}. Código de erro: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Erro ao processar a requisição: {e}"

    return render_template('approve.html', nome=nome)

if __name__ == '__main__':
    app.run(debug=True)
