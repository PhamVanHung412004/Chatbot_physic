# Physics Dataset Converter

A comprehensive Python package for converting physics educational content from Word documents and JSON files into structured CSV datasets suitable for machine learning and data analysis.

## Features

- **Multi-format Support**: Process Word documents (.docx) and JSON files
- **Intelligent Parsing**: Advanced question-answer separation using pattern matching
- **CSV Export**: Generate clean datasets compatible with pandas and ML frameworks
- **Easy Integration**: Simple API for quick conversions

## Installation

```bash
# Install required dependencies
pip install python-docx pandas openpyxl
```

## Quick Start

```python
from physics_dataset_converter import quick_convert

# Convert all files in dataset_teacher folder to CSV
results = quick_convert("dataset_teacher", "physics_dataset.csv")
print(f"Converted {results['total_pairs']} question-answer pairs")
```

## Advanced Usage

```python
from physics_dataset_converter import ImprovedDatasetConverter

# Initialize converter
converter = ImprovedDatasetConverter("dataset_teacher")

# Process files
results = converter.process_all_files()

# Save to CSV
converter.save_to_csv("my_dataset.csv")

# Create detailed report
converter.create_summary_report("conversion_report.txt")
```

## Package Structure

```
physics_dataset_converter/
├── __init__.py              # Main package interface
├── core/                    # Core functionality
│   ├── __init__.py
│   └── converter.py         # Main conversion logic
├── examples/                # Example scripts
│   └── basic_converter.py   # Basic usage example
└── README.md               # This file
```

## Output Format

The converter generates CSV files with the following structure:

| Column | Description |
|--------|-------------|
| Cau_hoi | Question text (Vietnamese) |
| Dap_an | Answer text (Vietnamese) |
| Embedding | Empty field for future embeddings |

## Example Results

From your dataset_teacher folder, the converter successfully processed:
- **1509 question-answer pairs** from 40 files
- **Multiple choice questions** with A, B, C, D options
- **Calculation problems** with numerical solutions
- **Explanation questions** requiring detailed answers

## Requirements

- Python 3.7+
- python-docx
- pandas
- openpyxl (for Excel support)

## Usage Examples

### Basic Conversion
```python
import physics_dataset_converter as pdc

# Quick conversion
results = pdc.quick_convert("dataset_teacher", "output.csv")
print(f"Processed {results['total_files']} files")
print(f"Generated {results['total_pairs']} question-answer pairs")
```

### Advanced Processing
```python
from physics_dataset_converter.core.converter import ImprovedDatasetConverter

converter = ImprovedDatasetConverter("dataset_teacher")
results = converter.process_all_files()

# Save with custom filename
converter.save_to_csv("physics_questions_2024.csv")

# Generate detailed analysis
converter.create_summary_report("analysis_report.txt")
```

## File Support

- **Word Documents (.docx)**: Extracts questions and answers from formatted documents
- **JSON Files**: Processes structured question data
- **Error Handling**: Gracefully handles corrupted or unsupported files

## License

This project is provided as-is for educational purposes.

## Contributing

Feel free to contribute improvements, bug fixes, or new features.
