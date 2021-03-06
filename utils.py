import datetime

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import html
from plotly_calplot import calplot

import constants


def load_data(url: str):
    """
    A helper function for getting the data in some decent state. 
    """
    df = pd.read_csv(url)
    df["Date"] = pd.to_datetime(df["Date"])
    if url == constants.WEIGHTLIFTING_URL:
        df["Volume"] = df["Weight"] * df["Total Reps"]
        df["Projected 1RM"] = df["Weight"] * (1 + (df["Reps"] / 30))
        df["Per Arm"] = df["Per Arm"].map({True: "Yes", False: "No"})
    return df


def time_filter(df: pd.DataFrame, window: str):
    """
    A help function to filter the dataframe by time window.
    """
    curr = df
    if window == "Last Three Months":
        curr = df[
            df["Date"] >= datetime.date.today() - pd.offsets.MonthBegin(3)
        ]
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
        symbol="Per Arm",
    )
    return figure


def create_recent_exercises_table(df: pd.DataFrame, muscle: str, exercise: str):
    """
    Creates a nice table of the recent sets by reps for a given exercise. 

    :param df: the complete dataset
    :param muscle: the muscle group to filter by
    :param exercise: the exercise to filter by
    """
    temp = df[(df["Muscle Groups"] == muscle) & (
        df["Exercise"] == exercise)].groupby(["Sets", "Reps"]).last()
    temp.drop(df.columns.difference(
        ["Sets", "Reps", "Per Arm", "Weight", "Difficulty"]), axis=1, inplace=True)
    table = dbc.Table.from_dataframe(
        temp, striped=True, bordered=True, hover=True, index=True)
    return table


def create_video_description_row(exercise_constants: dict):
    """
    Creates a row that contains the exercise video and its description.

    :param exercise_constants: the constants for the exercise
    """
    if "src" in exercise_constants:
        return dbc.Row(
            [
                dbc.Col(
                    html.Iframe(
                        src=exercise_constants.get("src", ""),
                        style={"width": "560px", "height": "315px"}
                    ),
                    width="auto"
                ),
                dbc.Col(html.P(exercise_constants.get("description", "")))
            ],
            class_name="justify-content-start"
        )
    else:
        return dbc.Row(
            dbc.Col(html.P(exercise_constants.get("description", "")))
        )


def create_fatique_plot():
    # Load data
    df = load_data(constants.WEIGHTLIFTING_URL)

    # Workout plots
    fatigue = (
        df[df["Date"] >= datetime.date.today() - pd.offsets.Day(2)]
        .groupby("Muscle Groups")
        .agg({"Volume": "sum", "Projected 1RM": "mean"})
    )

    missing = set(df["Muscle Groups"].unique()) - set(fatigue.index)
    fatigue["Cumulative Volume / Average Project 1RM"] = (
        fatigue["Volume"] / fatigue["Projected 1RM"]
    )

    for muscle in missing:
        fatigue.loc[muscle] = 0
    
    fatigue = fatigue.sort_values("Cumulative Volume / Average Project 1RM", ascending=True)
    return px.bar(fatigue, y="Cumulative Volume / Average Project 1RM")


def create_calendar_plot():
    df = load_data(constants.WEIGHTLIFTING_URL)
    days = df.groupby("Date").agg({"Exercise": "count"}).reset_index()
    fig = calplot(
        days,
        x="Date",
        y="Exercise",
        colorscale="greens",
        years_title=True,
        showscale=True
    )
    fig.update_layout(width=None)
    return fig


def get_highlights(column: str) -> dict:
    df = load_data(constants.FITBIT_URL)
    return {
        "min": df[column].min(), 
        "max": df[column].max(),
        "mean": df[column].mean(),
        "median": df[column].median()
    }
