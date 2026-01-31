#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动Web界面
"""

import os
import sys
from web_interface.app import app

if __name__ == '__main__':
    print("启动公租房信息展示系统...")
    print("访问 http://localhost:5000 查看房源信息")
    app.run(host='0.0.0.0', port=5000, debug=False)