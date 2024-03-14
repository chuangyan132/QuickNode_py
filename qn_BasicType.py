#!
# @brief   
# @project qn_pluginExe
# @file    qn_BasicType.py
# @author  Chuang Yan
# @email   Yanchuang1122@gmail.com  
# @license 
#     Copyright(C) Shining3D  
# @versions 
#     V0.1-ChuangYan 11/03/2024 13:01  
#

from typing import Any, Dict, Union

# For the sake of example, importing typing for potential type hints
from typing import Any, Dict, Union

# Basic type representations and constants in Python
QN_BOOL = bool
QN_TRUE = True
QN_FALSE = False

# Integer types can simply use Python's built-in int, but for clarity in translation:
QN_INT8 = int
QN_UINT8 = int
QN_BYTE = int
QN_INT16 = int
QN_UINT16 = int
QN_INT32 = int
QN_UINT32 = int
QN_INT64 = int
QN_UINT64 = int

# Character and string types
QN_CHAR = str
QN_WCHAR = str  # Python does not differentiate between wide and narrow characters
QN_STR = str
QN_CSTR = str
QN_WSTR = str
QN_CWSTR = str

# Floating-point types
QN_FLOAT = float
QN_DOUBLE = float
QN_LONGDOUBLE = float

# Time value, represented as integer in Python
QN_TIME_VALUE = int
QN_MAX_TIME_VALUE = 32535215999000000  # or 2147483647000000 depending on context

# Pointer and binary types, broadly represented as Any, since Python does not have direct equivalents
QN_LPVOID = Any
QN_HANDLE = Any
QN_BINARY = bytes
QN_BLOB = bytes

# Pointer operator types
QN_INTPTR_T = int
QN_UINTPTR_T = int
QN_PTRDIFF_T = int

# Result type, represented as int in Python for status codes
QN_RESULT = int
