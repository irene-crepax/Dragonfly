import pandas as pd
import numpy as np
import ast
import spacy
from pandas.api.types import is_list_like
from handling_missing_values import *

# Load spaCy model (you can choose a larger model if needed)
nlp = spacy.load("en_core_web_sm")


# 1. Load and describe the dataset
def load_and_describe(path, name="DataFrame", list_columns=None):
    if list_columns is None:
        list_columns = []
    df = pd.read_csv(path)
    for col in list_columns:
        df[col] = df[col].apply(lambda x: ast.literal_eval(x) if pd.notnull(x) else x)
    print(f"\n📄 {name}")
    print(f"Rows: {len(df):,}")
    print(f"Columns ({len(df.columns)}): {', '.join(df.columns)}")
    for col in df.columns:
        print(f"\n🔍 Column: '{col}'")
        value_types = df[col].dropna().map(type).value_counts()
        for t, count in value_types.items():
            print(f"  - {t.__name__}")
    print("\n❓ Missing Values:")
    print(df.isnull().sum())
    return df


def spacy_normalize(text):
    if not isinstance(text, str) or text.strip() == "":
        return ""
    doc = nlp(text)
    tokens = [token.lemma_.lower().strip() for token in doc if not token.is_punct and not token.is_space]
    return " ".join(tokens)


# 2. Normalize string and list contents using spaCy
def normalize_column_spacy(df, col):
    def normalize(x):
        if is_list_like(x):
            return [spacy_normalize(str(i)) for i in x]
        if isinstance(x, str):
            return spacy_normalize(x)
        return x

    df[col] = df[col].apply(normalize)
    return df


### Run the functions by changing file paths, names, and list_columns (if your file contains a column of lists)
### Example
ts = load_and_describe('files/ts_technologies - ts_technologies.csv', name="ts")
for col in ts.columns:
    ts = normalize_column_spacy(ts, col)

ts.to_csv('files/ts_cleaned.csv', index=False)

bd = load_and_describe('files/bd_technologies.csv', name="bd", list_columns=['categories'])
for col in bd.columns:
    bd = normalize_column_spacy(bd, col)
bd.to_csv('files/bd_cleaned.csv', index=False)


# 3. Visualize missing values
test_missing_values(ts)
test_missing_values(bd)






