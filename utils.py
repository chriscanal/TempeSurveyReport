import re
import pandas as pd


def get_clean_df(file=None):
    df = pd.read_csv(file)
    df = df.astype("int32")
    df = df.set_index("ID")
    rename_dict = {}
    for key in df.keys():
        rename_dict[key] = key.split(" ")[0]
    return df.rename(columns=rename_dict)


def get_data(df_file=None, col_names_file=None):
    df = get_clean_df(file=df_file)
    full_col_names = []
    with open(col_names_file, "r") as f:
        full_col_names = f.read().split("\n")

    full_name_question_map = {}
    special_questions = {
        "9": " The following adequately support my work-related needs:",
        "10": " The following programs/services adequately support my needs:",
    }

    for text in full_col_names:
        period_loc = text.find(".")
        question_number = text[:period_loc]
        if question_number:
            stripped_number = re.sub("[^0-9]", "", question_number)
            if stripped_number in special_questions:
                special_text = (
                    "Q"
                    + question_number
                    + "."
                    + special_questions[stripped_number]
                    + text[period_loc + 1 :]
                )
                full_name_question_map["Q" + question_number] = special_text
            else:
                full_name_question_map["Q" + question_number] = "Q" + text
    return df.rename(columns=full_name_question_map), full_name_question_map
