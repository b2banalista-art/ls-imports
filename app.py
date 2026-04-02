from flask import Flask, render_template, request, redirect, url_for
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

EMAIL = "LSIMPORTS.FAQ@GMAIL.COM"
SENHA = "kuzjrrchxzoxihoz"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    nome = request.form['nome']
    email_cliente = request.form['email']
    telefone = request.form['telefone']
    endereco = request.form['endereco']
    cep = request.form['cep']
    produto = request.form['produto']

    tipo_camisa = request.form.get('tipo_camisa')
    nome_personalizado = request.form.get('nome_personalizado')
    numero_personalizado = request.form.get('numero_personalizado')
    tamanho_chuteira = request.form.get('tamanho_chuteira')

    arquivo = request.files['print']
    caminho = os.path.join(UPLOAD_FOLDER, arquivo.filename)
    arquivo.save(caminho)

    msg = EmailMessage()
    msg['Subject'] = 'Novo Pedido - LS IMPORTS'
    msg['From'] = EMAIL
    msg['To'] = EMAIL

    msg.set_content(f"""
Novo pedido recebido!

Nome: {nome}
Email: {email_cliente}
Telefone: {telefone}
Endereço: {endereco}
CEP: {cep}

Produto: {produto}

Tipo camisa: {tipo_camisa}
Nome personalizado: {nome_personalizado}
Número: {numero_personalizado}

Tamanho chuteira: {tamanho_chuteira}
""")

    with open(caminho, 'rb') as f:
        msg.add_attachment(f.read(), maintype='image', subtype='jpeg', filename=arquivo.filename)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL, SENHA)
        smtp.send_message(msg)

    return redirect(url_for('sucesso'))

@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')

if __name__ == '__main__':
    app.run(debug=True)