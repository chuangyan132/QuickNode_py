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



PATH_DLL = r'D:\Reserch\bin\plugins\executable\qn_IQC\plugincore.dll'

class PluginCoreDLL:
    def __init__(self, dll_path):
        self.dll = CDLL(dll_path)                           # Load the DLL
        self._setup_functions()

    def _setup_functions(self):
        # Cleanup
        self.qn_cleanup = self.dll["?qn_cleanup@@YAHXZ"]
        self.qn_cleanup.restype = c_int

        # Free
        self.qn_free = self.dll["?qn_free@@YAXPEAX@Z"]
        self.qn_free.argtypes = [c_void_p]

        # Get UserData
        self.qn_get_userdata = self.dll["?qn_get_userdata@@YAHPEBDPEAPEADPEAH@Z"]
        self.qn_get_userdata.argtypes = [c_char_p, POINTER(POINTER(c_char_p)), POINTER(c_int)]
        self.qn_get_userdata.restype = c_int

        # Init (Overloaded version for host and port)
        self.qn_init = self.dll["?qn_init@@YAHPEBDH@Z"]
        self.qn_init.argtypes = [c_char_p, c_int]
        self.qn_init.restype = c_int

        # Malloc
        self.qn_malloc = self.dll["?qn_malloc@@YAPEAXH@Z"]
        self.qn_malloc.argtypes = [c_int]
        self.qn_malloc.restype = c_void_p

        # Receive Message
        self.qn_receive_message = self.dll["?qn_receive_message@@YAPEBDPEAPEADPEAH@Z"]
        self.qn_receive_message.argtypes = [POINTER(POINTER(c_char_p)), POINTER(c_int)]
        self.qn_receive_message.restype = c_char_p

        # Send Command
        self.qn_send_command = self.dll["?qn_send_command@@YAHPEBDH@Z"]
        self.qn_send_command.argtypes = [c_char_p, c_int]
        self.qn_send_command.restype = c_int

        # Send Message
        self.qn_send_message = self.dll["?qn_send_message@@YAHPEBDPEADH@Z"]
        self.qn_send_message.argtypes = [c_char_p, POINTER(c_char_p), c_int]
        self.qn_send_message.restype = c_int

        # Set Log Callback
        CALLBACKFUNC_LOG = ctypes.CFUNCTYPE(None, c_int, c_char_p, c_void_p)
        self.qn_set_log_callback = self.dll["?qn_set_log_callback@@YAHP6AXHPEBDPEAX@Z1@Z"]
        self.qn_set_log_callback.argtypes = [CALLBACKFUNC_LOG, c_void_p]
        self.qn_set_log_callback.restype = c_int

        # Set Log Path
        self.qn_set_log_path = self.dll["?qn_set_log_path@@YAHPEBD@Z"]
        self.qn_set_log_path.argtypes = [c_char_p]
        self.qn_set_log_path.restype = c_int

        # Set Message Callback
        CALLBACKFUNC_MSG = ctypes.CFUNCTYPE(None, c_char_p, c_size_t, c_void_p)
        self.qn_set_message_callback = self.dll["?qn_set_message_callback@@YAHP6AXPEBD_KPEAX@Z2@Z"]
        self.qn_set_message_callback.argtypes = [CALLBACKFUNC_MSG, c_void_p]
        self.qn_set_message_callback.restype = c_int

        # Set Plugin Name
        self.qn_set_plugin_name = self.dll["?qn_set_plugin_name@@YAHPEBD@Z"]
        self.qn_set_plugin_name.argtypes = [c_char_p]
        self.qn_set_plugin_name.restype = c_int

        # Set Statistics
        self.qn_set_statistics = self.dll["?qn_set_statistics@@YAHPEBDPEADH@Z"]
        self.qn_set_statistics.argtypes = [c_char_p, POINTER(c_char_p), c_int]
        self.qn_set_statistics.restype = c_int

        # Set UserData
        self.qn_set_userdata = self.dll["?qn_set_userdata@@YAHPEBDPEADH@Z"]
        self.qn_set_userdata.argtypes = [c_char_p, POINTER(c_char_p), c_int]
        self.qn_set_userdata.restype = c_int

        # Version
        self.qn_version = self.dll["?qn_version@@YAHPEAH00@Z"]
        self.qn_version.argtypes = [POINTER(c_int), POINTER(c_int), POINTER(c_int)]
        self.qn_version.restype = c_int

    def set_plugin_name(self, name):
        return self.qn_set_plugin_name(name.encode('utf-8'))

    def initialize(self, host, port):
        return self.qn_init(host.encode('utf-8'), port)

    def cleanup(self):
        return self.qn_cleanup()

    def send_command(self, reply, len1):
        return self.qn_send_command(reply, len1)

    def get_version(self):
        major, minor, patch = c_int(), c_int(), c_int()
        self.qn_version(byref(major), byref(minor), byref(patch))
        return major.value, minor.value, patch.value
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
        self.plugin_core.set_plugin_name(app_name)
        rc = 1
        rc = self.plugin_core.initialize(host, port)
        if rc != 0:
            print("Initialization failed")
            return rc
        version = self.plugin_core.get_version()
        print(f"Plugin Core Version: {version[0]}.{version[1]}.{version[2]}")
        return rc

    def fini(self):
        return self.plugin_core.cleanup()

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
        self.plugin_core.send_command(reply_bytes, len(reply_bytes))




        #return 0
    def on_Set_inputs(self, data, len1):
        helper = SetInputsCommandHelp(data)
        node_id = helper.node_id()
        if node_id in self.m_nodes:
            node_obj = self.m_nodes[node_id]
            rc = node_obj.setInput(data)
            reply = helper.generate_reply(rc)
            reply_bytes = reply.encode('utf-8')
            self.plugin_core.send_command(reply_bytes, len(reply_bytes))

    def on_apply(self, data, len1):
        helper = ApplyCommandHelper(data)
        node_id = helper.node_id()
        if node_id in self.m_nodes:
            node_obj = self.m_nodes[node_id]
            rc = node_obj.apply()
            reply = helper.generate_reply(rc)
            reply_bytes = reply.encode('utf-8')
            self.plugin_core.send_command(reply_bytes, len(reply_bytes))

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


            reply = helper.generate_reply(datas)
            reply_bytes = reply.encode('utf-8')
            self.plugin_core.send_command(reply_bytes, len(reply_bytes))

    def on_set_properties(self, data, len1):
        helper = SetPropertiesCommandHelp(data, len1)
        node_id = helper.node_id()
        if node_id in self.m_nodes:
            node_obj = self.m_nodes[node_id]
            rc = node_obj.setProperty(data)
            reply = helper.generate_reply(rc)



    def on_get_properties(self, data, len1):
        pass
    def on_view_datas(self, data, len1):
        pass




