import datetime

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Input, Output, callback, dcc, html

descriptions = {
    "Back":
        """
        To me, the back is a generic muscle group mainly referring to the traps. 
        """,
    "Dumbbell Rows":
        """
        Dumbell rows are traditional rows that are performed bent over using a single arm at a time,
        at least that's how I do them. In short, I usually just bend down with one hand on a
        surface and the other pulling the weight toward me from the ground.
        """,
}

dash.register_page(__name__)

# Load data
df = pd.read_csv("https://raw.githubusercontent.com/jrg94/personal-data/main/health/weight-lifting.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Volume"] = df["Weight"] * df["Total Reps"]
df["Projected 1RM"] = df["Weight"] * (1 + (df["Reps"] / 30))

# Create plots
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
fatigue = fatigue.sort_values(
    "Cumulative Volume / Average Project 1RM", ascending=True)
fig = px.bar(fatigue, y="Cumulative Volume / Average Project 1RM")

# Setup layout
layout = html.Div(
    [
        html.H2("Exercise Sets and Reps"),
        html.P
        (
            """
            This last section is just bookkeeping for me. It's hard to remember how much weight I did
            last, so I made plots of the individual exercise by set and rep.
            """
        ),
        dbc.Spinner(
            dbc.Accordion(id="exercise-sets-reps",
                          class_name="pb-3", style={"min-height": "60px"}),
            color="primary",
            spinner_style={"height": "50px", "width": "50px"}
        ),
        html.H2("Muscle Fatigue"),
        html.P
        (
            """
            Muscle fatigue is a metric that I use to track how much muscle I've used in the
            past 48 hours. It's a bit rudimentary, but basically I compute a ratio of muscle 
            group volume (sum) against the projected 1RM (mean). This is a pretty sloppy metric 
            since I don't find 1RM very accurate and the aggregate functions are somewhat misleading, 
            but I don't really think it needs to be that accurate. Regardless, it's not like I have
            a scientific way of assessing fatique anyway.
            """
        ),
        dcc.Graph(figure=fig),
    ]
)


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
    )
    return figure


@callback(Output("exercise-sets-reps", "children"), Input("dropdown", "value"))
def update_exercise_sets_reps(dropdown_value):
    items = []
    curr = time_filter(df, dropdown_value)
    for muscle in sorted(curr["Muscle Groups"].unique()):
        children = []
        children.append(html.H3(muscle))
        children.append(html.P(descriptions.get(muscle, "")))
        curr_muscle = curr[curr["Muscle Groups"] == muscle]
        for exercise in sorted(curr_muscle["Exercise"].unique()):
            curr_exercise = curr_muscle[curr_muscle["Exercise"] == exercise]
            children.append(html.H4(exercise))
            children.append(html.P(descriptions.get(exercise, "")))
            difficulty = curr_exercise["Difficulty"].iloc[-1]
            sets = curr_exercise["Sets"].iloc[-1]
            reps = curr_exercise["Reps"].iloc[-1]
            weight = curr_exercise["Weight"].iloc[-1]
            children.append(
                html.P(
                    [
                        f"Last time I did a set (",
                        html.B(f"{sets}x{reps}x{weight}"),
                        "), I described it as ",
                        html.B(f"{difficulty}"),
                        ".",
                    ]
                )
            )
            figure = plot_exercise_sets_reps(
                df,
                dropdown_value,
                muscle,
                exercise
            )
            children.append(dcc.Graph(figure=figure))
        items.append(dbc.AccordionItem(children=children, title=muscle))
    return items
