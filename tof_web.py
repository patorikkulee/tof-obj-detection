from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
# from pywebio.session import info as session_info
# import asyncio
# from tof_utils import *


def get_size_range(vol):
    assert vol >= 0
    big = 200
    small = 100

    if vol > big:
        return 'large'
    elif vol < small:
        return 'small'
    else:
        return 'medium'


def show_attributes(x, y, z, vol):
    put_table([
        ['Attributes', 'Value'],
        ['object ID', 'TBD'],
        ['length of X', x],
        ['length of Y', y],
        ['length of Z', z],
        ['object volumn', vol],
        ['object size range', get_size_range(vol)]
    ])


def show_img(path):
    put_image(open(path, 'rb').read()).style("""
        max-height: 250px;
        border: 2px solid #fff;
        border-radius: 25px;
        """)


def show_popup():
    popup('Previous 3 objects', [
        'Popup body text goes here.',
        put_table([
            ['Type', 'Content'],
            ['html', put_html('X<sup>2</sup>')],
            ['text', '<hr/>'],
            ['buttons', put_buttons(['A', 'B'], onclick=toast)],
            ['markdown', put_markdown('`Awesome PyWebIO!`')],
            ['file', put_file('hello.text', b'')],
            ['table', put_table([['A', 'B'], ['C', 'D']])]
        ]),
        put_image(
            open("hi.jpg", 'rb').read()),
        put_button('Close', onclick=close_popup, outline=True)
    ], size=PopupSize.NORMAL)


def main():
    """
    ToF sensor demo
    """

    put_row([put_markdown(r'# **ToF object detection** 🥹🥹🥹🥹🥹')],
            size='1fr auto', position=0).style('align-items:center')

    put_text('This is a demo webpage for the 111-1 Introduction to IoT term project of ToF object detection.')
    
    put_markdown(r'## Information')
    put_row(show_attributes(4, 5, 6, 120))
    
    put_markdown(r'## Picture')
    show_img(path)

    put_markdown(r'## Show previous results')
    put_button("show previous results", onclick=show_popup)


if __name__ == '__main__':
    start_server(main, debug=True, port=8080)
