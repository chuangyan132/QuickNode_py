#!
# @brief   
# @project QuickNode-1d90654c1a42267181e98389625213812f7feb4b
# @file    qn_Debug.py
# @author  Chuang Yan
# @email   Yanchuang1122@gmail.com  
# @license 
#     Copyright(C) Shining3D  
# @versions 
#     V0.1-ChuangYan 19/03/2024 13:38  
#

''' This is a debug script for Quicknode plugin development. '''

import createprocess
from qn_plugincore import *
from qn_pluginbusiness import *
from PyQt5.QtWidgets import QApplication
import sys
import json

plugin_core_dll = PluginCoreDLL(PATH_DLL)


if __name__ == "__main__":
    plugin_business = PluginBusiness(plugin_core_dll)
    rc = plugin_business.init(sys.argv)
    print("Initialization successful")





    message0 = "{\"cmdUuid\": \"uuid\", \"cmd\": \"create\", \"data\": {\"nodeClass\": \"QN_Sleep\",\"nodeId\": \"abc\"}}"

    # send first message: create node
    plugin_business.on_handle_message(message0, len(message0), None)

    message1 = """
       {
           "cmdUuid": "uuid",
           "cmd": "setInputs",
           "data": {
               "nodeId": "abc",
               "inputs": [
                   {
                       "name": "Time",
                       "isSharedMemory": false,
                       "value": 3
                   }
               ]
           }
       }
       """
    # send second message: set inputs
    plugin_business.on_handle_message(message1, len(message1), None)

    # send third message: setProperties
    message4 = """
            {
                "cmdUuid": "uuid",
                "cmd": "setProperties",
                "data": {
                    "nodeId": "abc",
                    "properties": [
                        {
                            "name": "Time1",
                            "isSharedMemory": false,
                            "value": 3
                        }
                    ]
                }
            }
            """
    plugin_business.on_handle_message(message4, len(message4), None)
    message2 = "{\"cmdUuid\": \"uuid\", \"cmd\": \"apply\", \"data\": {\"nodeClass\": \"QN_Sleep\",\"nodeId\": \"abc\"}}"

    # send fourth message: apply
    plugin_business.on_handle_message(message2, len(message2), None)

    # send fifth message: getOutputs
    message3 = "{\"cmdUuid\": \"uuid\", \"cmd\": \"getOutputs\", \"data\": {\"nodeId\": \"abc\", \"outputs\": [\"ret2\"]}}"
    plugin_business.on_handle_message(message3, len(message3), None)