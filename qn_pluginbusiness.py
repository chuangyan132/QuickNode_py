#!
# @brief   
# @project qn_pluginExe
# @file    qn_pluginbusiness.py
# @author  Chuang Yan
# @email   Yanchuang1122@gmail.com  
# @license 
#     Copyright(C) Shining3D  
# @versions 
#     V0.1-ChuangYan 08/03/2024 13:40  
#

import ctypes
import os
import sys
import json
from ctypes import *
from qn_plugincore import *
from qn_basenode import *
from ctypes import c_int, c_char_p, POINTER, c_void_p, c_size_t, byref


PATH_DLL = r'../qn_plugincore/plugincored.dll'

class PluginCoreDLL:
    def __init__(self, dll_path):
        self._library = ctypes.cdll.LoadLibrary(dll_path)


    def qn_init(self, host, port):
        self._library.qn_init.argtypes = [c_char_p, c_int]
        self._library.qn_init.restype = c_int
        return self._library.qn_init(host.encode('utf-8'), port)

    def qn_cleanup(self):
        self._library.qn_cleanup.restype = c_int
        return self._library.qn_cleanup()

    def qn_set_plugin_name(self, name):
        self._library.qn_set_plugin_name.argtypes = [c_char_p]
        self._library.qn_set_plugin_name.restype = c_int
        return self._library.qn_set_plugin_name(name.encode('utf-8'))

    def qn_version(self):
        self._library.qn_version.argtypes = [POINTER(c_int), POINTER(c_int), POINTER(c_int)]
        major = c_int()
        minor = c_int()
        patch = c_int()

        self._library.qn_version(byref(major), byref(minor), byref(patch))
        return major.value, minor.value, patch.value

    def qn_set_log_path(self, path):
        self._library.qn_set_log_path.argtypes = [c_char_p]
        self._library.qn_set_log_path.restype = c_int
        return self._library.qn_set_log_path(path.encode('utf-8'))

    def qn_send_command(self, command_data):
        if isinstance(command_data, str):
            command_data = command_data.encode('utf-8')

        self._library.qn_send_command.argtypes = [c_char_p, c_int]
        self._library.qn_send_command.restype = c_int
        return self._library.qn_send_command(command_data, len(command_data))

    def qn_set_userdata(self,key, user_data):
        if isinstance(key, str):
            key = key.encode('utf-8')
        if isinstance(user_data, str):
            user_data = user_data.encode('utf-8')
        elif isinstance(user_data, int):
            user_data = (ctypes.c_int(user_data)).value.to_bytes(4, byteorder='little')

        self._library.qn_set_userdata.argtypes = [c_char_p, c_char_p, c_int]
        self._library.qn_set_userdata.restype = c_int
        return self._library.qn_set_userdata(key, user_data, len(user_data))

    def qn_get_userdata(self, key):
        if isinstance(key, str):
            key = key.encode('utf-8')
        data = ctypes.c_char_p()
        length = ctypes.c_int()
        self._library.qn_get_userdata.argtypes = [c_char_p, POINTER(c_char_p), POINTER(c_int)]
        self._library.qn_get_userdata.restype = c_int
        return self._library.qn_get_userdata(key, byref(data), byref(length))

    def set_message_callback(self, callback):
        CALLBACK = CFUNCTYPE(None, c_char_p, c_size_t, c_void_p)
        self.callback = CALLBACK(callback)
        self._library.qn_set_message_callback.argtypes = [CALLBACK, c_void_p]
        self._library.qn_set_message_callback.restype = c_int
        return self._library.qn_set_message_callback(self.callback, None)

def parse_command(data):
    """
    Dummy function to simulate command helper class parsing.

    """
    cmd_data = json.loads(data)
    return cmd_data.get("cmdUuid"), cmd_data

