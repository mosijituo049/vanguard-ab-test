import pandas as pd

def add_segment(
    df,
    column,
    bins,
    labels,
    segment_name
):
    df = df.copy()

    df[segment_name] = pd.cut(
        df[column],
        bins=bins,
        labels=labels,
        right=False
    )

    return df