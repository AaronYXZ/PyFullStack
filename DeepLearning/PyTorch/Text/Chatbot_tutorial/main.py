import torch
import os

from torch.jit import script, trace


USE_CUDA = torch.cuda.is_available()
device = torch.device("cuda" if USE_CUDA else "cpu")

## Load and preprocess data
corpus_name = "cornell movie-dialogs corpus"
corpus = os.path.join("data", corpus_name)

def print_lines(file, n = 10):
    with open(file, "rb") as datafile:
        lines = datafile.readlines()
    for line in lines[:n]:
        print(line)

print_lines(os.path.join(corpus, "movie_lines.txt"))