from flask import Flask, request, render_template, jsonify, redirect, url_for, flash, abort
import time
from datetime import timedelta
import xml_to_csv as xtoc
import test
import test2
import tp4
import tp5
import os
import json


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

#训练页面
@app.route('/pretrpage')
def pretrpage():
    return render_template('tr.html')

#训练过程
@app.route('/trpage')
def trpage():
    res=xtoc.main()
    if res!=1:
        return 'Es gibt eine Fehler. Bite schauen Sie es in console'
    os.system("python3 generate_tfrecord_tr.py")
    os.system("python3 generate_tfrecord_te.py")
    os.system("python3 train.py")
    return 'Ok! <a href="/" onClick=”javascript :history.go(-1);”>back</a>'

#输出
@app.route('/output')
def output():
    os.system("python3 export_inference_graph.py")
    return 'Ok! <a href="/" onClick=”javascript :history.go(-1);”>back</a>'

#上传界面
@app.route('/uppage')
def uppage():
    return render_template('upload.html')

#上传以后的处理
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    #用时间命名图片id
    t=time.time()
    t=int(t)
    t=str(t)
    img_path = 'static/'
    img_name = '1.jpg'
    img_save = 'pic_'+t+'.jpg'
    imge=img_path+img_name
    imge2=img_path+img_save
    json_name = 'json_'+t+'.json'
    json_save =img_path+json_name
    if request.method == 'POST':
        #option = request.form['option']
        f = request.files['picture']
        if f==None:
            return 'You should update picture <a href="/" onClick=”javascript :history.go(-1);”>back</a>'
        f.save(imge)
        ou = test.check(imge,imge2)
        tp4.imge(imge2)
        out = test2.check(imge)
        out = tp5.text_xml(out,imge)
        with open(json_save, 'w') as f:
            json.dump(out, f)
            f.close()
        with open(img_path+'list.json', 'r') as f1:
            data = json.load(f1)
            item = [{'id':t}]
            data.append(item)
            #print(data[0]['id'])
            f1.close()
        with open(img_path+'list.json', 'w') as f2:
            json.dump(data, f2)
        return 'ok <a href="/" onClick=”javascript :history.go(-1);”>back</a>'
    else:
        return 'You should update picture <a href="/" onClick=”javascript :history.go(-1);”>back</a>'

#列出图片id列表
@app.route('/list_img', methods=['GET', 'POST'])
def list_img():
    img_path = 'static/'
    with open(img_path+'list.json', 'r') as f:
        data = json.load(f)
        result="<ul>"
        for d in data:
            idd=d[0]['id']
            result=result+'<li>'+idd+'&nbsp;&nbsp;<a href="/show_img?id='+idd+'&option=bild">picture</a>&nbsp;&nbsp;<a href="/show_img?id='+idd+'&option=json">json</a></li>'
        f.close()
    result=result+"</ul>"
    return result+'<p></p> <a href="/" onClick=”javascript :history.go(-1);”>back</a>'

#用id来显示图片或者json
@app.route('/show_img', methods=['GET', 'POST'])
def show_img():
    idd = request.args.get('id')
    option = request.args.get('option')
    img_path = 'static/'
    if option=='bild':
        img_name='pic_'+idd+'.jpg'
        imge=img_path+img_name
        ife=os.path.exists(imge)
        if ife==False:
            return render_template('404.html'), 404
        print("200 ok")
        return render_template('upload_ok.html', pic=imge)
    else:
        jso=img_path+'json_'+idd+'.json'
        ife=os.path.exists(jso)
        if ife==False:
            return render_template('404.html'), 404
        with open(jso, 'r') as f:
            data = json.load(f)
            f.close()
        print("200 ok")
        return json.dumps(data)


if __name__ == '__main__':
    app.debug = True
    app.run()
