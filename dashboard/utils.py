import datetime

import pandas as pd
import plotly.express as px


def load_data():
    """
    A helper function for getting the data in some decent state. 
    """
    df = pd.read_csv(
        "https://raw.githubusercontent.com/jrg94/personal-data/main/health/weightlifting.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Volume"] = df["Weight"] * df["Total Reps"]
    df["Projected 1RM"] = df["Weight"] * (1 + (df["Reps"] / 30))
    return df


def time_filter(df: pd.DataFrame, window: str):
    """
    A help function to filter the dataframe by time window.
    """
    curr = df
    if window == "Last Three Months":
        curr = df[df["Date"] >= datetime.date.today() -
                  pd.offsets.MonthBegin(3)]
    return curr


def plot_exercise_sets_reps(df: pd.DataFrame, window: str, muscle: str, exercise: str):
    """
    :param df: the complete dataset
    :param window: the time window to filter by
    :param muscle: the muscle group to filter by
    :param exercise: the exercise to filter by
    """
    temp = time_filter(df, window)
    muscle_df = temp[temp["Muscle Groups"] == muscle]
    exercise_df = muscle_df[muscle_df["Exercise"] == exercise]
    figure = px.line(
        exercise_df,
        x="Date",
        y="Weight",
        facet_col="Sets",
        color="Reps",
        category_orders={
            # Ensures only existing sets are shown
            "Sets": sorted(exercise_df["Sets"].unique()),
            # Ensures colors are constant between plots
            "Reps": sorted(df["Reps"].unique()),
        },
        markers=True,
        symbol="Per Arm"
    )
    return figure
