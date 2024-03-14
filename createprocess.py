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
def register(cmd_name):
    def decorator(cls):
        create_func = lambda: cls()
        RegisterAction(cmd_name, create_func)
        return cls
    return decorator





# class RobotHansNode(BaseNode):
#     def __init__(self):
#         super().__init__()
#         self.node_name = "QN_core"
#
#     def apply(self):
#         print("Performing a long-running task...")
#         print("Performing a long-running task...")
#         print("Performing a long-running task...")
#         print("Performing a long-running task...")
#         print("Performing a long-running task...")
#         print("Performing a long-running task...")
#         print("Performing a long-running task...")
#         print("Performing a long-running task...")
#
#         ret1 = 20008
#
#
#         output_ret = {}
#         output_ret["name"] = "ret"
#         output_ret["isSharedMemory"] = False
#         output_ret["value"] = ret1
#
#         output_json = json.dumps(output_ret, indent=4)
#         self._setOutput("ret", output_json)
#
#         # 模拟耗时操作
#         return "Task completed"

@register("QN_core1")
class QNCore1(BaseNode):
    def __init__(self):
        super().__init__()
        self.node_name = "QN_core1"

    def apply(self):
        rc = 0
        print("1111111111111111111111111111111111111111111111")
        print("Performing a long-running task from QNCore1...")
        # 模拟耗时操作
        ret2 = 22222


        output_ret2 = {}
        output_ret2["name"] = "ret2"
        output_ret2["isSharedMemory"] = False
        output_ret2["value"] = ret2
        output_json2 = json.dumps(output_ret2, indent=4)
        self._setOutput("ret2", output_json2)


        return rc

@register("QN_core2")
class QNCore2(BaseNode):
    def __init__(self):
        super().__init__()
        self.node_name = "QN_core2"

    def apply(self):
        rc = 0
        print("22222222222222222222222222222222222222222")
        print("Performing a long-running task QNCore2...")
        # 模拟耗时操作
        ret7 = 20008
        output_ret = {}
        output_ret["name"] = "ret7"
        output_ret["isSharedMemory"] = False
        output_ret["value"] = ret7
        output_json = json.dumps(output_ret, indent=4)
        self._setOutput("ret7", output_json)
        return rc

@register("QN_core3")
class QNCore3(BaseNode):
    def __init__(self):
        super().__init__()
        self.node_name = "QN_core3"

    def apply(self):
        rc = 0
        print("333333333333333333333333333333333333333333")
        print("Performing a long-running task QNCore3...")
        # 模拟耗时操作

        ret9 = "ccccc"

        output_ret9 = {}
        output_ret9["name"] = "ret9"
        output_ret9["isSharedMemory"] = False
        output_ret9["value"] = ret9
        output_json9 = json.dumps(output_ret9, indent=4)
        self._setOutput("ret9", output_json9)
        return rc