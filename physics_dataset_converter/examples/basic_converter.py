#!/usr/bin/env python3
"""
Dataset Converter for Physics Files
===================================

This script converts physics dataset files from dataset_teacher folder 
into CSV format similar to the existing dataset.csv structure.

Output format:
- Cau_hoi: Question text
- Dap_an: Answer/explanation text  
- Embedding: Vector embedding (empty for now, can be generated later)

Author: AI Assistant
"""

import os
import json
import re
import docx
import pandas as pd
from typing import Dict, List, Tuple, Any
from pathlib import Path


class DatasetConverter:
    """Converts physics dataset files to CSV format."""
    
    def __init__(self, dataset_folder: str = "dataset_teacher"):
        """
        Initialize the converter.
        
        Args:
            dataset_folder (str): Path to folder containing dataset files
        """
        self.dataset_folder = Path(dataset_folder)
        self.questions_and_answers = []
        
        # Patterns to identify questions
        self.question_patterns = [
            r'^Câu\s+\d+[:\.]',  # "Câu 1:", "Câu 2.", etc.
            r'^Câu\s+hỏi',       # "Câu hỏi"
            r'^Hoạt\s+động',     # "Hoạt động"
            r'^Bài\s+tập',       # "Bài tập"
            r'^Bài\s+\d+',       # "Bài 1", "Bài 2", etc.
            r'Hãy\s+',           # "Hãy ..." (imperative questions)
            r'Tính\s+',          # "Tính ..." (calculation questions)
            r'Xác\s+định',       # "Xác định ..." (determination questions)
            r'Tìm\s+',           # "Tìm ..." (find questions)
            r'Chứng\s+minh',     # "Chứng minh ..." (proof questions)
            r'Giải\s+thích',     # "Giải thích ..." (explanation questions)
            r'Nêu\s+',           # "Nêu ..." (state/mention questions)
            r'So\s+sánh',        # "So sánh ..." (comparison questions)
            r'Vẽ\s+',            # "Vẽ ..." (drawing questions)
            r'Quan\s+sát',       # "Quan sát ..." (observation questions)
            r'Thảo\s+luận',      # "Thảo luận ..." (discussion questions)
            r'Em\s+có\s+thể',    # "Em có thể ..." (ability questions)
            r'Theo\s+em',        # "Theo em ..." (opinion questions)
            r'Tại\s+sao',        # "Tại sao ..." (why questions)
            r'Làm\s+thế\s+nào',  # "Làm thế nào ..." (how questions)
            r'Có\s+những',       # "Có những ..." (what are questions)
            r'\?\s*$',           # Lines ending with question mark
        ]
        
        # Compile patterns for efficiency
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE | re.MULTILINE) 
                                 for pattern in self.question_patterns]
    
    def is_question(self, text: str) -> bool:
        """
        Determine if a given text is likely a question.
        
        Args:
            text (str): Text to analyze
            
        Returns:
            bool: True if text appears to be a question
        """
        if not text or len(text.strip()) < 5:
            return False
            
        text = text.strip()
        
        # Check against all question patterns
        for pattern in self.compiled_patterns:
            if pattern.search(text):
                return True
                
        return False
    
    def extract_question_answer_pairs(self, paragraphs: List[str]) -> List[Tuple[str, str]]:
        """
        Extract question-answer pairs from a list of paragraphs.
        
        Args:
            paragraphs (List[str]): List of paragraph texts
            
        Returns:
            List[Tuple[str, str]]: List of (question, answer) pairs
        """
        pairs = []
        current_question = []
        current_answer = []
        in_question_mode = False
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            if self.is_question(para):
                # Save previous question-answer pair if exists
                if current_question and current_answer:
                    question_text = '\n'.join(current_question)
                    answer_text = '\n'.join(current_answer)
                    pairs.append((question_text, answer_text))
                
                # Start new question
                current_question = [para]
                current_answer = []
                in_question_mode = True
                
            elif in_question_mode:
                # Check if this might be part of a multi-line question
                # (like answer choices A, B, C, D)
                if (len(para) < 100 and 
                    (para.startswith(('A.', 'B.', 'C.', 'D.', 'a)', 'b)', 'c)', 'd)')) or
                     re.match(r'^[A-D]\s*[.)]', para) or
                     para.lower().startswith(('giải:', 'đáp án:', 'lời giải:')))):
                    current_question.append(para)
                else:
                    # This is likely an answer/explanation
                    current_answer.append(para)
                    in_question_mode = False
            else:
                # Continue collecting answer text
                current_answer.append(para)
        
        # Handle the last question-answer pair
        if current_question and current_answer:
            question_text = '\n'.join(current_question)
            answer_text = '\n'.join(current_answer)
            pairs.append((question_text, answer_text))
        elif current_question:
            # Question without explicit answer - use empty answer
            question_text = '\n'.join(current_question)
            pairs.append((question_text, ""))
        
        return pairs
    
    def process_json_file(self, file_path: Path) -> List[Tuple[str, str]]:
        """
        Process a JSON file and extract question-answer pairs.
        
        Args:
            file_path (Path): Path to the JSON file
            
        Returns:
            List[Tuple[str, str]]: List of (question, answer) pairs
        """
        pairs = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Handle malformed JSON (multiple objects without array brackets)
            if not content.strip().startswith('['):
                # Split by '}{'  and add proper JSON array formatting
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
                    question_text = item['cau_hoi'].strip()
                    # For JSON files, we don't have separate answers, so use empty string
                    answer_text = ""
                    if question_text:
                        pairs.append((question_text, answer_text))
                        
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON file {file_path}: {e}")
        except Exception as e:
            print(f"Error processing JSON file {file_path}: {e}")
            
        return pairs
    
    def process_docx_file(self, file_path: Path) -> List[Tuple[str, str]]:
        """
        Process a Word document and extract question-answer pairs.
        
        Args:
            file_path (Path): Path to the .docx file
            
        Returns:
            List[Tuple[str, str]]: List of (question, answer) pairs
        """
        pairs = []
        
        try:
            doc = docx.Document(file_path)
            
            # Extract all paragraphs
            paragraphs = []
            for para in doc.paragraphs:
                text = para.text.strip()
                if text:
                    paragraphs.append(text)
            
            # Extract question-answer pairs
            pairs = self.extract_question_answer_pairs(paragraphs)
                
        except Exception as e:
            print(f"Error processing Word document {file_path}: {e}")
            
        return pairs
    
    def process_all_files(self) -> Dict[str, Any]:
        """
        Process all files in the dataset folder.
        
        Returns:
            Dict[str, Any]: Processing results and statistics
        """
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
    
    def save_to_csv(self, output_file: str = "converted_dataset.csv") -> None:
        """
        Save the extracted question-answer pairs to CSV format.
        
        Args:
            output_file (str): Output CSV file path
        """
        if not self.questions_and_answers:
            print("No question-answer pairs found. Please run process_all_files() first.")
            return
        
        # Create DataFrame
        data = []
        for question, answer in self.questions_and_answers:
            data.append({
                'Cau_hoi': question,
                'Dap_an': answer,
                'Embedding': ""  # Empty for now, can be generated later
            })
        
        df = pd.DataFrame(data)
        
        # Save to CSV
        df.to_csv(output_file, index=False, encoding='utf-8')
        print(f"Saved {len(data)} question-answer pairs to {output_file}")
    
    def save_detailed_analysis(self, output_file: str = "conversion_analysis.txt") -> None:
        """
        Save detailed analysis of the conversion process.
        
        Args:
            output_file (str): Output analysis file path
        """
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("DATASET CONVERSION ANALYSIS\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Total question-answer pairs: {len(self.questions_and_answers)}\n\n")
            
            f.write("SAMPLE QUESTION-ANSWER PAIRS:\n")
            f.write("-" * 30 + "\n\n")
            
            # Show first 10 pairs as examples
            for i, (question, answer) in enumerate(self.questions_and_answers[:10], 1):
                f.write(f"PAIR {i}:\n")
                f.write(f"Question: {question[:200]}{'...' if len(question) > 200 else ''}\n")
                f.write(f"Answer: {answer[:200]}{'...' if len(answer) > 200 else ''}\n")
                f.write("\n" + "-" * 50 + "\n\n")
        
        print(f"Detailed analysis saved to {output_file}")


def main():
    """Main function to run the dataset conversion."""
    print("Physics Dataset Converter")
    print("=" * 40)
    
    # Initialize converter
    converter = DatasetConverter("dataset_teacher")
    
    # Process all files
    print("\nProcessing files...")
    results = converter.process_all_files()
    
    # Display results
    print(f"\nProcessing Complete!")
    print(f"Files processed: {results['processed_files']}/{results['total_files']}")
    print(f"Total question-answer pairs: {results['total_pairs']}")
    
    # Show file-by-file breakdown
    print(f"\nFile-by-file breakdown:")
    for filename, stats in results['file_details'].items():
        print(f"  {filename}: {stats['pairs_count']} pairs")
    
    # Save to CSV
    print(f"\nSaving to CSV...")
    converter.save_to_csv("converted_dataset.csv")
    
    # Save detailed analysis
    converter.save_detailed_analysis("conversion_analysis.txt")
    
    print(f"\nConversion complete!")
    print(f"Output files:")
    print(f"  - converted_dataset.csv: Main dataset in CSV format")
    print(f"  - conversion_analysis.txt: Detailed analysis")


if __name__ == "__main__":
    main()
