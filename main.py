import createprocess
from qn_plugincore import *
from qn_pluginbusiness import *
from PyQt5.QtWidgets import QApplication
import sys
import json


plugin_core_dll = PluginCoreDLL(PATH_DLL)


dll_path = r'D:\Reserch\bin\plugins\executable\qn_IQC\plugincore.dll'
dll = CDLL(dll_path)

qn_set_message_callback = getattr(dll, "?qn_set_message_callback@@YAHP6AXPEBD_KPEAX@Z2@Z")
MessageCallback = CFUNCTYPE(None, c_char_p, c_size_t, c_void_p)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    plugin_business = PluginBusiness(plugin_core_dll)
    rc = plugin_business.init(sys.argv)
    print("Initialization successful")


    def callback_proxy(data, len, user_data):
        # 因为是通过代理函数调用，所以这里直接使用plugin_bussiness的实例方法
        plugin_business.on_handle_message(data, len, user_data)


    c_on_message = MessageCallback(callback_proxy)

    # 设置qn_set_message_callback函数的参数和返回类型
    qn_set_message_callback.argtypes = [MessageCallback, c_void_p]
    qn_set_message_callback.restype = c_int
    result = qn_set_message_callback(c_on_message, None)

    app.exec()
    while True:
        str_input = input()
        if str_input == "exit":
            break
        else:
            print("error command")

    # message1 = """
    # {
    #     "cmdUuid": "uuid",
    #     "cmd": "setInputs",
    #     "data": {
    #         "nodeId": "abc",
    #         "inputs": [
    #             {
    #                 "name": "lhs",
    #                 "isSharedMemory": false,
    #                 "value": "2024"
    #             }
    #         ]
    #     }
    # }
    # """
    # message0 = "{\"cmdUuid\": \"uuid\", \"cmd\": \"create\", \"data\": {\"nodeClass\": \"QN_core3\",\"nodeId\": \"abc\"}}"
    # plugin_business.on_handle_message(message0, len(message0), None)
    # plugin_business.on_handle_message(message1, len(message1), None)
    # message2 = "{\"cmdUuid\": \"uuid\", \"cmd\": \"apply\", \"data\": {\"nodeClass\": \"QN_core3\",\"nodeId\": \"abc\"}}"
    # plugin_business.on_handle_message(message2, len(message2), None)
    # message3 = "{\"cmdUuid\": \"uuid\", \"cmd\": \"getOutputs\", \"data\": {\"nodeId\": \"abc\", \"outputs\": [\"ret2\", \"ret9\", \"ret7\"]}}"
    # plugin_business.on_handle_message(message3, len(message3), None)

    # Clean up
    plugin_business.fini()