# OCR-attendance-list
## Processing stages:
- perspective - Detecting corners of the paper, correcting the perspective and cutting out the paper.
- checkered - Removing the checkered from the paper so that only words are visible.
- rows - finding rows.
- cols - finding cols.
- digits - Detection of individual digits.
- final-recognition - Final number recognition.

Each stage is in separate file.

final-recognition.py file should run all modules.

## Development:
- `pip install -r requirements.txt`
- `python3 final-recognition.py` 
