from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import *
import asyncio
from tof_utils import *
import pickle


default_style = "max-height: 250px;border: 2px solid #fff;border-radius: 25px;"


def write_pkl(x):
    with open('theThing.pkl', 'wb') as f:
        pickle.dump(x, f)


def read_pkl():
    with open('theThing.pkl', 'rb') as f:
        return pickle.load(f)


def show_attributes(object):
    put_table([
        ['Attributes', 'Value'],
        ['object ID', object.serialID],
        ['length of X', str(object.x)+' mm'],
        ['length of Y', str(object.y)+' mm'],
        ['length of Z', str(object.z)+' mm'],
        ['object volumn', put_html(f'{object.volumn} cm<sup>3</sup>')],
        ['object size range', object.size()]
    ])


def show_img(object):
    put_image(open(object.pic_path, 'rb').read()).style(default_style)


def put_history(data):
    history = []
    for objID in data:
        history.append(put_table([
            ['Attributes', 'Value'],
            ['object ID', objID],
            ['length of X', str(data[objID]['x'])+" mm"],
            ['length of Y', str(data[objID]['y'])+" mm"],
            ['length of Z', str(data[objID]['z'])+" mm"],
            ['object volumn', put_html(f"{data[objID]['volumn']} cm<sup>3</sup>")],
            ['object size range', data[objID]['size']]
        ]))
        history.append(put_image(open(data[objID]['picture'], 'rb').read()).style(default_style))
        history.append(put_markdown(r'---'))
    history.append(put_button('Close', onclick=close_popup, outline=True))
    
    return history


def show_prev():
    popup('Previous 3 objects', put_history(get_prev_3()), size=PopupSize.NORMAL)


def show_charts():
    draw_distribution('size')

    popup('statistic charts', 
    put_image(open('piecharts/size.png', 'rb').read()).style(default_style),
    size=PopupSize.NORMAL)


async def main():
    """
    ToF sensor demo
    """

    put_row([put_markdown(r'# **ToF object detection** 🥹🥹🥹🥹🥹')],
            size='1fr auto', position=0).style('align-items:center')

    put_text('This is a demo webpage for the 111-1 Introduction to IoT course term project of ToF object detection.')
    set_scope('newobj')
    # tmp = obj(40,20,300,"123")
    
    # put_row(show_attributes(tmp))
    
    # put_markdown(r'## Picture')
    # show_img(tmp)
    async def bg_task():
        while 1:
            newobj = read_pkl()
            if newobj:
                print(newobj)
                with use_scope('newobj', clear=True):
                    put_markdown(r'## Information')
                    put_row(show_attributes(newobj))

                    put_markdown(r'## Picture')
                    show_img(newobj)

                    write_pkl(None)
            
            await asyncio.sleep(1)

    run_async(bg_task())


    put_markdown(r'## Show previous results')
    put_button("show previous results", onclick=show_prev)

    put_markdown(r'## Show statistic charts')
    put_button("show statistic charts", onclick=show_charts)


if __name__ == '__main__':
    start_server(main, debug=True, port=8080)
