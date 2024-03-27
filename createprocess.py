#!
# @brief   
# @project qn_pluginExe
# @file    createprocess.py
# @author  Chuang Yan
# @email   Yanchuang1122@gmail.com  
# @license 
#     Copyright(C) Shining3D  
# @versions 
#     V0.1-ChuangYan 12/03/2024 14:42  
#
from qn_plugincore import *
from qn_basenode import *
import json
import Robotiq_gripper
import time



@register("QN_Sleep")
class QNSleep(BaseNode):
    def __init__(self):
        super().__init__()
        self.node_name = "QN_Sleep"

    def apply(self):
        rc = 0
        rc1 = -2147483647


        port = self._property("Time1")
        data = json.loads(port)
        Time1 = data["value"]
        rc = self.check_value(Time1)
        # ret2 = 2
        # output_ret = {}
        # output_ret["name"] = "ret2"
        # output_ret["isSharedMemory"] = False
        # output_ret["value"] = ret2
        # output_json = json.dumps(output_ret, indent=4)
        # self._setOutput("ret2", output_json)  # set the output port

        if rc != 0:
            return rc1
        else:
            time.sleep(Time1)
            return rc