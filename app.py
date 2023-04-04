import os
from flask import Flask
app = Flask(__name__)

@app.route('/l')
def hello_world():
   return '𝐇𝐨𝐥𝐚, 𝐃𝐞 𝐀𝐧𝐭𝐞𝐦𝐚𝐧𝐨 𝐆𝐫𝐚𝐜𝐢𝐚𝐬 𝐩𝐨𝐫 𝐌𝐚𝐧𝐭𝐞𝐫 𝐌𝐢 𝐒𝐞𝐫𝐯𝐢𝐜𝐢𝐨 𝐀𝐜𝐭𝐢𝐯𝐨 😊 𝐄𝐫𝐞𝐬 𝐍𝐮𝐞𝐬𝐭𝐫𝐚 𝐑𝐚𝐳𝐨́𝐧 𝐃𝐞 𝐒𝐞𝐫'

from flask import Flask, request, render_template
from tqdm import tqdm
import requests
import json


@app.route('/', methods=['GET', 'POST'])
def download_file():
    if request.method == 'POST':
        session = requests.Session()
        login_data = {
            'username': "stvz02",
            'password': "stvz02**"
        }
        session.post("https://anuarioeco.uo.edu.cu/index.php/aeco/login/signIn", data=login_data)
        input_str = request.form['files']
        try:
            files_dict = json.loads(input_str)
            if isinstance(files_dict, dict):
                files_dict = [files_dict]
        except:
            id_archive, filename = input_str.split()
            files_dict = [{"id": id_archive, "name": filename}]
        for file_dict in files_dict:
            id_archive = file_dict["id"]
            filename = file_dict["name"]
            download_url = f'https://anuarioeco.uo.edu.cu/index.php/aeco/$$$call$$$/api/file/file-api/download-file?submissionFileId={id_archive}&submissionId=5736&stageId=1'
            response = session.head(download_url)
            response = session.get(download_url, stream=True)
            total_size_in_bytes = int(response.headers.get('content-length', 0))
            block_size = 1024
            progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
            with open('/storage/emulated/0/Download/'+filename, 'wb') as file:
                for data in response.iter_content(block_size):
                    progress_bar.update(len(data))
                    file.write(data)
            progress_bar.close()
        return 'Archivos descargados exitosamente!'
    else:
        return render_template('index.html')

