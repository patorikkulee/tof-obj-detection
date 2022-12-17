from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
# from pywebio.session import info as session_info
# import asyncio
from tof_utils import *


def show_attributes(object):
    put_table([
        ['Attributes', 'Value'],
        ['object ID', object.serialID],
        ['length of X', object.x],
        ['length of Y', object.y],
        ['length of Z', object.z],
        ['object volumn', object.volumn],
        ['object size range', object.size()]
    ])


def show_img(object):
    put_image(open(object.pic_path, 'rb').read()).style("""
        max-height: 250px;
        border: 2px solid #fff;
        border-radius: 25px;
        """)


def put_history(data):
    history = []
    for objID in data:
        history.append(put_table([
            ['Attributes', 'Value'],
            ['object ID', objID],
            ['length of X', data[objID]['x']],
            ['length of Y', data[objID]['y']],
            ['length of Z', data[objID]['z']],
            ['object volumn', data[objID]['volumn']],
            ['object size range', data[objID]['size']]
        ]))
        history.append(put_image(open(data[objID]['picture'], 'rb').read()).style("""
            max-height: 250px;
            border: 2px solid #fff;
            border-radius: 25px;
            """))
        history.append(put_markdown(r'---'))
    history.append(put_button('Close', onclick=close_popup, outline=True))
    
    return history


def show_popup():
    popup('Previous 3 objects', put_history(get_latest_3()), size=PopupSize.NORMAL)


def main():
    """
    ToF sensor demo
    """

    put_row([put_markdown(r'# **ToF object detection** 🥹🥹🥹🥹🥹')],
            size='1fr auto', position=0).style('align-items:center')

    put_text('This is a demo webpage for the 111-1 Introduction to IoT course term project of ToF object detection.')
    tmp = obj(40,20,300,"123")
    
    put_markdown(r'## Information')
    put_row(show_attributes(tmp))
    
    put_markdown(r'## Picture')
    show_img(tmp)

    put_markdown(r'## Show previous results')
    put_button("show previous results", onclick=show_popup)


if __name__ == '__main__':
    start_server(main, debug=True, port=8080)
