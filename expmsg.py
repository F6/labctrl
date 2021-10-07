# -*- coding: utf-8 -*-

"""expmsg.py:
This module provides the Bokeh UI widgets for 
outputing messages to Output section
"""

__author__ = "Zhi Zi"
__email__ = "x@zzi.io"
__version__ = "20211003"

from functools import partial
from tornado import gen
from bokeh.models.widgets import Div

from main_doc import doc

div_exp_msg = Div(
    text='<pre>After setting up params and remote servers, click Start to start.</pre>')

msg_list = []


def expmsg(t:str) -> None:
    """formats messages, then send it to front end via a callback"""
    # print(t)
    for i in t.split('\n'):
        msg_list.append(i)
    while len(msg_list) > 20:
        msg_list.pop(0)
    text = '<pre>' + '\n'.join(msg_list) + '</pre>'
    doc.add_next_tick_callback(partial(update_exp_msg, text))


@gen.coroutine
def update_exp_msg(t):
    div_exp_msg.text = t
