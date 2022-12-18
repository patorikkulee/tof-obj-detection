import requests
import io
from flask import Flask, request, abort, redirect, send_file
from camera import *  # Rpi camera
from tof_utils import get_prev_n, log_line, draw_distribution


app = Flask(__name__)


@app.route("/text", methods=['GET'])
def text():
    text = "hello"
    return text


@app.route("/txtfile", methods=['GET'])
def file():
    f = open('test.txt')
    txtfile = f.read().replace('\n', '<br>')
    print(txtfile)
    return txtfile


@app.route("/searchcargoID", methods=['GET'])
def cargoIDlist():
    entries = get_prev_n(12)
    IDlist = list(entries.keys())# open('ID.txt')
    log_line(entries)
    IDfile = '<br>'.join(IDlist) # IDlist.read().replace('\n', '<br>')
    
    return IDfile


@app.route("/ID/txt/<id>", methods=['GET'])
def ID(id):
    ID = open('./IDfolder/'+id+'.txt', encoding="utf-8")
    IDfile = ID.read().replace('\n', '<br>')
    print(IDfile)
    with open(f"pictures/{id}.jpg", 'rb') as bites:
        pic = send_file(
            io.BytesIO(bites.read()),
            mimetype='image/jpg'
        )
        
    return IDfile

# @app.route("/pic", methods=['GET'])
@app.route("/ID/img/<id>", methods=['GET'])
def IDimg(id):
    with open(f"pictures/{id}.jpg", 'rb') as bites:
        return send_file(
            io.BytesIO(bites.read()),
            mimetype='image/png'
        )

@app.route("/volumedistribution", methods=['GET'])
def volumechart():
    draw_distribution('size')
    with open("./piecharts/size.png", 'rb') as bites:
        return send_file(
            io.BytesIO(bites.read()),
            mimetype='image/png'
        )

@app.route("/rpicameratakephoto", methods=['GET'])
def takepic():
    take_pic("123")
    with open("./pictures/123.jpg", 'rb') as bites:
        return send_file(
            io.BytesIO(bites.read()),
            mimetype='image/png'
        )
        
# @app.route("/rpicamerashootvideo", methods=['GET'])
# def shootvideo():
#     shoot_video("123")
#     with open("./videos/123.mp4", 'rb') as bites:
#         return send_file(
#             io.BytesIO(bites.read()),
#             mimetype='video/mp4'
#         )


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=7070, debug=True)
