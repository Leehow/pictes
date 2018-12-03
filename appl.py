from flask import Flask, request, render_template, jsonify, redirect, url_for, flash, abort
import time
from datetime import timedelta
import xml_to_csv as xtoc
import test
import test2
import tp4
import tp5
import os


app = Flask(__name__)
app.secret_key = 'some_secret'


# 设置静态文件缓存过期时间
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)


@app.route('/error')
def error():
    abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/pretrpage')
def pretrpage():
    return render_template('tr.html')

@app.route('/trpage')
def trpage():
    res=xtoc.main()
    if res!=1:
        return 'Es gibt eine Fehler. Bite schauen Sie es in console'
    os.system("python3 generate_tfrecord_tr.py")
    os.system("python3 generate_tfrecord_te.py")
    os.system("python3 train.py")
    return 'Ok! <a href="/" onClick=”javascript :history.go(-1);”>back</a>'

@app.route('/output')
def output():
    os.system("python3 export_inference_graph.py")
    return 'Ok! <a href="/" onClick=”javascript :history.go(-1);”>back</a>'

@app.route('/uppage')
def uppage():
    return render_template('upload.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    img_path = 'static/'
    img_name = '1.jpg'
    imge=img_path+img_name
    if request.method == 'POST':
        #option = request.form['option']
        f = request.files['picture']
        if f==None:
            return 'You should update picture <a href="/" onClick=”javascript :history.go(-1);”>back</a>'
        f.save(imge)
#        ou=jsonify(test.check())
#        return option
#        ou = test.check()
        #anay_url=url_for('anay')+"?pic="+img_name+"&option="+option
        #flash('You were successfully updated!')
        #time.sleep(2)
        #flash('You were successfully updated!')
        return render_template('upload2.html', pic=img_name)
        

@app.route('/anay', methods=['GET', 'POST'])
def anay():
    img_name = request.args.get('pic')
    option = request.args.get('option')
    img_path = 'static/'
    img_name2 = 'show.jpg'
    imge=img_path+img_name
    imge2=img_path+img_name2

    if option=='bild':
            ou = test.check(imge)
            tp4.imge(imge2)
            
            return render_template('upload_ok.html')
            #return '<img src="'+img_stream+'" /><br/><br/>Ok! <a href="/uppage" onClick=”javascript :history.go(-1);”>back</a>'
#            os.system("python3 tp5.py")
    else:
            ou = test2.check(imge)
            ou = tp5.text_xml(ou,imge)
            return ou


if __name__ == '__main__':
    app.debug = True
    app.run()
