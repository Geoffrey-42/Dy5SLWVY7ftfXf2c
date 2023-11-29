import os
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

import pandas as pd
import numpy as np
from math import isclose

import nltk
nltk.download('punkt')
nltk.download('stopwords')
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sentence_transformers import SentenceTransformer

from sklearn.preprocessing import normalize

print('setup file was run')