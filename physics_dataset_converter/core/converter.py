#!/usr/bin/env python3
"""
Improved Dataset Converter for Physics Files
============================================

This script provides better separation of questions and answers from physics dataset files.
It creates a CSV format similar to the existing dataset.csv structure with improved parsing.

Author: AI Assistant
"""

import os
import json
import re
import docx
import pandas as pd
from typing import Dict, List, Tuple, Any
from pathlib import Path


class ImprovedDatasetConverter:
    """Improved converter with better question-answer separation."""
    
    def __init__(self, dataset_folder: str = "dataset_teacher"):
        """Initialize the converter."""
        self.dataset_folder = Path(dataset_folder)
        self.questions_and_answers = []
        
        # Enhanced patterns for better question detection
        self.question_start_patterns = [
            r'^Câu\s+\d+[:\.]',  # "Câu 1:", "Câu 2.", etc.
            r'^Câu\s+hỏi',       # "Câu hỏi"
            r'^Hoạt\s+động',     # "Hoạt động"
            r'^Bài\s+tập',       # "Bài tập"
            r'^Bài\s+\d+',       # "Bài 1", "Bài 2", etc.
        ]
        
        # Patterns for question content
        self.question_content_patterns = [
            r'Hãy\s+',           # "Hãy ..."
            r'Tính\s+',          # "Tính ..."
            r'Xác\s+định',       # "Xác định ..."
            r'Tìm\s+',           # "Tìm ..."
            r'Chứng\s+minh',     # "Chứng minh ..."
            r'Giải\s+thích',     # "Giải thích ..."
            r'Nêu\s+',           # "Nêu ..."
            r'So\s+sánh',        # "So sánh ..."
            r'Vẽ\s+',            # "Vẽ ..."
            r'Quan\s+sát',       # "Quan sát ..."
            r'Thảo\s+luận',      # "Thảo luận ..."
            r'Em\s+có\s+thể',    # "Em có thể ..."
            r'Theo\s+em',        # "Theo em ..."
            r'Tại\s+sao',        # "Tại sao ..."
            r'Làm\s+thế\s+nào',  # "Làm thế nào ..."
            r'Có\s+những',       # "Có những ..."
            r'\?\s*$',           # Lines ending with question mark
        ]
        
        # Multiple choice patterns
        self.choice_patterns = [
            r'^[A-D]\.',         # A., B., C., D.
            r'^[a-d]\)',         # a), b), c), d)
            r'^[A-D]\s*[.)]',    # A ., B ), etc.
        ]
        
        # Answer/solution indicators
        self.answer_indicators = [
            r'^Giải:',
            r'^Đáp án:',
            r'^Lời giải:',
            r'^Hướng dẫn:',
            r'^Kết quả:',
            r'^Trả lời:',
        ]
        
        # Compile patterns
        self.compiled_question_start = [re.compile(p, re.IGNORECASE) for p in self.question_start_patterns]
        self.compiled_question_content = [re.compile(p, re.IGNORECASE) for p in self.question_content_patterns]
        self.compiled_choices = [re.compile(p, re.IGNORECASE) for p in self.choice_patterns]
        self.compiled_answers = [re.compile(p, re.IGNORECASE) for p in self.answer_indicators]
    
    def is_question_start(self, text: str) -> bool:
        """Check if text starts a new question."""
        text = text.strip()
        for pattern in self.compiled_question_start:
            if pattern.match(text):
                return True
        return False
    
    def is_question_content(self, text: str) -> bool:
        """Check if text contains question content."""
        text = text.strip()
        for pattern in self.compiled_question_content:
            if pattern.search(text):
                return True
        return False
    
    def is_multiple_choice(self, text: str) -> bool:
        """Check if text is a multiple choice option."""
        text = text.strip()
        if len(text) > 200:  # Too long to be a choice
            return False
        for pattern in self.compiled_choices:
            if pattern.match(text):
                return True
        return False
    
    def is_answer_indicator(self, text: str) -> bool:
        """Check if text indicates start of answer."""
        text = text.strip()
        for pattern in self.compiled_answers:
            if pattern.match(text):
                return True
        return False
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        # Remove special characters that might cause CSV issues
        text = text.replace('"', '""')  # Escape quotes for CSV
        return text
    
    def extract_question_answer_pairs_improved(self, paragraphs: List[str]) -> List[Tuple[str, str]]:
        """
        Improved extraction of question-answer pairs.
        
        Args:
            paragraphs (List[str]): List of paragraph texts
            
        Returns:
            List[Tuple[str, str]]: List of (question, answer) pairs
        """
        pairs = []
        current_question = []
        current_answer = []
        state = "looking_for_question"  # States: looking_for_question, in_question, in_answer
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            if self.is_question_start(para):
                # Save previous pair if exists
                if current_question:
                    question_text = self.clean_text(' '.join(current_question))
                    answer_text = self.clean_text(' '.join(current_answer)) if current_answer else ""
                    if question_text:  # Only add if question is not empty
                        pairs.append((question_text, answer_text))
                
                # Start new question
                current_question = [para]
                current_answer = []
                state = "in_question"
                
            elif state == "in_question":
                if self.is_multiple_choice(para):
                    # Multiple choice options are part of the question
                    current_question.append(para)
                elif self.is_answer_indicator(para):
                    # Start of answer section
                    current_answer = [para]
                    state = "in_answer"
                elif self.is_question_content(para) or para.endswith('?'):
                    # Continue question content
                    current_question.append(para)
                else:
                    # This might be an answer or explanation
                    current_answer = [para]
                    state = "in_answer"
                    
            elif state == "in_answer":
                if self.is_question_start(para):
                    # New question found, save current pair
                    question_text = self.clean_text(' '.join(current_question))
                    answer_text = self.clean_text(' '.join(current_answer))
                    if question_text:
                        pairs.append((question_text, answer_text))
                    
                    # Start new question
                    current_question = [para]
                    current_answer = []
                    state = "in_question"
                else:
                    # Continue answer
                    current_answer.append(para)
            
            elif state == "looking_for_question":
                if self.is_question_start(para) or self.is_question_content(para):
                    current_question = [para]
                    current_answer = []
                    state = "in_question"
        
        # Handle the last pair
        if current_question:
            question_text = self.clean_text(' '.join(current_question))
            answer_text = self.clean_text(' '.join(current_answer)) if current_answer else ""
            if question_text:
                pairs.append((question_text, answer_text))
        
        return pairs
    
    def process_json_file(self, file_path: Path) -> List[Tuple[str, str]]:
        """Process JSON file with improved handling."""
        pairs = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Handle malformed JSON
            if not content.strip().startswith('['):
                json_objects = content.strip().split('}{')
                if len(json_objects) > 1:
                    json_objects[0] += '}'
                    for i in range(1, len(json_objects) - 1):
                        json_objects[i] = '{' + json_objects[i] + '}'
                    json_objects[-1] = '{' + json_objects[-1]
                    content = '[' + ','.join(json_objects) + ']'
                else:
                    content = '[' + content + ']'
            
            data = json.loads(content)
            
            for item in data:
                if isinstance(item, dict) and 'cau_hoi' in item:
                    question_text = self.clean_text(item['cau_hoi'])
                    # For JSON, try to extract answer if available
                    answer_text = ""
                    if 'dap_an' in item:
                        answer_text = self.clean_text(item['dap_an'])
                    
                    if question_text:
                        pairs.append((question_text, answer_text))
                        
        except Exception as e:
            print(f"Error processing JSON file {file_path}: {e}")
            
        return pairs
    
    def process_docx_file(self, file_path: Path) -> List[Tuple[str, str]]:
        """Process Word document with improved parsing."""
        pairs = []
        
        try:
            doc = docx.Document(file_path)
            
            # Extract all paragraphs
            paragraphs = []
            for para in doc.paragraphs:
                text = para.text.strip()
                if text:
                    paragraphs.append(text)
            
            # Use improved extraction
            pairs = self.extract_question_answer_pairs_improved(paragraphs)
                
        except Exception as e:
            print(f"Error processing Word document {file_path}: {e}")
            
        return pairs
    
    def process_all_files(self) -> Dict[str, Any]:
        """Process all files with improved logic."""
        if not self.dataset_folder.exists():
            raise FileNotFoundError(f"Dataset folder '{self.dataset_folder}' not found")
        
        results = {
            'total_files': 0,
            'processed_files': 0,
            'total_pairs': 0,
            'file_details': {}
        }
        
        # Get all relevant files
        files = list(self.dataset_folder.glob('*.docx')) + list(self.dataset_folder.glob('*.json'))
        results['total_files'] = len(files)
        
        for file_path in files:
            print(f"Processing: {file_path.name}")
            
            try:
                if file_path.suffix.lower() == '.json':
                    file_pairs = self.process_json_file(file_path)
                elif file_path.suffix.lower() == '.docx':
                    file_pairs = self.process_docx_file(file_path)
                else:
                    continue
                
                # Store results
                self.questions_and_answers.extend(file_pairs)
                
                # Track statistics
                file_stats = {
                    'pairs_count': len(file_pairs),
                    'pairs': file_pairs
                }
                
                results['file_details'][file_path.name] = file_stats
                results['processed_files'] += 1
                
                print(f"  - Found {len(file_pairs)} question-answer pairs")
                
            except Exception as e:
                print(f"Error processing {file_path.name}: {e}")
        
        results['total_pairs'] = len(self.questions_and_answers)
        return results
    
    def save_to_csv(self, output_file: str = "improved_dataset.csv") -> None:
        """Save to CSV with better formatting."""
        if not self.questions_and_answers:
            print("No question-answer pairs found.")
            return
        
        # Create DataFrame
        data = []
        for question, answer in self.questions_and_answers:
            data.append({
                'Cau_hoi': question,
                'Dap_an': answer,
                'Embedding': ""  # Empty for now
            })
        
        df = pd.DataFrame(data)
        
        # Save to CSV with proper encoding
        df.to_csv(output_file, index=False, encoding='utf-8', quoting=1)  # quoting=1 for QUOTE_ALL
        print(f"Saved {len(data)} question-answer pairs to {output_file}")
    
    def create_summary_report(self, output_file: str = "improved_conversion_report.txt") -> None:
        """Create a detailed summary report."""
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("IMPROVED DATASET CONVERSION REPORT\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Total question-answer pairs: {len(self.questions_and_answers)}\n\n")
            
            # Statistics
            questions_with_answers = sum(1 for q, a in self.questions_and_answers if a.strip())
            questions_without_answers = len(self.questions_and_answers) - questions_with_answers
            
            f.write("STATISTICS:\n")
            f.write(f"- Questions with answers: {questions_with_answers}\n")
            f.write(f"- Questions without answers: {questions_without_answers}\n")
            f.write(f"- Average question length: {sum(len(q) for q, a in self.questions_and_answers) / len(self.questions_and_answers):.1f} characters\n")
            f.write(f"- Average answer length: {sum(len(a) for q, a in self.questions_and_answers if a) / max(1, questions_with_answers):.1f} characters\n\n")
            
            # Sample pairs
            f.write("SAMPLE QUESTION-ANSWER PAIRS:\n")
            f.write("-" * 30 + "\n\n")
            
            for i, (question, answer) in enumerate(self.questions_and_answers[:5], 1):
                f.write(f"SAMPLE {i}:\n")
                f.write(f"Question: {question[:300]}{'...' if len(question) > 300 else ''}\n")
                f.write(f"Answer: {answer[:300] if answer else '(No answer)'}{'...' if len(answer) > 300 else ''}\n")
                f.write("\n" + "-" * 50 + "\n\n")
        
        print(f"Summary report saved to {output_file}")


def main():
    """Main function."""
    print("Improved Physics Dataset Converter")
    print("=" * 40)
    
    # Initialize converter
    converter = ImprovedDatasetConverter("dataset_teacher")
    
    # Process all files
    print("\nProcessing files...")
    results = converter.process_all_files()
    
    # Display results
    print(f"\nProcessing Complete!")
    print(f"Files processed: {results['processed_files']}/{results['total_files']}")
    print(f"Total question-answer pairs: {results['total_pairs']}")
    
    # Save to CSV
    print(f"\nSaving to CSV...")
    converter.save_to_csv("improved_dataset.csv")
    
    # Create summary report
    converter.create_summary_report("improved_conversion_report.txt")
    
    print(f"\nConversion complete!")
    print(f"Output files:")
    print(f"  - improved_dataset.csv: Improved dataset in CSV format")
    print(f"  - improved_conversion_report.txt: Detailed report")


if __name__ == "__main__":
    main()