class PluginBusiness:
    def __init__(self, plugin_core):
        self.plugin_core = plugin_core
        self.m_nodes = {}

    def init(self, argv):                                               # Initialize the plugin
        argc = len(argv)
        host = "127.0.0.1"
        port = 10086
        if argc >= 3:
            host = argv[1]
            port = int(argv[2])

        app_name = os.path.splitext(os.path.basename(argv[0]))[0]
        self.plugin_core.qn_set_plugin_name(app_name)
        rc = 1
        rc = self.plugin_core.qn_init(host, port)
        if rc != 0:
            print("Initialization failed")
            return rc
        version = self.plugin_core.qn_version()
        print(f"Plugin Core Version: {version[0]}.{version[1]}.{version[2]}")
        return rc

    def fini(self):
        return self.plugin_core.qn_cleanup()

    def send_nodes_desc(self):
        # Implementation placeholder
        return 0

    def on_handle_message(self, data, len1, p_user):
        cmd_uuid, cmd_data = parse_command(data)

        if cmd_data["cmd"] == "restart":
            self.on_restart(data, len1)
        elif cmd_data["cmd"] == "create":
            self.on_create(data, len1)

        elif cmd_data["cmd"] == "setInputs":
            self.on_Set_inputs(data, len1)
        elif cmd_data["cmd"] == "apply":
            self.on_apply(data, len1)
        elif cmd_data["cmd"] == "getOutputs":
            self.on_get_outputs(data, len1)
        elif cmd_data["cmd"] == "getProperties":
            self.on_get_properties(data, len1)
        elif cmd_data["cmd"] == "setProperties":
            self.on_set_properties(data, len1)
        elif cmd_data["cmd"] == "viewDatas":
            self.on_view_datas(data, len1)
        else:
            print(f"Unknown command: {cmd_data['cmd']}")




    def on_restart(self, data, len1):
        print("Restarting...")
        return 0
    def on_create(self, data, len1):
        helper = CreateCommandHelp(data)
        cmd_uuid = helper.command_uuid()
        node_class = helper.node_class()
        node_id = helper.node_id()

        print(f"m_nodes: {self.m_nodes}")
        if node_id not in self.m_nodes:
            print(f"1111.step: {self.m_nodes}")
            class_name = ClassFactory().create_object_by_name(node_class)
            #class_name = ClassFactory.instance().class_name(node_class)
            #class_name = ClassFactory.instance().class_name(node_class)
            if class_name:
                self.m_nodes[node_id] = class_name
                #node_obj = ClassFactory.instance().create_object_by_name(class_name)
                print(f"Creating node {node_id} of class {node_class}")
                print(f"m_nodes: {self.m_nodes}")
        reply = helper.generate_reply()
        print(f"Reply: {reply}")
        reply_bytes = reply.encode('utf-8')
        self.plugin_core.qn_send_command(reply_bytes)




        #return 0
    def on_Set_inputs(self, data, len1):
        helper = SetInputsCommandHelp(data)
        node_id = helper.node_id()
        if node_id in self.m_nodes:
            node_obj = self.m_nodes[node_id]
            rc = node_obj.setInput(data)
            reply = helper.generate_reply(rc)
            reply_bytes = reply.encode('utf-8')
            self.plugin_core.qn_send_command(reply_bytes)

    def on_apply(self, data, len1):
        helper = ApplyCommandHelper(data)
        node_id = helper.node_id()
        if node_id in self.m_nodes:
            node_obj = self.m_nodes[node_id]
            rc = node_obj.apply()
            reply = helper.generate_reply(rc)
            reply_bytes = reply.encode('utf-8')
            self.plugin_core.qn_send_command(reply_bytes)

    def on_get_outputs(self, data, len1):
        helper = GetOutputsCommandHelper(data)
        node_id = helper.node_id()
        if node_id in self.m_nodes:
            node_obj = self.m_nodes[node_id]
            datas = []
            outputs_name = helper.outputs_name()
            for name in outputs_name:
                print(f"Getting output: {name}")
                items = node_obj.output(name)
                datas.append(items)
                print(f"datas: {datas}")


            reply = helper.generate_reply(datas)
            reply_bytes = reply.encode('utf-8')
            self.plugin_core.qn_send_command(reply_bytes)

    def on_set_properties(self, data, len1):
        helper = SetPropertiesCommandHelp(data)
        node_id = helper.node_id()
        if node_id in self.m_nodes:
            node_obj = self.m_nodes[node_id]
            rc = node_obj.setProperty(data)
            reply = helper.generate_reply(rc)

            reply_bytes = reply.encode('utf-8')
            self.plugin_core.qn_send_command(reply_bytes)



    def on_get_properties(self, data, len1):
        pass
    def on_view_datas(self, data, len1):
        pass




