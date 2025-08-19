from src import PhysicsMultipleChoieAgent
import json

def main():
    # Đường dẫn đến model đã fine-tune
    model_path = "/home/phamvanhung/system/Desktop/Project_ca_nhan/Building_a_physics_problem_solving_system/src/Multi_agent/AI_AGENT_TN/Version_2_ft_with_model_qwen3_0.6B/model_LLM_trac_nghiem/fold_4"
    
    # Khởi tạo agent
    agent = PhysicsMultipleChoiceAgent(model_path)
    
    # Test cases - Câu hỏi trắc nghiệm vật lý
    test_questions = [
        {
            "question": "Một vật chuyển động thẳng đều với vận tốc 10 m/s. Quãng đường vật đi được trong 5 giây là bao nhiêu?",
            "options": ["5 m", "10 m", "50 m", "25 m"],
            "correct_answer": "C"
        },
        {
            "question": "Lực hấp dẫn giữa hai vật tỉ lệ thuận với:",
            "options": ["Tích khối lượng hai vật", "Tổng khối lượng hai vật", "Hiệu khối lượng hai vật", "Thương khối lượng hai vật"],
            "correct_answer": "A"
        },
        {
            "question": "Đơn vị của công cơ học là:",
            "options": ["Niu-tơn (N)", "Jun (J)", "Oát (W)", "Pascal (Pa)"],
            "correct_answer": "B"
        },
        {
            "question": "Một vật có khối lượng 2 kg được ném thẳng đứng lên trên với vận tốc ban đầu 20 m/s. Gia tốc trọng trường g = 10 m/s². Độ cao cực đại vật đạt được là:",
            "options": ["10 m", "20 m", "40 m", "80 m"],
            "correct_answer": "B"
        },
        {
            "question": "Hiện tượng nào sau đây là hiện tượng phản xạ ánh sáng?",
            "options": ["Nhìn thấy ảnh trong gương", "Cầu vồng xuất hiện sau mưa", "Bóng đen xuất hiện khi che ánh sáng", "Ánh sáng đi qua lăng kính"],
            "correct_answer": "A"
        },
        {
            "question": "Một dòng điện có cường độ 2A chạy qua một điện trở 10Ω trong thời gian 5 giây. Nhiệt lượng tỏa ra trên điện trở là:",
            "options": ["20 J", "100 J", "200 J", "400 J"],
            "correct_answer": "C"
        },
        {
            "question": "Chu kỳ dao động của con lắc đơn phụ thuộc vào:",
            "options": ["Khối lượng của vật nặng", "Chiều dài dây treo", "Biên độ dao động", "Tất cả các yếu tố trên"],
            "correct_answer": "B"
        },
        {
            "question": "Một vật dao động điều hòa với tần số 2 Hz. Chu kỳ dao động của vật là:",
            "options": ["0.5 s", "1 s", "2 s", "4 s"],
            "correct_answer": "A"
        },
        {
            "question": "Khi một vật chuyển động tròn đều, lực hướng tâm có đặc điểm:",
            "options": ["Luôn hướng vào tâm quỹ đạo", "Luôn hướng ra ngoài tâm quỹ đạo", "Luôn vuông góc với vận tốc", "Luôn cùng hướng với vận tốc"],
            "correct_answer": "A"
        },
        {
            "question": "Một vật có khối lượng 1 kg được thả rơi tự do từ độ cao 20 m. Vận tốc của vật khi chạm đất là (g = 10 m/s²):",
            "options": ["10 m/s", "20 m/s", "30 m/s", "40 m/s"],
            "correct_answer": "B"
        }
    ]
    
    # Chạy test
    results, accuracy = agent.batch_test(test_questions, verbose=True)
    
    # Lưu kết quả
    with open("physics_test_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "accuracy": accuracy,
            "total_questions": len(test_questions),
            "results": results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\nKết quả đã được lưu vào file 'physics_test_results.json'")

if __name__ == "__main__":
    main()