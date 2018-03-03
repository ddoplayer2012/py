# -*- encoding:utf-8 -*-
# Author: Koctr

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)
from core import main

main.run()
