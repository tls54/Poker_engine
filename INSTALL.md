# Poker Project Engine – Experimental Build Guide

## Requirements
•	Python 3.10 or higher  
•	pip (Python package installer)  
•	C++ compiler (e.g. g++, clang++)   
•	pybind11 (headers only — installable via pip)  	  
•	numpy and other Python dependencies   

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Program Structure
```
Poker_project_engine/  
├── poker_engine/                # Core engine source code  
│   ├── hand_eval.cpp            # C++ hand evaluator  
│   ├── hand_eval.cpython-xxx.so  # (auto-built after pip install)  
│   ├── back_end/                # Python core logic (cards, players)  
│   └── preset_ranges/           # 13x13 hand range matrices (.npy)  
│       └── range_loader.py      # Utility to load .npy matrices  
├── Benchmarks/                  # Benchmarking code  
├── testing/                     # Testing and development   notebooks  
├── Info/                        # Overview, build info, hand ranking docs  
├── setup.py                     # Python build script  
├── pyproject.toml               # Optional – modern Python packaging config  
└── INSTALL.md       # This guide  
```


## Install in Development Mode
```Bash
pip install -e .
```
## Running Benchmarks and tests
Benchmark Example:
```
python Benchmarks/Python_vs_cpp.py
```
Test Preset Range Directory:
``` Bash
python -c "from poker_engine.preset_ranges import load_range; print(load_range('22+and_suited'))"
```
