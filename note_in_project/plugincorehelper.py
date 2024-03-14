#!
# @brief   
# @project qn_pluginExe
# @file    plugincorehelper.py
# @author  Chuang Yan
# @email   Yanchuang1122@gmail.com  
# @license 
#     Copyright(C) Shining3D  
# @versions 
#     V0.1-ChuangYan 08/03/2024 14:28  
#

import json

class ClassFactory:
    _instance = None
    class_map = {}
    node_class = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def create_object_by_name(self, class_name):
        return self.class_map.get(class_name, lambda: None)()

    def register_class(self, cmd_name, class_name, creator):
        self.class_map[class_name] = creator
        self.node_class[cmd_name] = class_name

def register(cmd_name, class_name):
    def decorator(creator):
        factory = ClassFactory()
        factory.register_class(cmd_name, class_name, creator)
        return creator
    return decorator

class BaseCommand:
    def __init__(self, data):
        self.data = json.loads(data)
        self.m_cmdUuid = self.data.get('cmdUuid', '')
        self.m_cmd = self.data.get('cmd', '')
        self.m_nodeId = self.data.get('nodeId', '')
        self.m_jsonData = self.data.get('data', {})

    def is_active(self):
        return bool(self.data)

    def query_command_element(self, element):
        # Directly retrieve element if it's a top-level key
        if element in self.data and isinstance(self.data[element], str):
            return self.data[element]

        # Retrieve element from 'data' if it's a dictionary/object
        if isinstance(self.m_jsonData, dict) and element in self.m_jsonData:
            return self.m_jsonData[element]

        return ''

    def command(self):
        return self.m_cmd

    def command_uuid(self):
        return self.m_cmdUuid

    def node_id(self):
        return self.m_nodeId

    def data_styled_string(self):
        if isinstance(self.m_jsonData, dict):
            return json.dumps(self.m_jsonData, indent=4)
        return ''

    def generate_reply(self, result=0, why=''):
        reply = {
            'cmdUuid': self.m_cmdUuid,
            'cmd': f'{self.m_cmd}Reply',
            'result': result,
            'why': why,
            'data': {
                'nodeId': self.m_nodeId
            }
        }
        return json.dumps(reply)

class RestartCommandHelp(BaseCommand):
    def __init__(self, data):
        super().__init__(data)


class CreateCommandHelp(BaseCommand):
    def __init__(self, data):
        super().__init__(data)  # Initialize the BaseCommand part of the object
        self.m_nodeClass = self.query_command_element("nodeClass")

    def node_class(self):
        return self.m_nodeClass

class SetInputsCommandHelp(BaseCommand):
    def __init__(self, data):
        super().__init__(data)
        # Additional initialization or methods specific to SetInputsCommandHelp can be added here

class ApplyCommandHelper(BaseCommand):
    def __init__(self, data):
        super().__init__(data)
