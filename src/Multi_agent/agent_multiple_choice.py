import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import json
import time
import os

class PhysicsMultipleChoiceAgent:
    def __init__(self, model_path, device="cuda" if torch.cuda.is_available() else "cpu"):
        """
        Khởi tạo agent cho bài toán trắc nghiệm vật lý
        
        Args:
            model_path: Đường dẫn đến model đã fine-tune
            device: Thiết bị chạy model (cuda/cpu)
        """
        self.device = device
        self.model_path = model_path
        
        print(f"Đang tải model từ: {model_path}")
        print(f"Sử dụng thiết bị: {device}")
        
        # Tải tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        # Tải base model
        self.base_model = AutoModelForCausalLM.from_pretrained(
            "Qwen/Qwen3-0.6B",
            torch_dtype=torch.float16 if device == "cuda" else torch.float32,
            device_map="auto" if device == "cuda" else None,
            trust_remote_code=True
        )
        
        # Sửa cấu hình LoRA để tương thích
        self._fix_lora_config()
        
        # Tải LoRA adapter
        self.model = PeftModel.from_pretrained(self.base_model, model_path)
        
        # Đặt model ở chế độ evaluation
        self.model.eval()
        
        print("Model đã được tải thành công!")
    
    def _fix_lora_config(self):
        """Sửa cấu hình LoRA để tương thích với phiên bản PEFT hiện tại"""
        config_path = os.path.join(self.model_path, "adapter_config.json")
        if os.path.exists(config_path):
            import json
            with open(config_path, 'r') as f:
                config = json.load(f)
            
            # Loại bỏ các tham số không tương thích
            incompatible_keys = ['corda_config', 'eva_config', 'megatron_config', 'megatron_core']
            for key in incompatible_keys:
                if key in config:
                    del config[key]
            
            # Lưu lại cấu hình đã sửa
            with open(config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            print("Đã sửa cấu hình LoRA để tương thích")
    
    def format_physics_question(self, question, options, correct_answer=None):
        """
        Format câu hỏi trắc nghiệm vật lý theo template của model
        
        Args:
            question: Câu hỏi vật lý
            options: Danh sách các lựa chọn
            correct_answer: Đáp án đúng (nếu có)
        """
        formatted_options = ""
        for i, option in enumerate(options):
            formatted_options += f"{chr(65+i)}. {option}\n"
        
        prompt = f"""Câu hỏi vật lý: {question}

Các lựa chọn:
{formatted_options.strip()}

Đáp án:"""
        
        return prompt
    
    def generate_answer(self, question, options, max_length=512, temperature=0.7, top_p=0.9):
        """
        Sinh đáp án cho câu hỏi trắc nghiệm vật lý
        
        Args:
            question: Câu hỏi vật lý
            options: Danh sách các lựa chọn
            max_length: Độ dài tối đa của output
            temperature: Nhiệt độ sampling
            top_p: Top-p sampling
        """
        prompt = self.format_physics_question(question, options)
        
        # Tokenize input
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        
        # Generate
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id
            )
        
        # Decode output
        generated_text = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Lấy phần đáp án (sau "Đáp án:")
        answer_part = generated_text.split("Đáp án:")[-1].strip()
        
        return answer_part, generated_text
    
    def batch_test(self, test_questions, verbose=True):
        """
        Test model với nhiều câu hỏi vật lý
        
        Args:
            test_questions: List các dict chứa question, options, correct_answer
            verbose: In kết quả chi tiết
        """
        results = []
        correct_count = 0
        
        for i, test_case in enumerate(test_questions):
            if verbose:
                print(f"\n{'='*60}")
                print(f"Câu hỏi vật lý {i+1}:")
                print(f"{'='*60}")
            
            question = test_case['question']
            options = test_case['options']
            correct_answer = test_case.get('correct_answer', None)
            
            # Generate answer
            start_time = time.time()
            answer, full_response = self.generate_answer(question, options)
            end_time = time.time()
            
            # Extract predicted answer (A, B, C, D)
            predicted_answer = None
            for char in answer.upper():
                if char in ['A', 'B', 'C', 'D']:
                    predicted_answer = char
                    break
            
            # Check if correct
            is_correct = False
            if correct_answer and predicted_answer:
                is_correct = predicted_answer == correct_answer.upper()
                if is_correct:
                    correct_count += 1
            
            result = {
                'question': question,
                'options': options,
                'correct_answer': correct_answer,
                'predicted_answer': predicted_answer,
                'full_response': full_response,
                'is_correct': is_correct,
                'time_taken': end_time - start_time
            }
            
            results.append(result)
            
            if verbose:
                print(f"Câu hỏi: {question}")
                print(f"Lựa chọn: {options}")
                print(f"Đáp án đúng: {correct_answer}")
                print(f"Đáp án dự đoán: {predicted_answer}")
                print(f"Kết quả: {'✅ ĐÚNG' if is_correct else '❌ SAI'}")
                print(f"Thời gian: {end_time - start_time:.2f}s")
                print(f"Phản hồi đầy đủ:\n{full_response}")
        
        # Calculate accuracy
        accuracy = correct_count / len(test_questions) if test_questions else 0
        
        if verbose:
            print(f"\n{'='*60}")
            print(f"KẾT QUẢ TỔNG KẾT")
            print(f"{'='*60}")
            print(f"Tổng số câu hỏi: {len(test_questions)}")
            print(f"Số câu đúng: {correct_count}")
            print(f"Độ chính xác: {accuracy:.2%}")
        
        return results, accuracy

