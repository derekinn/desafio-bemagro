from flask import Flask, request, send_file
from script import process_file
import tempfile
import os

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return "Nenhum arquivo enviado.", 400

        file = request.files['file']
        
        if file.filename == '':
            return "Nenhum arquivo selecionado.", 400

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir, file.filename)
            file.save(file_path)

            # Processa o(s) arquivo(s) fora do diretório temporário
            print("Iniciando o processamento do arquivo...")
            output_zip = process_file(file_path)  # Chamando a função do script.py

            if output_zip:
                try:
                    return send_file(output_zip, as_attachment=True)
                except Exception as e:
                    return f'Erro ao enviar o arquivo: {str(e)}', 500 
            else:
                 return "Erro ao processar o arquivo.", 500

    except Exception as e:
        return f'Erro ao processar o arquivo: {str(e)}', 500

if __name__ == "__main__":
    app.run(debug=True)