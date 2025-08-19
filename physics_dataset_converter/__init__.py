"""
Physics Dataset Converter Package
=================================

A comprehensive Python package for converting physics educational content
from Word documents and JSON files into structured CSV datasets.

Features:
- Multi-format support (Word documents, JSON files)
- Intelligent question-answer separation
- CSV export compatible with machine learning workflows
- Detailed analysis and reporting

Author: AI Assistant
Version: 1.0.0
"""

from .core.converter import ImprovedDatasetConverter

__version__ = "1.0.0"
__author__ = "AI Assistant"

__all__ = [
    'ImprovedDatasetConverter'
]

def quick_convert(input_folder="dataset_teacher", output_file="physics_dataset.csv"):
    """
    Quick conversion function for immediate use.
    
    Args:
        input_folder (str): Path to folder containing dataset files
        output_file (str): Output CSV file path
        
    Returns:
        dict: Conversion results
    """
    converter = ImprovedDatasetConverter(input_folder)
    results = converter.process_all_files()
    converter.save_to_csv(output_file)
    return results
