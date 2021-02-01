import os
from flask import Flask, request, redirect, url_for, render_template, send_from_directory
import pandas as pd
from werkzeug.utils import secure_filename
from PyPDF2 import PdfFileReader, PdfFileWriter

UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads/'
ALLOWED_EXTENSIONS = {'pdf', 'txt','jpeg','csv'}

app = Flask(__name__, static_url_path="/static")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER
# limit upload size upto 8mb
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/index1")
def home():
    return render_template("index1.html")

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        print(request.files['file'])
        print(allowed_file(request.files['file'].filename))
        if 'file' not in request.files:
            print('No file attached in request')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            extension_type = request.files['file'].filename.split('.')[1] 
            if extension_type == 'pdf':
              process_file(os.path.join(app.config['UPLOAD_FOLDER'], filename), filename)
              print('Uploaded folder and filename is {0},{1}'.format(app.config['UPLOAD_FOLDER'], filename))
              return redirect(url_for('uploaded_file', filename=filename))
            elif extension_type == 'csv':
              input_file = pd.read_csv(filepath_or_buffer = os.path.join(app.config['UPLOAD_FOLDER'], filename)) 

              table = filename.split('.')[0]  # Get name of the table

              # Get all "keys" inside "values" key of dictionary (column names)
              columns = ', '.join(list(input_file.columns))  

              # Get all "values" inside "values" key of dictionary (insert values)
              values = ', '.join(dictionary["values"].values())

              # Generate INSERT query
              print(f"INSERT INTO {table} ({columns}) VALUES ({values})" + "\n")


              # Generate QUERY for each dictionary inside data list
              for query in data:
                generate_insert_query(query)
              # input_file.to_csv(app.config['DOWNLOAD_FOLDER'] + filename)
              # output_stream = open(app.config['DOWNLOAD_FOLDER'] + filename, 'wb')
              # output.write(output_stream)
              return render_template("tables.html", column_names=input_file.columns.values, row_data=list(input_file.head().values.tolist()),
                            zip=zip)
    return render_template('index1.html')

@app.route("/analyse")
def analyse():
  return "in analyse"
def process_file(path, filename):
    remove_watermark(path, filename)
    # with open(path, 'a') as f:
    #    f.write("\nAdded processed content")


def remove_watermark(path, filename):
    input_file = PdfFileReader(open(path, 'rb'))
    output = PdfFileWriter()
    for page_number in range(input_file.getNumPages()):
        page = input_file.getPage(page_number)
        page.mediaBox.lowerLeft = (page.mediaBox.getLowerLeft_x(), 20)
        output.addPage(page)
    output_stream = open(app.config['DOWNLOAD_FOLDER'] + filename, 'wb')
    output.write(output_stream)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run()