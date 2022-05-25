
from .singleton import Singleton
from datetime import datetime

from functools import partial
from tornado import gen
from bokeh.models.widgets import PreText

from .main_doc import doc

import json


class LabStat(metaclass=Singleton):
    """
    Singleton class to hold all the information about the current experiment.
    Also holds the front panel message widgets because these widgets are
    universal for all components
    """

    def __init__(self) -> None:
        self.msg_list = list()
        self.pre_exp_msg = PreText(
            text='''After setting up params and remote servers, click Start to start.''', width=800, height=500, name="messages")

        self.stat = dict()

        # save front end panel pages so that different threads see the same doc
        self.root_names = ["dashboard", "setup",
                          "params", "schedule", "reports", "messages", "manual"]
        self.doc = doc

        self.doc.add_root(self.pre_exp_msg)

    def dump_stat(self, filename) -> None:
        with open(filename, 'w') as f:
            json.dump(self.stat, f, indent=4)

    def expmsg(self, t: str) -> None:
        """formats messages, then send it to front end via a callback"""
        # print(t)
        for i in t.split('\n'):
            self.msg_list.append(i)
        while len(self.msg_list) > 20:
            self.msg_list.pop(0)
        text = '\n'.join(self.msg_list)
        self.doc.add_next_tick_callback(
            partial(self.update_exp_msg, text))

    def fmtmsg(self, d: dict) -> None:
        """expmsg, but accepts a dict from json"""
        param = ""
        for i in d:
            if i != "success" and i != "message":
                param = param + ', '
                param = param + str(i)
                param = param + ':'
                param = param + str(d[i])

        msg_str = "[{time}][{success}] {message}{param}".format(
            time=str(datetime.now()),
            success="OK" if d["success"] else "Error",
            message=d["message"],
            param=param)

        self.expmsg(msg_str)

    @gen.coroutine
    def update_exp_msg(self, t):
        self.pre_exp_msg.text = t


lstat = LabStat()
