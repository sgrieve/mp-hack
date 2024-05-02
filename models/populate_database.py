import pandas as pd
import numpy as np

import json
from pathlib import Path

def add_mp(mp_id: str, dict_in: dict, df: pd.DataFrame):
    """Add an entry to dataframe of mp.csv
    """

    if mp_id in df["ID"]:
        return df
    else:
        # Create new row for mp
        if "PhotoURL" in dict_in.keys():
            photo_url = dict_in["PhotoURL"]
        else:
            photo_url = None

        row = pd.DataFrame([{
            "ID": mp_id,
            "Name": dict_in["Name"],
            "PhotoURL": photo_url,
        }])
        return pd.concat([df, row], ignore_index=True)


def add_subject(dict_in, df):
    """Add an entry to dataframe of subject.csv
        TODO
    """
    return df

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
                    # "WikiURL": uni["WikiURL"],
                    "WikiURL": None,
                }])
            if row is None:
                row = new_row
            else:
                row = pd.concat([row, new_row], ignore_index=True)

    if row is None:
        return df
    else:
        return pd.concat([df, row], ignore_index=True)


def add_relationship(dict_in, df_mp, df_uni, df_rel, df_sub=None):
    """Add an entry to dataframe of relationship.csv,
       linking indexes of the different database csv files

       TODO: Add logic for subject once it is ready
    """
    # Find MP name and university in DF
    # print(df_mp["Name"])
    if dict_in["Name"] in list(df_mp["Name"]):
        row = df_mp.loc[df_mp['Name'] == dict_in["Name"]]
        row = row.reset_index()
        mp_id = str(row["ID"][0])
        print(mp_id)
    else:
        raise ValueError(f"{dict_in['Name']} not in MP dataframe")

    uni_ids = []
    for uni in dict_in["Education"]:
        if uni["UniName"] in list(df_uni["UniName"]):
            # uni_ids.append(str(df_uni.loc[df_uni['UniName'] == uni["UniName"]]["ID"]))
            row = df_uni.loc[df_uni['UniName'] == uni["UniName"]]
            row = row.reset_index()
            uni_id = str(row["ID"][0])
            uni_ids.append(uni_id)

        else:
            raise ValueError(f"{uni['UniName']} not in df_uni")

    # Add rows for each uni / subject
    rows = pd.DataFrame(
        [{"MP": mp_id,
        "University": uni_id,
        "Subject": None} for uni_id in uni_ids]
    )

    # TODO: Add a check to make sure rows do not currently exist
    return pd.concat([df_rel, rows], ignore_index=False)


def load_name_data(path: Path) -> pd.DataFrame:
    """Load JSON data from SPARQL query

    Loads JSON data and returns a Pandas DataFrame with
    Wikipedia/Wikidata ID as the index and MP name as column.

    Args:
        path (Path): Path to JSON data

    Returns:
        pd.DataFrame: Pandas DataFrame 
    """
    with open(path, 'r') as input_file:
        mp_name_id = input_file.readline()
    
    return json.loads(mp_name_id)


def main():
    """Do something useful
    """

    mp_df = pd.read_csv("database/mp.csv")
    uni_df = pd.read_csv("database/university.csv")
    rel_df = pd.read_csv("database/relationship.csv")

    extracted_name_dict = load_name_data("json/mps.json")

    for mp_id, mp_dict in extracted_name_dict.items():
        mp_df = add_mp(str(mp_id), mp_dict, mp_df)
        uni_df = add_university(mp_dict, uni_df)
        rel_df = add_relationship(mp_dict, mp_df, uni_df, rel_df)

    mp_df.to_csv("database/mp.csv")
    uni_df.to_csv("database/university.csv")
    rel_df.to_csv("database/relationship.csv")

if __name__ == "__main__":
    main()
