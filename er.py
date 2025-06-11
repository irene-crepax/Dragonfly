import pandas as pd
import recordlinkage
from recordlinkage.preprocessing import clean
from preprocessing_step import load_and_describe


def run_record_linkage(df1, df2, blocking=None, compare_columns=None, threshold=0.85):
    indexer = recordlinkage.Index()
    if blocking:
        indexer.sortedneighbourhood(on=blocking)
        indexer.block(on=blocking)
    else:
        indexer.full()
    candidate_links = indexer.index(df1, df2)

    compare = recordlinkage.Compare()
    for col1, col2 in compare_columns:
        compare.string(col1, col2, method='cosine', label=f"{col1}_{col2}")

    features = compare.compute(candidate_links, df1, df2)
    matches = features[features.sum(axis=1) >= 1].sort_index(level=0)
    return matches, features


def create_matched_catalogue(df1, df2, matches, features=None):
    df1_matches = df1.loc[matches.index.get_level_values(0)].reset_index(drop=True)
    df2_matches = df2.loc[matches.index.get_level_values(1)].reset_index(drop=True)

    df1_matches.columns = [f"A_{col}" for col in df1_matches.columns]
    df2_matches.columns = [f"B_{col}" for col in df2_matches.columns]

    final_df = pd.concat([df1_matches, df2_matches], axis=1)

    if features is not None:
        matched_features = features.loc[matches.index].reset_index()
        final_df = pd.concat([final_df, matched_features], axis=1)

    return final_df

def save_catalogue(df, path):
    df.to_csv(path, index=False)


ts = load_and_describe('files/ts_cleaned.csv', 'ts')
bd = load_and_describe('files/bd_cleaned.csv', list_columns=['categories'])
bd= bd.explode('categories').reset_index(drop=True)
ts = ts.rename(columns={"category": "blocking_category"})
bd = bd.rename(columns={"categories": "blocking_category"})
print(ts['blocking_category'].head())
print(bd['blocking_category'].head())

matches, features = run_record_linkage(bd, ts, blocking='blocking_category', compare_columns=[("product_name", "name"), ("description", "description")])
print(matches)
print(features)
catalogue = create_matched_catalogue(bd, ts, matches, features)
print(len(catalogue))
save_catalogue(catalogue, "files/matched_catalogue.csv")
