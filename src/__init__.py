"""
Module chính của hệ thống giải quyết bài tập vật lý.

Module này chứa các thành phần chính của hệ thống AI giải quyết
bài tập vật lý, bao gồm:
- Agent_theory: Module xử lý lý thuyết và RAG
- router_theory: Module định tuyến câu hỏi
- Flow_splitter_agent: Module phân loại câu hỏi (đang phát triển)
- Multi_agent: Module đa agent (đang phát triển)

Author: Physics Problem Solving System Team
Version: 1.0.0
"""

# from .Flow_splitter_agent import *
from .router_theory import *
from .router_multiple_choice import *