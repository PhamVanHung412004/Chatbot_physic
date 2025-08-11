import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

def test_simple():
    # Đường dẫn đến model
    model_path = "AI_AGENT_TN/Version_2_ft_with_model_qwen3_0.6B/model_LLM_trac_nghiem/fold_0"
    
    print("Đang tải model...")
    
    # Tải tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    
    # Tải base model
    base_model = AutoModelForCausalLM.from_pretrained(
        "Qwen/Qwen3-0.6B",
        torch_dtype=torch.float16,
        device_map="auto",
        trust_remote_code=True
    )
    
    # Tải LoRA adapter
    model = PeftModel.from_pretrained(base_model, model_path)
    model.eval()
    
    print("Model đã được tải thành công!")
    
    # Test câu hỏi đơn giản
    question = "Thủ đô của Việt Nam là gì?"
    options = ["Hà Nội", "Hồ Chí Minh", "Đà Nẵng", "Huế"]
    
    # Format prompt
    formatted_options = ""
    for i, option in enumerate(options):
        formatted_options += f"{chr(65+i)}. {option}\n"
    
    prompt = f"""Câu hỏi: {question}

Các lựa chọn:
{formatted_options.strip()}

Đáp án:"""
    
    print(f"\nPrompt: {prompt}")
    
    # Generate
    inputs = tokenizer(prompt, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_length=256,
            temperature=0.7,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )
    
    # Decode
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"\nGenerated text: {generated_text}")
    
    # Extract answer
    answer_part = generated_text.split("Đáp án:")[-1].strip()
    print(f"\nAnswer: {answer_part}")

if __name__ == "__main__":
    test_simple() 