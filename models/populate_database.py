import pandas as pd
import numpy as np


def add_mp(dict_in, df):
    """Add an entry to dataframe of mp.csv
    """
    if dict_in["Name"] in df["Name"]:
        return df
    else:
        # Create new row for mp
        mp_id = np.max(df["ID"]) + 1
        row = pd.DataFrame([{
            "ID": mp_id,
            "Name": dict_in["Name"],
            "PhotoURL": dict_in["PhotoURL"],
        }])
        return pd.concat([df, row], ignore_index=True)


def add_subject(dict_in, df):
    """Add an entry to dataframe of subject.csv
    """


def add_university(dict_in, df):
    """Add an entry to dataframe of university.csv
    """
    row = None
    for uni in dict_in["Education"]:
        if uni["UniName"] in df["UniName"]:
            continue
        else:
            # Create new row for University
            uni_id = np.max(df["ID"]) + 1
            new_row = pd.DataFrame([{
                    "ID": uni_id,
                    "UniName": uni["UniName"],
                    "UniLocation": uni["UniLocation"],
                    "WikiURL": uni["WikiURL"],
                }])
            if row is None:
                row = new_row
            else:
                row = pd.concat([row, new_row], ignore_index=True)

    if row is None:
        return df
    else:
        return pd.concat([df, row], ignore_index=True)


def add_relationship(dict_in, df_mp, df_sub, df_uni, df_rel):
    """Add an entry to dataframe of relationship.csv,
       linking indexes of the different database csv files
    """
