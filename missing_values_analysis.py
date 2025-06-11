import pandas as pd
from preprocessing_step import load_and_describe


def analyse_missing(path, col1, col2):
    df = load_and_describe(path)
    grouped = df.groupby(col1)[col2].agg(
        total='count',
        missing=lambda x: x.isnull().sum()
    ).reset_index()
    print(grouped)
    # Add flag if missing == total (i.e., all rows missing for this website)
    grouped['all_missing'] = grouped['missing'] >= grouped['total']
    grouped['none_missing'] = grouped['missing'] == 0
    print(grouped)
    # Rows where some are missing and some are not
    inconsistent = grouped[~(grouped['all_missing'] | grouped['none_missing'])]

    print(f"🧪 Inconsistent: {len(inconsistent)}")
    if inconsistent.empty:
        print(f"Each {col1} either always {col2} or never does.")
    else:
        print(inconsistent.head())

    print(f"{(grouped['all_missing'].sum() / len(grouped)):.2%} of {col1} always have missing {col2}.")
    print(f"{(grouped['none_missing'].sum() / len(grouped)):.2%} of {col1} always have {col2}.")


