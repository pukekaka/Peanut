# -*- coding: utf-8 -*-
from pandas import DataFrame
from typing import List, Tuple


def dataframe_astype(df: DataFrame, columns: List[Tuple[str, type]]):

    for column, tp in columns:
        print(df[column])
        if tp == int or tp == float:
            # df[column] = df[column].str.replace(',|-', '').astype(tp, errors='ignore')

            df[column] = df[column].str.replace(r',|-', '', regex=True).astype(tp)
        else:
            # df[column] = df[column].astype(tp, errors='ignore')
            df[column] = df[column].astype(tp)
        print(df[column])
    return df
