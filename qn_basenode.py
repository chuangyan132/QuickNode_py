#!
# @brief   
# @project qn_pluginExe
# @file    qn_basenode.py
# @author  Chuang Yan
# @email   Yanchuang1122@gmail.com  
# @license 
#     Copyright(C) Shining3D  
# @versions 
#     V0.1-ChuangYan 11/03/2024 12:51  
#
import json
from qn_BasicType import *
from qn_ErroType import *

class BaseNode:
    def __init__(self):
        self.m_inputs = {}
        self.m_properties = {}
        self.m_outputs = {}
        self.m_descriptor = ""
        self.m_nodeName = ""

    def apply(self):
        raise NotImplementedError("Subclasses should implement this!")

    def setInput(self, data):
        try:
            root = json.loads(data)
            if root and "data" in root and "inputs" in root["data"] and isinstance(root["data"]["inputs"], list):

                for arrayElement in root["data"]["inputs"]:

                    if "name" in arrayElement:

                        inputName = arrayElement["name"]
                        self.m_inputs[inputName] = json.dumps(arrayElement, indent=4)
                        print(self.m_inputs[inputName])
            return QN_OK
        except json.JSONDecodeError:
            return QN_FAIL

    def setProperty(self, data):
        try:
            root = json.loads(data)
            if root and isinstance(root, dict) and "properties" in root and isinstance(root["properties"], list):
                for arrayElement in root["properties"]:
                    if isinstance(arrayElement, dict) and "name" in arrayElement:
                        propertyName = arrayElement["name"]
                        # If name exists, replace value; else, add new property
                        self.m_properties[propertyName] = json.dumps(arrayElement, indent=4)
            return QN_OK
        except json.JSONDecodeError:
            return QN_FAIL

    def property(self, name):
        return self.m_properties.get(name, "")

    def output(self, name):
        return self.m_outputs.get(name, "")

    def nodeDesc(self):
        return self.m_descriptor

    def nodeName(self):
        return self.m_nodeName

    def _hasInput(self, name):
        if name in self.m_inputs:
            return QN_OK
        else:
            return QN_NOT_FIND

    def _hasInputs(self, inputs):
        for item in inputs:
            result = self._hasInput(item)
            if result != QN_OK:
                return result
        return QN_OK

    def _input(self, name):
        return self.m_inputs.get(name, "")

    def _setOutput(self, name, data):
        self.m_outputs[name] = data
        return QN_OK

    def _hasProperty(self, name):
        if name in self.m_properties:
            return QN_OK
        else:
            return QN_NOT_FIND

    def _hasProperties(self, properties):
        for property in properties:
            if self._hasProperty(property) != QN_OK:
                return QN_NOT_FIND
        return QN_OK

    def _property(self, name):
        return self.m_properties.get(name, "")
