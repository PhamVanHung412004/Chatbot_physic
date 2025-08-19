#!/usr/bin/env python3
"""
Test script cho Rule-based Physics Question Classifier.

Script này kiểm tra:
- Khả năng phân loại câu hỏi vật lý bằng rule-based approach
- Tính chính xác của các rules
- Xử lý các trường hợp edge case

Author: Physics Problem Solving System Team
Version: 3.0.0 - Rule-based Approach
"""

def classify_physics_question(question: str) -> str:
    """
    Phân loại câu hỏi vật lý dựa trên rules cải tiến.

    Args:
        question: Câu hỏi cần phân loại

    Returns:
        str: Loại câu hỏi (THEORY, PRACTICE, MULTIPLE_CHOICE)
    """
    if not question or not question.strip():
        return "THEORY"

    question_clean = question.strip()
    question_lower = question_clean.lower()

    # Priority 1: Check for multiple choice (highest priority)
    multiple_choice_patterns = [
        'a)', 'b)', 'c)', 'd)',
        'A)', 'B)', 'C)', 'D)',
        'a.', 'b.', 'c.', 'd.',
        'A.', 'B.', 'C.', 'D.'
    ]
    if any(pattern in question_clean for pattern in multiple_choice_patterns):
        return "MULTIPLE_CHOICE"

    # Priority 2: Check for theory keywords FIRST (before practice)
    theory_keywords = [
        'là gì', 'định nghĩa', 'khái niệm', 'giải thích', 'mô tả', 'nêu', 'trình bày',
        'định luật', 'nguyên lý', 'hiện tượng', 'bản chất', 'đặc điểm', 'tính chất',
        'phân loại', 'so sánh', 'phân biệt', 'ứng dụng', 'vai trò', 'ý nghĩa',
        'tại sao', 'vì sao', 'như thế nào', 'ra sao'
    ]

    # Strong theory indicators - if found, return THEORY immediately
    if any(keyword in question_lower for keyword in theory_keywords):
        return "THEORY"

    # Priority 3: Check for calculation/practice keywords
    # Only strong calculation verbs
    calc_verbs = ['tính', 'tìm', 'xác định', 'tính toán', 'giải', 'suy ra']

    # Units and measurements (more specific)
    units = ['kg', 'm/s', 'm/s²', 'newton', 'joule', 'watt', 'volt', 'ampere', 'ohm',
             'n', 'j', 'w', 'v', 'a', 'ω', 'pa', 'hz']

    # Mathematical symbols and expressions
    math_symbols = ['=', '+', '-', '×', '÷', '²', '³', '√']

    # Strong calculation context
    calc_context = ['với', 'khi', 'rơi', 'ném', 'dao động', 'va chạm']

    # Numerical patterns
    import re
    has_numbers_with_units = bool(re.search(r'\d+\s*(kg|m/s|m/s²|n|j|w|v|a)', question_lower))
    has_formula = bool(re.search(r'[a-zA-Z]\s*=\s*[a-zA-Z]', question_clean))
    has_calculation = bool(re.search(r'\d+\s*[+\-×÷]\s*\d+', question_clean))

    # Check for practice indicators with stricter rules
    practice_score = 0

    # Very strong indicators (worth 3 points each)
    if any(verb in question_lower for verb in calc_verbs):
        practice_score += 3
    if has_formula:
        practice_score += 3
    if has_numbers_with_units:
        practice_score += 3
    if has_calculation:
        practice_score += 3

    # Medium indicators (worth 1 point each)
    if any(unit in question_lower for unit in units):
        practice_score += 1
    if any(symbol in question_clean for symbol in math_symbols):
        practice_score += 1
    if any(context in question_lower for context in calc_context):
        practice_score += 1

    # Only classify as PRACTICE if score >= 3 (stricter threshold)
    if practice_score >= 3:
        return "PRACTICE"

    # Default: if no clear indicators, classify as THEORY
    return "THEORY"

