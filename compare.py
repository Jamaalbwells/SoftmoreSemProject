import argparse
from correlation import correlate
from tkinter.filedialog import askdirectory
def initialize(song, song2):

  
    SOURCE_FILE = song
    TARGET_FILE = song2
    if not SOURCE_FILE or not TARGET_FILE:
      raise Exception("Source or Target files not specified.")
    return SOURCE_FILE, TARGET_FILE
  
if __name__ == "__main__":
    SOURCE_FILE, TARGET_FILE = initialize()
    correlate(SOURCE_FILE, TARGET_FILE)