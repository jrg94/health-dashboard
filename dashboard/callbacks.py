import datetime
from dash import Input, Output, callback, dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import utils

# Declare global data
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


@callback(
    Output("exercise-volume-over-time", "children"),
    Input("dropdown", "value")
)
def update_exercise_volume(dropdown_value):
    items = []
    curr = utils.load_data()
    if dropdown_value == "Last Three Months":
        curr = curr[
            curr["Date"] >= datetime.date.today() - pd.offsets.MonthBegin(3)
        ]
    for muscle in sorted(curr["Muscle Groups"].unique()):
        children = []
        children.append(html.H3(muscle))
        curr_muscle = curr[curr["Muscle Groups"] == muscle]
        display_order = {"Exercise": sorted(curr_muscle["Exercise"].unique())}
        children.append(
            dcc.Graph(
                id=f"{muscle}-volume-over-time",
                figure=px.line(
                    curr_muscle,
                    x="Date",
                    y="Volume",
                    color="Exercise",
                    title=f"Lift Volume by Muscle Group: {dropdown_value}",
                    category_orders=display_order,
                    markers=True,
                    symbol="Per Arm"
                )
            )
        )
        items.append(
            dbc.AccordionItem(children, title=muscle)
        )
    return items


@callback(
    Output("1rm-over-time", "children"),
    Input("dropdown", "value")
)
def update_1rm(dropdown_value):
    items = []
    curr = utils.load_data()
    if dropdown_value == "Last Three Months":
        curr = curr[
            curr["Date"] >= datetime.date.today() - pd.offsets.MonthBegin(3)
        ]
    for muscle in sorted(curr["Muscle Groups"].unique()):
        children = []
        children.append(html.H3(muscle))
        curr_muscle = curr[curr["Muscle Groups"] == muscle]
        display_order = {"Exercise": sorted(curr_muscle["Exercise"].unique())}
        children.append(
            dcc.Graph(
                figure=px.line(
                    curr_muscle,
                    x="Date",
                    y="Projected 1RM",
                    color="Exercise",
                    title=f"Projected 1RM by Muscle Group: {dropdown_value}",
                    category_orders=display_order,
                    markers=True,
                    symbol="Per Arm"
                )
            )
        )
        items.append(dbc.AccordionItem(children, title=muscle))
    return items


@callback(
    Output("exercise-sets-reps", "children"), 
    Input("dropdown", "value")
)
def update_exercise_sets_reps(dropdown_value):
    items = []
    df = utils.load_data()
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