def test_rule_based_classification():
    """
    Test function để kiểm tra phân loại câu hỏi với rule-based approach.
    """
    print("📏 Bắt đầu test phân loại câu hỏi với Rule-based Classifier...")
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
        {
            "question": "Định luật bảo toàn năng lượng nói gì?",
            "expected": "THEORY",
            "description": "Câu hỏi về định luật"
        },
        {
            "question": "Lực ma sát là gì?",
            "expected": "THEORY",
            "description": "Câu hỏi định nghĩa với 'là gì'"
        },
        {
            "question": "Tại sao vật rơi tự do có gia tốc không đổi?",
            "expected": "THEORY",
            "description": "Câu hỏi giải thích với 'tại sao'"
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
        {
            "question": "Tìm gia tốc khi v=20m/s, t=5s",
            "expected": "PRACTICE",
            "description": "Bài tập tìm gia tốc"
        },
        {
            "question": "Một vật có khối lượng 2kg rơi từ độ cao 10m",
            "expected": "PRACTICE",
            "description": "Bài tập có từ khóa 'có'"
        },
        {
            "question": "Xác định vận tốc của vật khi t = 5s",
            "expected": "PRACTICE",
            "description": "Bài tập với 'xác định'"
        },
        {
            "question": "Giải bài toán: F = ma với m = 10kg",
            "expected": "PRACTICE",
            "description": "Bài tập với 'giải' và công thức"
        },
        {
            "question": "Tính toán công suất tiêu thụ P = UI",
            "expected": "PRACTICE",
            "description": "Bài tập với 'tính toán'"
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
        },
        {
            "question": "Vận tốc ánh sáng trong chân không: a) 3×10⁸ m/s b) 340 m/s c) 9.8 m/s² d) 1.6×10⁻¹⁹ C",
            "expected": "MULTIPLE_CHOICE",
            "description": "Trắc nghiệm với a) b) c) d)"
        },

        # Trường hợp khó phân biệt
        {
            "question": "Tính lực F trong công thức F=ma: A) 10N B) 20N C) 30N D) 40N",
            "expected": "MULTIPLE_CHOICE",
            "description": "Có cả 'tính' và lựa chọn - ưu tiên MULTIPLE_CHOICE"
        },
        {
            "question": "Một vật khối lượng 5kg. Động năng là gì?",
            "expected": "THEORY",
            "description": "Có số liệu nhưng hỏi định nghĩa - ưu tiên THEORY"
        },
        {
            "question": "Trong công thức E=mc², c là gì?",
            "expected": "THEORY",
            "description": "Có công thức nhưng hỏi ý nghĩa - ưu tiên THEORY"
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
            # Thực hiện phân loại
            result = classify_physics_question(test_case['question'])

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

def test_edge_cases():
    """
    Test các trường hợp đặc biệt
    """
    print("\n🧪 Test các trường hợp đặc biệt:")
    print("-" * 50)

    edge_cases = [
        ("Câu hỏi rỗng", ""),
        ("Chỉ có số", "123456789"),
        ("Không liên quan vật lý", "Hôm nay thời tiết thế nào?"),
        ("Có ký tự đặc biệt", "Câu hỏi có @#$%^&*()"),
        ("Trắc nghiệm viết hoa", "ĐƠN VỊ CỦA LỰC LÀ: A) KG B) N C) M D) S"),
        ("Có cả từ khóa tính và A)", "Tính lực: A) 10N B) 20N C) 30N D) 40N"),
        ("Câu dài", "Trong một thí nghiệm vật lý phức tạp, chúng ta cần tính toán nhiều đại lượng khác nhau"),
    ]

    for i, (description, case) in enumerate(edge_cases, 1):
        print(f"\nEdge case {i}: {description}")
        print(f"Input: {case[:50]}{'...' if len(case) > 50 else ''}")
        try:
            result = classify_physics_question(case)
            print(f"Kết quả: {result}")
        except Exception as e:
            print(f"Lỗi: {str(e)}")

def test_single_question():
    """
    Test với một câu hỏi đơn lẻ để debug.
    """
    print("\n🔍 Test câu hỏi đơn lẻ:")
    print("-" * 50)

    question = input("Nhập câu hỏi cần test: ")

    try:
        result = classify_physics_question(question)

        print(f"Câu hỏi: {question}")
        print(f"Kết quả phân loại: {result}")

        # Hiển thị lý do phân loại
        question_lower = question.lower()
        if any(choice in question for choice in ['a)', 'b)', 'c)', 'd)', 'A)', 'B)', 'C)', 'D)']):
            print("Lý do: Phát hiện lựa chọn A), B), C), D)")
        elif any(keyword in question_lower for keyword in ['tính', 'tìm', 'kg', 'm/s', 'newton', 'joule', '=', 'với', 'khi', 'có', 'chuyển động']):
            print("Lý do: Phát hiện từ khóa tính toán")
        else:
            print("Lý do: Mặc định là THEORY")

    except Exception as e:
        print(f"Lỗi: {str(e)}")

if __name__ == "__main__":
    print("🚀 CHƯƠNG TRÌNH TEST RULE-BASED PHYSICS CLASSIFIER")
    print("=" * 70)

    # Chạy test tự động
    test_rule_based_classification()

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