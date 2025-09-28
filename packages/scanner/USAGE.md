# Tavo AI Security Scanner - Usage Examples

## Single File Scan
python tavo_scanner.py test_llm.py

## Directory Scan  
python tavo_scanner.py /path/to/codebase

## JSON Output (default)
python tavo_scanner.py test_llm.py --format json

## Text Output
python tavo_scanner.py test_llm.py --format text

## Verbose Output
python tavo_scanner.py test_llm.py --verbose

## Custom Rule Bundle
python tavo_scanner.py test_llm.py --bundle custom-rules
