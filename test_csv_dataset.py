#!/usr/bin/env python3
"""
Test script cho Rule-based Physics Classifier với dataset CSV thực tế.

Script này kiểm tra:
- Khả năng phân loại câu hỏi vật lý từ file CSV
- Tính chính xác trên dataset lớn
- Phân tích chi tiết theo từng loại

Author: Physics Problem Solving System Team
Version: 4.0.0 - CSV Dataset Testing
"""

import pandas as pd
import re
from typing import Dict, List, Tuple

def classify_physics_question(question: str) -> str:
    """
    Phân loại câu hỏi vật lý dựa trên rules cải tiến để đạt 100% accuracy.

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
    # Use more specific patterns to avoid false positives with °C, °F, etc.
    multiple_choice_patterns = [
        ' a)', ' b)', ' c)', ' d)',
        ' A)', ' B)', ' C)', ' D)',
        'a) ', 'b) ', 'c) ', 'd) ',
        'A) ', 'B) ', 'C) ', 'D) '
    ]

    # Check for multiple choice with proper context (space before or after)
    has_multiple_choice = False
    for pattern in multiple_choice_patterns:
        if pattern in question_clean:
            has_multiple_choice = True
            break

    # Additional check for patterns at start of options
    if not has_multiple_choice:
        # Look for patterns like ": A)" or "A)" at beginning of options
        mc_regex = r'[:\s][ABCD]\)\s'
        if re.search(mc_regex, question_clean):
            has_multiple_choice = True

    if has_multiple_choice:
        return "MULTIPLE_CHOICE"

    # Priority 2: Check for theory keywords FIRST (before practice)
    theory_keywords = [
        'là gì', 'định nghĩa', 'khái niệm', 'giải thích', 'mô tả', 'nêu', 'trình bày',
        'định luật', 'nguyên lý', 'hiện tượng', 'bản chất', 'đặc điểm',
        'phân loại', 'so sánh', 'phân biệt', 'ứng dụng', 'vai trò', 'ý nghĩa',
        'tại sao', 'vì sao', 'như thế nào', 'ra sao', 'phân tích', 'mô tả cơ chế',
        'hoạt động của', 'nguyên lý hoạt động', 'cơ chế hoạt động', 'hãy giải thích'
    ]

    # Check for theory keywords but exclude cases where it's part of calculation context
    has_theory_keywords = False
    for keyword in theory_keywords:
        if keyword in question_lower:
            # Special handling for "tính chất" - check if it's in calculation context
            if keyword == 'tính chất':
                # If "tính" appears before "tính chất", it's likely a calculation question
                if 'tính' in question_lower and question_lower.find('tính') < question_lower.find('tính chất'):
                    continue  # Skip this theory keyword
            has_theory_keywords = True
            break

    # Strong theory indicators - if found, return THEORY immediately
    if has_theory_keywords:
        return "THEORY"

    # Priority 3: Enhanced calculation/practice detection
    # Strong calculation verbs
    calc_verbs = ['tính', 'tìm', 'xác định', 'tính toán', 'giải', 'suy ra', 'hỏi']

    # Enhanced units and measurements
    units = [
        # Basic units
        'kg', 'm/s', 'm/s²', 'newton', 'joule', 'watt', 'volt', 'ampere', 'ohm',
        'n', 'j', 'w', 'v', 'a', 'ω', 'pa', 'hz', 'tesla', 'weber', 'henry', 'farad',
        # Length units
        'cm', 'mm', 'km', 'm', 'nm',
        # Temperature units
        '°c', 'k', 'kelvin',
        # Pressure units
        'atm', 'pascal',
        # Volume units
        'lít', 'l', 'ml',
        # Energy units
        'ev', 'cal', 'kcal',
        # Time units
        's', 'ms', 'min', 'h',
        # Angle units
        'rad/s', 'rad', '°', 'độ'
    ]

    # Mathematical symbols and expressions
    math_symbols = ['=', '+', '-', '×', '÷', '²', '³', '√', 'π', 'α', 'β', 'γ', 'λ', 'μ', 'ρ', 'σ', 'ω']

    # Enhanced calculation context
    calc_context = [
        'với', 'khi', 'rơi', 'ném', 'dao động', 'va chạm', 'quay', 'chuyển động',
        'khối lượng', 'vận tốc', 'gia tốc', 'lực', 'công', 'công suất', 'năng lượng',
        'nhiệt lượng', 'nhiệt độ', 'áp suất', 'thể tích', 'điện áp', 'dòng điện',
        'điện trở', 'từ trường', 'điện trường', 'tần số', 'chu kì', 'bước sóng',
        'chiều dài', 'bán kính', 'đường kính', 'diện tích', 'thời gian', 'khoảng cách',
        'độ cao', 'góc', 'biên độ', 'pha', 'hiệu điện thế', 'cường độ', 'suất điện động',
        'từ thông', 'điện dung', 'độ cứng', 'hệ số', 'chiết suất', 'tiêu cự',
        'độ phóng đại', 'cảm ứng từ', 'năng lượng liên kết', 'khối lượng nghỉ',
        'động lượng', 'xung lượng', 'momen', 'entropy', 'hiệu suất'
    ]

    # Enhanced numerical patterns
    has_numbers_with_units = bool(re.search(r'\d+\s*[a-zA-Zα-ωΩ°]+', question_clean))
    has_formula = bool(re.search(r'[a-zA-Zα-ωΩ]\s*=\s*[a-zA-Zα-ωΩ]', question_clean))
    has_calculation = bool(re.search(r'\d+\s*[+\-×÷]\s*\d+', question_clean))
    has_scientific_notation = bool(re.search(r'\d+\.?\d*\s*×?\s*10[⁻¹²³⁴⁵⁶⁷⁸⁹⁰]*', question_clean))
    has_temperature = bool(re.search(r'\d+\s*°[CF]?', question_clean))
    has_percentage = bool(re.search(r'\d+\s*%', question_clean))
    has_decimal_numbers = bool(re.search(r'\d+\.\d+', question_clean))

    # Check for practice indicators with enhanced scoring
    practice_score = 0

    # Very strong indicators (worth 4 points each)
    if any(verb in question_lower for verb in calc_verbs):
        practice_score += 4
    if has_formula:
        practice_score += 4
    if has_scientific_notation:
        practice_score += 4
    if has_calculation:
        practice_score += 4

    # Strong indicators (worth 2 points each)
    if has_numbers_with_units:
        practice_score += 2
    if has_temperature:
        practice_score += 2
    if has_percentage:
        practice_score += 2
    if has_decimal_numbers:
        practice_score += 2

    # Medium indicators (worth 1 point each)
    if any(unit in question_lower for unit in units):
        practice_score += 1
    if any(symbol in question_clean for symbol in math_symbols):
        practice_score += 1
    if any(context in question_lower for context in calc_context):
        practice_score += 1

    # Enhanced threshold - classify as PRACTICE if score >= 3
    if practice_score >= 3:
        return "PRACTICE"

    # Default: if no clear indicators, classify as THEORY
    return "THEORY"

def map_csv_type_to_our_type(csv_type: str) -> str:
    """
    Map loại câu hỏi từ CSV sang format của chúng ta.
    """
    csv_type_lower = csv_type.lower().strip()
    
    if csv_type_lower == 'trắc nghiệm':
        return 'MULTIPLE_CHOICE'
    elif csv_type_lower == 'bài tập':
        return 'PRACTICE'
    elif csv_type_lower == 'lý thuyết':
        return 'THEORY'
    else:
        return 'UNKNOWN'

def test_csv_dataset():
    """
    Test function với dataset CSV thực tế.
    """
    print("📊 Bắt đầu test với dataset CSV physics_questions_dataset.csv...")
    print("=" * 80)
    
    try:
        # Đọc file CSV
        df = pd.read_csv('physics_questions_dataset.csv')
        print(f"✅ Đã đọc {len(df)} câu hỏi từ file CSV")
        
        # Thống kê dataset
        print(f"\n📈 THỐNG KÊ DATASET:")
        type_counts = df['type'].value_counts()
        for type_name, count in type_counts.items():
            print(f"{type_name}: {count} câu ({count/len(df)*100:.1f}%)")
        
        # Test trên toàn bộ dataset
        correct_predictions = 0
        total_tests = len(df)
        results_by_category = {
            "THEORY": {"correct": 0, "total": 0, "wrong_predictions": []},
            "PRACTICE": {"correct": 0, "total": 0, "wrong_predictions": []}, 
            "MULTIPLE_CHOICE": {"correct": 0, "total": 0, "wrong_predictions": []}
        }
        
        print(f"\n🔄 Đang test {total_tests} câu hỏi...")
        
        for index, row in df.iterrows():
            question = row['question']
            csv_type = row['type']
            expected_type = map_csv_type_to_our_type(csv_type)
            
            if expected_type == 'UNKNOWN':
                continue
                
            # Thực hiện phân loại
            predicted_type = classify_physics_question(question)
            
            # Cập nhật thống kê
            results_by_category[expected_type]["total"] += 1
            
            if predicted_type == expected_type:
                correct_predictions += 1
                results_by_category[expected_type]["correct"] += 1
            else:
                # Lưu lại các dự đoán sai để phân tích
                results_by_category[expected_type]["wrong_predictions"].append({
                    "question": question[:100] + "..." if len(question) > 100 else question,
                    "expected": expected_type,
                    "predicted": predicted_type
                })
        
        # Tổng kết
        print("\n" + "=" * 80)
        print("📊 KẾT QUẢ TỔNG KẾT:")
        print(f"Số test đúng: {correct_predictions}/{total_tests}")
        print(f"Độ chính xác tổng thể: {(correct_predictions/total_tests)*100:.1f}%")
        
        # Thống kê chi tiết theo từng loại
        print("\n📈 THỐNG KÊ CHI TIẾT THEO LOẠI:")
        for category, stats in results_by_category.items():
            if stats["total"] > 0:
                accuracy = (stats["correct"] / stats["total"]) * 100
                print(f"{category}: {stats['correct']}/{stats['total']} ({accuracy:.1f}%)")
        
        # Phân tích lỗi
        print("\n🔍 PHÂN TÍCH LỖI (Top 5 mỗi loại):")
        for category, stats in results_by_category.items():
            if stats["wrong_predictions"]:
                print(f"\n❌ {category} - Dự đoán sai:")
                for i, error in enumerate(stats["wrong_predictions"][:5], 1):
                    print(f"  {i}. {error['question']}")
                    print(f"     Expected: {error['expected']}, Got: {error['predicted']}")
                
                if len(stats["wrong_predictions"]) > 5:
                    print(f"     ... và {len(stats['wrong_predictions']) - 5} lỗi khác")
        
        # Đánh giá tổng thể
        overall_accuracy = (correct_predictions/total_tests)*100
        if overall_accuracy >= 90:
            print("\n🌟 XUẤT SẮC! (≥90% accuracy)")
        elif overall_accuracy >= 80:
            print("\n✅ TỐT! (≥80% accuracy)")
        elif overall_accuracy >= 70:
            print("\n👍 KHÁ TỐT! (≥70% accuracy)")
        elif overall_accuracy >= 60:
            print("\n⚠️ CHẤP NHẬN ĐƯỢC! (≥60% accuracy)")
        else:
            print("\n❌ CẦN CẢI THIỆN! (<60% accuracy)")
            
    except FileNotFoundError:
        print("❌ Không tìm thấy file physics_questions_dataset.csv")
    except Exception as e:
        print(f"❌ Lỗi khi đọc file: {str(e)}")

def test_sample_questions():
    """
    Test với một số câu hỏi mẫu từ dataset.
    """
    print("\n🔍 TEST MỘT SỐ CÂU HỎI MẪU:")
    print("-" * 60)
    
    try:
        df = pd.read_csv('physics_questions_dataset.csv')
        
        # Lấy mẫu từ mỗi loại
        sample_questions = []
        
        for question_type in ['trắc nghiệm', 'bài tập', 'lý thuyết']:
            type_questions = df[df['type'] == question_type].head(3)
            for _, row in type_questions.iterrows():
                sample_questions.append({
                    'question': row['question'],
                    'expected': map_csv_type_to_our_type(row['type']),
                    'csv_type': row['type']
                })
        
        for i, sample in enumerate(sample_questions, 1):
            print(f"\n📝 Mẫu {i} ({sample['csv_type']}):")
            question = sample['question']
            if len(question) > 150:
                question = question[:150] + "..."
            print(f"Câu hỏi: {question}")
            print(f"Expected: {sample['expected']}")
            
            result = classify_physics_question(sample['question'])
            print(f"Predicted: {result}")
            
            if result == sample['expected']:
                print("✅ ĐÚNG")
            else:
                print("❌ SAI")
                
    except Exception as e:
        print(f"❌ Lỗi: {str(e)}")

if __name__ == "__main__":
    print("🚀 CHƯƠNG TRÌNH TEST RULE-BASED CLASSIFIER VỚI DATASET CSV")
    print("=" * 80)
    
    # Test với toàn bộ dataset
    test_csv_dataset()
    
    # Test với một số câu hỏi mẫu
    test_sample_questions()
    
    print("\n👋 Kết thúc chương trình test!")
