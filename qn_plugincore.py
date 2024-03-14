#!
# @brief   
# @project qn_pluginExe
# @file    qn_plugincore.py
# @author  Chuang Yan
# @email   Yanchuang1122@gmail.com  
# @license 
#     Copyright(C) Shining3D  
# @versions 
#     V0.1-ChuangYan 11/03/2024 10:23  
#
import json
import time


class ClassFactory:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ClassFactory, cls).__new__(cls)
            cls._class_map = {}
        return cls._instance

    def register_class(self, cmd_name, create_func):
        self._class_map[cmd_name] = create_func

    def create_object_by_name(self, cmd_name):
        create_func = self._class_map.get(cmd_name)
        if create_func is not None:
            return create_func()
        return None


class RegisterAction:
    def __init__(self, cmd_name, create_func):
        factory = ClassFactory()
        factory.register_class(cmd_name, create_func)



class BaseCommand:
    def __init__(self, data):
        self.data = json.loads(data)
        self.m_cmdUuid = self.data.get('cmdUuid', '')
        self.m_cmd = self.data.get('cmd', '')
        self.m_jsonData = self.data.get('data', {})
        self.m_nodeId = self.query_command_element("nodeId")
        # self.m_nodeClass = self.query_command_element("nodeClass")

    def is_active(self):
        return bool(self.data)

    def query_command_element(self, element):
        # Check if element is a top-level key
        if element in self.data and isinstance(self.data[element], str):
            return self.data[element]

        # Check if 'data' is a dictionary and contains the element
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
        super().__init__(data)
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
class GetOutputsCommandHelper(BaseCommand):
    def __init__(self, data):
        super().__init__(data)
        # Python's initializer simply calls the superclass initializer

    def generate_reply(self, outputs_data, result=0, why=""):
        root = {}
        root["cmdUuid"] = self.m_cmdUuid
        root["cmd"] = self.m_cmd + "Reply"
        root["result"] = result
        root["why"] = why

        # Prepare the JSON data with outputs
        json_data = {"nodeId": self.m_nodeId, "outputs": []}
        for item in outputs_data:
            # Assume each item in outputs_data is already a JSON string,
            # convert it to a Python dictionary and append to the outputs list
            array_element = json.loads(item)
            json_data["outputs"].append(array_element)

        root["data"] = json_data

        # Convert the root dictionary to a JSON string
        return json.dumps(root, ensure_ascii=False, indent=None)

    def outputs_name(self):
        # Extract output names if available
        vec = []
        if self.m_jsonData and "outputs" in self.m_jsonData:
            outputs = self.m_jsonData["outputs"]
            if isinstance(outputs, list):
                for item in outputs:
                    if isinstance(item, str):
                        vec.append(item)
        return vec
class SetPropertiesCommandHelp(BaseCommand):
    def __init__(self, data):
        super().__init__(data)
class GetPropertiesCommandHelper(BaseCommand):
    def __init__(self, data):
        super().__init__(data)
        # Additional initialization or methods specific to GetPropertiesCommandHelper can be added here

    def generate_reply(self, outputs_data, result=0, why=""):
        root = {
            "cmdUuid": self.m_cmdUuid,
            "cmd": self.m_cmd + "Reply",
            "result": result,
            "why": why,
            "data": {
                "nodeId": self.m_nodeId,
                "properties": []
            }
        }

        for item in outputs_data:
            # Assuming each item in outputs_data is a JSON string,
            # convert it to a Python dictionary and append to the properties list
            array_element = json.loads(item)
            root["data"]["properties"].append(array_element)

        # Convert the root dictionary to a JSON string
        return json.dumps(root, ensure_ascii=False, indent=None)

    def properties_name(self):
        # Extract property names if available
        vec = []
        if self.m_jsonData and "properties" in self.m_jsonData:
            for item in self.m_jsonData["properties"]:
                # Assuming each item in the properties list is a dictionary with a name field
                if isinstance(item, dict) and "name" in item:
                    vec.append(item["name"])
        return vec