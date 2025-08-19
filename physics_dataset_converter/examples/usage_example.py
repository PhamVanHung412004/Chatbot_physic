#!/usr/bin/env python3
"""
Usage Example for Physics Dataset Converter
===========================================

This script demonstrates how to use the physics dataset converter package.

Author: AI Assistant
"""

import sys
import os

# Add parent directory to path to import the package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from physics_dataset_converter import ImprovedDatasetConverter, quick_convert


def example_quick_conversion():
    """Example of quick conversion using the convenience function."""
    print("=" * 50)
    print("EXAMPLE 1: Quick Conversion")
    print("=" * 50)
    
    # Quick conversion - one line of code!
    results = quick_convert("dataset_teacher", "quick_output.csv")
    
    print(f"Quick conversion completed!")
    print(f"Files processed: {results['processed_files']}")
    print(f"Total question-answer pairs: {results['total_pairs']}")


def example_advanced_usage():
    """Example of advanced usage with detailed control."""
    print("\n" + "=" * 50)
    print("EXAMPLE 2: Advanced Usage")
    print("=" * 50)
    
    # Initialize converter
    converter = ImprovedDatasetConverter("dataset_teacher")
    
    # Process all files with detailed output
    print("Processing files...")
    results = converter.process_all_files()
    
    # Display detailed results
    print(f"\nDetailed Results:")
    print(f"Total files found: {results['total_files']}")
    print(f"Successfully processed: {results['processed_files']}")
    print(f"Total question-answer pairs: {results['total_pairs']}")
    
    # Show file-by-file breakdown
    print(f"\nFile-by-file breakdown:")
    for filename, stats in results['file_details'].items():
        print(f"  {filename}: {stats['pairs_count']} pairs")
    
    # Save to custom CSV file
    converter.save_to_csv("advanced_output.csv")
    
    # Create detailed analysis report
    converter.create_summary_report("detailed_analysis.txt")
    
    print(f"\nAdvanced processing completed!")
    print(f"Files generated:")
    print(f"  - advanced_output.csv: Main dataset")
    print(f"  - detailed_analysis.txt: Analysis report")


def example_custom_processing():
    """Example of custom processing for specific needs."""
    print("\n" + "=" * 50)
    print("EXAMPLE 3: Custom Processing")
    print("=" * 50)
    
    # Initialize converter
    converter = ImprovedDatasetConverter("dataset_teacher")
    
    # Process files
    results = converter.process_all_files()
    
    # Access the raw question-answer pairs for custom processing
    pairs = converter.questions_and_answers
    
    # Custom analysis
    multiple_choice_count = 0
    calculation_count = 0
    short_questions = 0
    long_questions = 0
    
    for question, answer in pairs:
        # Count multiple choice questions
        if any(option in question for option in ['A.', 'B.', 'C.', 'D.']):
            multiple_choice_count += 1
        
        # Count calculation questions
        if any(keyword in question.lower() for keyword in ['tính', 'xác định', 'tìm']):
            calculation_count += 1
        
        # Categorize by length
        if len(question) < 100:
            short_questions += 1
        else:
            long_questions += 1
    
    print(f"Custom Analysis Results:")
    print(f"  Multiple choice questions: {multiple_choice_count}")
    print(f"  Calculation questions: {calculation_count}")
    print(f"  Short questions (<100 chars): {short_questions}")
    print(f"  Long questions (>=100 chars): {long_questions}")
    
    # Save filtered datasets
    # Save only multiple choice questions
    mc_pairs = [(q, a) for q, a in pairs if any(opt in q for opt in ['A.', 'B.', 'C.', 'D.'])]
    
    if mc_pairs:
        import pandas as pd
        mc_df = pd.DataFrame([
            {'Cau_hoi': q, 'Dap_an': a, 'Embedding': ''} 
            for q, a in mc_pairs
        ])
        mc_df.to_csv("multiple_choice_questions.csv", index=False, encoding='utf-8')
        print(f"  - multiple_choice_questions.csv: {len(mc_pairs)} questions")


def main():
    """Main function to run all examples."""
    print("Physics Dataset Converter - Usage Examples")
    print("=" * 60)
    print("This script demonstrates various ways to use the converter.")
    print()
    
    try:
        # Run examples
        example_quick_conversion()
        example_advanced_usage()
        example_custom_processing()
        
        print("\n" + "=" * 60)
        print("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("\nGenerated files:")
        print("- quick_output.csv: Quick conversion result")
        print("- advanced_output.csv: Advanced processing result")
        print("- detailed_analysis.txt: Detailed analysis report")
        print("- multiple_choice_questions.csv: Filtered multiple choice questions")
        
        print("\nYou can now:")
        print("1. Examine the generated CSV files")
        print("2. Use them for machine learning or data analysis")
        print("3. Modify the converter for your specific needs")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        print("Make sure you have:")
        print("1. The 'dataset_teacher' folder with your files")
        print("2. Required Python packages: python-docx, pandas")
        print("3. Proper file permissions")


if __name__ == "__main__":
    main()
