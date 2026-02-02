#!/usr/bin/env python3
# bsa_suite.py —— BSA-seq 一体化入口（统一参数 → 调用 8 个算法脚本）

import argparse
import os
import subprocess
import sys
from pathlib import Path
from textwrap import dedent
