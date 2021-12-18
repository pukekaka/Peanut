# -*- coding: utf-8 -*-
from pandas import DataFrame
import pandas as pd
from typing import List, Tuple


def dataframe_astype(df: DataFrame, columns: List[Tuple[str, type]]):

    for column, tp in columns:
        if tp == int or tp == float:
            df[column] = df[column].str.replace(r',', '', regex=True).astype(tp, errors='ignore')
            df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0)
            df[column] = df[column].astype(tp, errors='ignore')
        else:
            df[column] = df[column].astype(tp)

    return df
