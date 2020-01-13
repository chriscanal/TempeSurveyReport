import pandas as pd
from IPython.display import display, HTML, display_html
import matplotlib.pyplot as plt
from collections import Counter

answer_map = {
    1: "strongly DISAGREE",
    2: "Disagree",
    3: "Neutral",
    4: "Agree",
    5: "Strongly AGREE",
    9: "Don't Know",
}
plot_map = {
    1: "DISAGREE!",
    2: "Disagree",
    3: "Neutral",
    4: "Agree",
    5: "AGREE!",
    9: "Unknown",
}


def display_side_by_side(*args):
    html_str = ""
    for df in args:
        html_str += df.to_html()
    display_html(html_str.replace("table", 'table style="display:inline"'), raw=True)


def get_possible_responses():
    return pd.DataFrame(
        [
            "strongly DISAGREE",
            "Disagree",
            "Neutral",
            "Agree",
            "Strongly AGREE",
            "Don't Know",
        ],
        index=[1, 2, 3, 4, 5, 9],
        columns=["Possible Response Key"],
    )


def print_stats(data=None, q_map=None, questions=None, bar_chart=True):
    possible_responses = get_possible_responses()
    for q in questions:
        df = data[q_map[q]]
        df_donts = df[df == 9]
        df_responses = df[df != 9]
        df_stats = df_responses.describe()[["count", "mean", "50%", "std"]]
        df_stats = df_stats.rename(
            {
                "count": "response count (1-5)",
                "mean": "average",
                "50%": "median",
                "std": "standard deviation",
            }
        )
        df_stats["percent dont know"] = len(df_donts) / len(df)
        df_stats["most common response"] = answer_map[df.value_counts().idxmax()]
        df_stats = pd.DataFrame(df_stats)
        display_side_by_side(df_stats, possible_responses)
        counts = Counter(df)
        items = [[plot_map[k], counts[k]] for k in [1, 2, 3, 4, 5, 9]]
        plot_df = pd.DataFrame(items, columns=["response", "count"])
        plot_df.plot.bar(x="response", y="count", rot=0)
        plt.show()


def get_top_response_cols(data, value=None, value2=None, n=3):
    if not value2:
        value2 = value
    num_responses = len(data)
    responses = []
    for col in data.keys():
        responses.append([col, len(data[data[col] == value | data[col] == value2])])
    top_questions = sorted(responses, key=lambda x: x[1], reverse=True)[:n]
    return [
        [q, num, "%.2f%%" % (100 * int(num) / num_responses)]
        for q, num in top_questions
    ]


def print_dont_knows(data=None, n=3):
    print("MOST AMBIGUOUS QUESTIONS ACCORDING TO USERS")
    top_questions = get_top_response_cols(data, value=9, n=n)
    pd.options.display.max_colwidth = 100
    df = pd.DataFrame(
        top_questions, columns=["Question", "Num Don't Knows", "Percent Don't Know"]
    )
    display(df)


def print_n_strong_agrees(data=None, n=3):
    print("MOST AMBIGUOUS QUESTIONS ACCORDING TO USERS")
    top_questions = get_top_response_cols(data, value=5, n=n)
    pd.options.display.max_colwidth = 100
    df = pd.DataFrame(
        top_questions, columns=["Question", "Num Strong Agrees", "Percent Strong Agree"]
    )
    display(df)


def print_n_agrees(data=None, n=3):
    print("MOST AMBIGUOUS QUESTIONS ACCORDING TO USERS")
    top_questions = get_top_response_cols(data, value=5, value2=4, n=n)
    pd.options.display.max_colwidth = 100
    df = pd.DataFrame(
        top_questions, columns=["Question", "Num Don't Knows", "Percent Don't Know"]
    )
    display(df)


def print_n_strong_disagrees(data=None, n=3):
    print("MOST AMBIGUOUS QUESTIONS ACCORDING TO USERS")
    top_questions = get_top_response_cols(data, value=1, n=n)
    pd.options.display.max_colwidth = 100
    df = pd.DataFrame(
        top_questions, columns=["Question", "Num Don't Knows", "Percent Don't Know"]
    )
    display(df)


def print_n_disagrees(data=None, n=3):
    print("MOST AMBIGUOUS QUESTIONS ACCORDING TO USERS")
    top_questions = get_top_response_cols(data, value=1, value2=2, n=n)
    pd.options.display.max_colwidth = 100
    df = pd.DataFrame(
        top_questions, columns=["Question", "Num Don't Knows", "Percent Don't Know"]
    )
    display(df)


def print_n_most_correlated(data=None, n=3):
    pass
