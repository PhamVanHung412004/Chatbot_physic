"""
Module tạo câu trả lời từ context và câu hỏi sử dụng Google Gemini.
Module này chịu trách nhiệm:
- Khởi tạo model Google Gemini
- Đọc cấu hình prompt từ file YAML
- Tạo câu trả lời dựa trên câu hỏi và context
- Xử lý prompt và response từ model

Author: Physics Problem Solving System Team
Version: 1.0.0
"""
import google.generativeai as genai
from typing import List, Dict, Optional
from pathlib import Path
import yaml
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure API key
api_key = os.getenv('GOOGLE_API_KEY')
if not api_key:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

genai.configure(api_key=api_key)

# Initialize model với các cấu hình phù hợp
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

# Khởi tạo model
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash",  # Sử dụng tên model chính xác
    generation_config=generation_config,
    safety_settings=safety_settings
)

# Load configuration
path_config_prompt_system = Path(__file__).parent.parent.parent.parent / "config_prompt_system.yaml"

try:
    with open(path_config_prompt_system, "r", encoding="utf-8") as file:
        information_prompt: Dict[str, str] = yaml.safe_load(file)
    system: str = information_prompt.get("system_model_llm_theory", "")
except FileNotFoundError:
    print(f"Warning: Config file not found at {path_config_prompt_system}")
    system = "Bạn là một trợ lý AI thông minh, hãy trả lời câu hỏi dựa trên context được cung cấp."
except Exception as e:
    print(f"Error loading config: {e}")
    system = "Bạn là một trợ lý AI thông minh, hãy trả lời câu hỏi dựa trên context được cung cấp."


class AnswerQuestionFromDocuments:
    """
    Class tạo câu trả lời từ câu hỏi và context sử dụng Google Gemini.
    
    Class này chịu trách nhiệm:
    - Nhận câu hỏi và context
    - Tạo prompt phù hợp với system prompt
    - Gọi model Gemini để tạo câu trả lời
    - Trả về câu trả lời được format
    """
    
    def __init__(self, question: str, context: str) -> None:
        """
        Khởi tạo AnswerQuestionFromDocuments với câu hỏi và context.
        
        Args:
            question: Câu hỏi của người dùng
            context: Context liên quan từ vector database
        """
        self.question: str = question
        self.context: str = context
        self.model = model  # Store model instance
        
    def run(self) -> str:
        """
        Tạo câu trả lời từ câu hỏi và context.
        
        Tạo prompt kết hợp system prompt, câu hỏi và context,
        sau đó gọi model Gemini để tạo câu trả lời.
        
        Returns:
            String chứa câu trả lời từ model
            
        Raises:
            Exception: Khi có lỗi trong quá trình generate content
        """
        prompt = f"""{system}

Câu hỏi: {self.question}

Nội dung trả lời của câu hỏi:
{self.context}

Trả lời:"""
        
        try:
            # Generate content với error handling
            response = self.model.generate_content(prompt)
            
            # Kiểm tra response
            if response.text:
                return response.text
            else:
                return "Xin lỗi, tôi không thể tạo câu trả lời cho câu hỏi này."
                
        except Exception as e:
            print(f"Error generating response: {e}")
            return f"Đã xảy ra lỗi khi tạo câu trả lời: {str(e)}"
    
    def run_with_streaming(self) -> str:
        """
        Tạo câu trả lời với streaming mode.
        
        Returns:
            String chứa toàn bộ câu trả lời
        """
        prompt = f"""{system}

Câu hỏi: {self.question}

Nội dung trả lời của câu hỏi:
{self.context}

Trả lời:"""
        
        try:
            # Generate với streaming
            response = self.model.generate_content(prompt, stream=True)
            
            full_response = ""
            for chunk in response:
                if chunk.text:
                    full_response += chunk.text
                    # Có thể yield từng chunk nếu cần
                    
            return full_response if full_response else "Không thể tạo câu trả lời."
            
        except Exception as e:
            print(f"Error in streaming response: {e}")
            return f"Đã xảy ra lỗi: {str(e)}"
    
    def get_token_count(self) -> int:
        """
        Đếm số token trong prompt.
        
        Returns:
            Số lượng token
        """
        prompt = f"""{system}

Câu hỏi: {self.question}

Nội dung trả lời của câu hỏi:
{self.context}

Trả lời:"""
        
        try:
            return self.model.count_tokens(prompt).total_tokens
        except Exception as e:
            print(f"Error counting tokens: {e}")
            return 0
