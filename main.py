from distutils.log import debug
import os
# from sys import ps1
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import send_from_directory,render_template
import sqlite3

UPLOAD_FOLDER = 'UPLOAD_FOLDER'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

con = sqlite3.connect('example.db',check_same_thread = False)
cur = con.cursor()

def init_db():
    try:
        cur.execute('''CREATE TABLE pics (pname text,price real,desc text)''')
        con.commit()
    except:pass
    

init_db()

def displayAllIMages(images):
    # print(images)
    return render_template("gallery.html",images=images)



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    # post block 
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # filename="3.jpeg"
            print(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # save file name to DB
            sql =f"INSERT INTO pics VALUES ('{filename}',{request.form.get('price')},'{request.form.get('desc')}')"
            # print(sql)
            cur.execute(sql)
            con.commit()
            # print to terminal all saved files
            images=[]
            for row in cur.execute('SELECT * FROM pics'):
                images.append([row[0],row[1],row[2]])
                # print(row)

            print(images)
            return displayAllIMages(images)
            # print(request.form.get('price'))
            # return redirect(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # return 'imgaes'

            # return redirect(url_for('download_file', name=filename))
            # Get block
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File aaa</h1>
    <form method=post enctype=multipart/form-data>
      Img<input type=file name=file>
      Price <input name=price>
      Desc <input  name=desc>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == '__main__':
    app.run(debug=True)
