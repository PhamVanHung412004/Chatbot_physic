"""
Module package chứa các thư viện và dependencies chính.

Module này chứa tất cả các import cần thiết cho hệ thống:
- Thư viện xử lý dữ liệu: numpy, pandas
- Thư viện AI/ML: torch, sentence_transformers, faiss
- Thư viện xử lý file: json, PIL, pathlib
- Thư viện web: streamlit
- Thư viện AI services: groq
- Các utility: ast, uuid, base64, re

Author: Physics Problem Solving System Team
Version: 1.0.0
"""

import os
import re
import numpy 
import pandas
import json
import faiss
import torch
import json
from groq import Groq
import base64

import uuid
from PIL import Image
import io
from sentence_transformers import SentenceTransformer
import ast
from pathlib import Path
from typing import Dict
from numpy.typing import NDArray
import streamlit

