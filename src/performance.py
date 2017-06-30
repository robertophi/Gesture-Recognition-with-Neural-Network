import os

os.system("kernprof -l main.py")
os.system("python -m line_profiler main.py.lprof")
