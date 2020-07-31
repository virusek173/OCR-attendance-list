# OCR-attendance-list
## Processing stages:
- perspective - Detecting corners of the paper, correcting the perspective and cutting out the paper.
- removeKartkens - Detecting and removing lines.
- checkered - Removing the checkered from the paper so that only words remains visible.
- words - Detecting words positions.
- digits - Detection of individual digits.
- train_model - Functions to train model.
- predict_model - Functions to predict model.
- utils - Helper functions
- final - Final file run all functions and return result.

Each stage is in separate file.
final.py file should run all modules.

## Development:
- `pip install -r requirements.txt`
- `python3 final.py` 
