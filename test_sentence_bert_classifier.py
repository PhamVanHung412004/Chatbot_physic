#!/usr/bin/env python3
"""
Test script cho Sentence-BERT + Classifier approach.

Script này kiểm tra:
- Khả năng phân loại câu hỏi vật lý với Sentence-BERT
- Tính chính xác của model
- So sánh với rule-based approach

Author: Physics Problem Solving System Team
Version: 2.0.0
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Flow_splitter_agent.init_model_llm import Check_Flow

def test_sentence_bert_classification():
    """
    Test function để kiểm tra phân loại câu hỏi với Sentence-BERT.
    """
    print("🤖 Bắt đầu test phân loại câu hỏi với Sentence-BERT + Classifier...")
    print("=" * 70)
    
    # Test cases với các loại câu hỏi khác nhau
    test_cases = [
        # THEORY questions
        {
            "question": "Định luật Newton thứ nhất là gì?",
            "expected": "THEORY",
            "description": "Câu hỏi lý thuyết về định luật"
        },
        {
            "question": "Giải thích hiện tượng khúc xạ ánh sáng",
            "expected": "THEORY", 
            "description": "Câu hỏi giải thích hiện tượng"
        },
        {
            "question": "Động năng là gì?",
            "expected": "THEORY",
            "description": "Câu hỏi về khái niệm"
        },
        {
            "question": "Thế năng trọng trường là gì?",
            "expected": "THEORY",
            "description": "Câu hỏi về định nghĩa"
        },
        
        # PRACTICE questions
        {
            "question": "Tính lực tác dụng khi khối lượng m=5kg và gia tốc a=2m/s²",
            "expected": "PRACTICE",
            "description": "Bài tập tính toán với số liệu"
        },
        {
            "question": "Một vật có khối lượng 10kg chuyển động với vận tốc 5m/s. Tính động năng của vật",
            "expected": "PRACTICE",
            "description": "Bài tập tính động năng"
        },
        {
            "question": "Tính công suất khi P=UI với U=220V, I=2A",
            "expected": "PRACTICE",
            "description": "Bài tập tính công suất"
        },
        {
            "question": "Tính vận tốc khi s=100m, t=10s",
            "expected": "PRACTICE",
            "description": "Bài tập tính vận tốc"
        },
        
        # MULTIPLE_CHOICE questions
        {
            "question": "Đơn vị của lực là: A) kg B) m/s C) N D) J",
            "expected": "MULTIPLE_CHOICE",
            "description": "Câu hỏi trắc nghiệm với lựa chọn"
        },
        {
            "question": "Công thức tính động năng là: A) mgh B) 1/2mv² C) Ft D) ma",
            "expected": "MULTIPLE_CHOICE", 
            "description": "Trắc nghiệm về công thức"
        },
        {
            "question": "Đơn vị của công suất là: A) W B) J C) N D) kg",
            "expected": "MULTIPLE_CHOICE",
            "description": "Trắc nghiệm về đơn vị"
        },
        {
            "question": "Định luật Ohm có dạng: A) P=UI B) F=ma C) U=IR D) E=mc²",
            "expected": "MULTIPLE_CHOICE",
            "description": "Trắc nghiệm về định luật"
        }
    ]
    
    correct_predictions = 0
    total_tests = len(test_cases)
    results_by_category = {"THEORY": {"correct": 0, "total": 0}, 
                          "PRACTICE": {"correct": 0, "total": 0}, 
                          "MULTIPLE_CHOICE": {"correct": 0, "total": 0}}
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}/{total_tests}: {test_case['description']}")
        print(f"Câu hỏi: {test_case['question']}")
        print(f"Kết quả mong đợi: {test_case['expected']}")
        
        try:
            # Khởi tạo Check_Flow với câu hỏi
            classifier = Check_Flow(test_case['question'])
            
            # Thực hiện phân loại
            result = classifier.run()
            
            print(f"Kết quả thực tế: {result}")
            
            # Cập nhật thống kê theo category
            expected_cat = test_case['expected']
            results_by_category[expected_cat]["total"] += 1
            
            # Kiểm tra kết quả
            if result == test_case['expected']:
                print("✅ ĐÚNG")
                correct_predictions += 1
                results_by_category[expected_cat]["correct"] += 1
            else:
                print("❌ SAI")
                
        except Exception as e:
            print(f"❌ LỖI: {str(e)}")
            results_by_category[test_case['expected']]["total"] += 1
    
    # Tổng kết
    print("\n" + "=" * 70)
    print("📊 KẾT QUẢ TỔNG KẾT:")
    print(f"Số test đúng: {correct_predictions}/{total_tests}")
    print(f"Độ chính xác tổng thể: {(correct_predictions/total_tests)*100:.1f}%")
    
    # Thống kê theo từng loại
    print("\n📈 THỐNG KÊ THEO LOẠI:")
    for category, stats in results_by_category.items():
        if stats["total"] > 0:
            accuracy = (stats["correct"] / stats["total"]) * 100
            print(f"{category}: {stats['correct']}/{stats['total']} ({accuracy:.1f}%)")
    
    # Đánh giá
    if correct_predictions == total_tests:
        print("\n🎉 HOÀN HẢO! TẤT CẢ TEST CASES ĐỀU PASS!")
    elif correct_predictions >= total_tests * 0.9:
        print("\n🌟 XUẤT SẮC! (>90% accuracy)")
    elif correct_predictions >= total_tests * 0.8:
        print("\n✅ TỐT! (>80% accuracy)")
    elif correct_predictions >= total_tests * 0.7:
        print("\n👍 KHÁ TỐT! (>70% accuracy)")
    else:
        print("\n⚠️ CẦN CẢI THIỆN! (<70% accuracy)")

def test_single_question():
    """
    Test với một câu hỏi đơn lẻ để debug.
    """
    print("\n🔍 Test câu hỏi đơn lẻ:")
    print("-" * 50)
    
    question = input("Nhập câu hỏi cần test: ")
    
    try:
        classifier = Check_Flow(question)
        result = classifier.run()
        
        print(f"Câu hỏi: {question}")
        print(f"Kết quả phân loại: {result}")
        
    except Exception as e:
        print(f"Lỗi: {str(e)}")

def test_edge_cases():
    """
    Test các trường hợp đặc biệt
    """
    print("\n🧪 Test các trường hợp đặc biệt:")
    print("-" * 50)
    
    edge_cases = [
        "Câu hỏi rỗng",
        "",
        "123456789",
        "Câu hỏi không liên quan đến vật lý: Hôm nay thời tiết thế nào?",
        "Câu hỏi dài: " + "Trong một thí nghiệm vật lý, " * 20,
        "Câu hỏi có ký tự đặc biệt: @#$%^&*()",
    ]
    
    for i, case in enumerate(edge_cases, 1):
        print(f"\nEdge case {i}: {case[:50]}...")
        try:
            classifier = Check_Flow(case)
            result = classifier.run()
            print(f"Kết quả: {result}")
        except Exception as e:
            print(f"Lỗi: {str(e)}")

if __name__ == "__main__":
    print("🚀 CHƯƠNG TRÌNH TEST SENTENCE-BERT CLASSIFIER")
    print("=" * 70)
    
    # Chạy test tự động
    test_sentence_bert_classification()
    
    # Test edge cases
    test_edge_cases()
    
    # Tùy chọn test thủ công
    while True:
        choice = input("\nBạn có muốn test câu hỏi riêng lẻ? (y/n): ").lower()
        if choice == 'y':
            test_single_question()
        else:
            break
    
    print("\n👋 Kết thúc chương trình test!")
