"""produce dataset of "matched" arrests for survey"""

import pandas

# create basic arrest data
arrest_data = pandas.read_csv("data/clean/temp/arrest.csv")
prisoner_data = pandas.read_csv("data/clean/temp/prisoner.csv")
arrest_data = arrest_data.merge(prisoner_data, on="prisoner_id")

# method A: loop over arrests
arrest_pairs_a = pandas.DataFrame()
while arrest_pairs_a.shape[0] < 100:
    arrest_left = arrest_data.sample(n=1)

    # get IDs of potential matches
    row_matches_ids = (
        (arrest_data["release_flag"] != arrest_left["release_flag"].iloc[0]) 
        & (arrest_data["sex"] == arrest_left["sex"].iloc[0])
        & (arrest_data["race"] == arrest_left["race"].iloc[0])
    )

    # get potential matches
    arrest_matches = arrest_data[row_matches_ids]

    # add pair to final dataset
    if arrest_matches.shape[0] > 0:
        arrest_match = arrest_matches.sample(n=1)
        arrest_pair = pandas.DataFrame(
            {
                "arrest_id_left": arrest_left["arrest_id"].iloc[0],
                "prisoner_id_left": arrest_left["prisoner_id"].iloc[0],
                "arrest_id_right": arrest_match["arrest_id"].iloc[0],
                "prisoner_id_right": arrest_match["prisoner_id"].iloc[0],
            },
            index=[0]
        )
        arrest_pairs_a = pandas.concat([arrest_pairs_a, arrest_pair])


# method B: cross-join all arrests
arrest_pairs_b = (
    pandas.merge(
        arrest_data[arrest_data["release_flag"] == 0][["arrest_id", "prisoner_id", "race", "sex"]],
        arrest_data[arrest_data["release_flag"] == 1][["arrest_id", "prisoner_id", "race", "sex"]],
        on=["race", "sex"],
        suffixes=["_left", "_right"],
    )
    .drop(["race", "sex"], axis=1)
    .sample(n=100)
)
