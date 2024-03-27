#!
# @brief   
# @project qn_testlib
# @file    main.py
# @author  Chuang Yan
# @email   Yanchuang1122@gmail.com  
# @license 
#     Copyright(C) Shining3D  
# @versions 
#     V0.1-ChuangYan 21/03/2024 11:06  
#
import createprocess
from qn_plugincore import *
from qn_pluginbusiness import *
from PyQt5.QtWidgets import QApplication
import sys
import json

dll_path = r'../qn_plugincore/plugincored.dll'

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)


    plugin_core_dll = PluginCoreDLL(PATH_DLL)

    plugin_business = PluginBusiness(plugin_core_dll)
    rc = plugin_business.init(sys.argv)
    print("Initialization successful")


    # Define the callback proxy function
    def callback_proxy(data, len, user_data):
        # Assuming data needs to be decoded from bytes to string for JSON parsing
        decoded_data = data.decode('utf-8')
        plugin_business.on_handle_message(decoded_data, len, user_data)


    plugin_core_dll.set_message_callback(callback_proxy)
    app.exec()
    while True:
        str_input = input()
        if str_input == "exit":
            break
        else:
            print("error command")

    plugin_business.fini()





