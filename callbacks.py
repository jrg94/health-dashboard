import dash_bootstrap_components as dbc
import plotly.express as px
from dash import Input, Output, callback, dcc, html

import constants
import utils


@callback(
    Output("exercise-volume-over-time", "children"),
    Input("dropdown", "value")
)
def update_exercise_volume(dropdown_value):
    items = []
    df = utils.load_data()
    curr = utils.time_filter(df, dropdown_value)
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
    df = utils.load_data()
    curr = utils.time_filter(df, dropdown_value)
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
    curr = utils.time_filter(df, dropdown_value)
    for muscle in sorted(curr["Muscle Groups"].unique()):
        children = []
        children.append(html.H3(muscle))
        children.append(html.P(constants.descriptions.get(muscle, "")))
        curr_muscle = curr[curr["Muscle Groups"] == muscle]
        for exercise in sorted(curr_muscle["Exercise"].unique()):
            curr_exercise = curr_muscle[curr_muscle["Exercise"] == exercise]
            children.append(html.H4(exercise))
            children.append(html.P(constants.descriptions.get(exercise, "")))
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
            figure = utils.plot_exercise_sets_reps(
                df,
                dropdown_value,
                muscle,
                exercise
            )
            children.append(dcc.Graph(figure=figure))
        items.append(dbc.AccordionItem(children=children, title=muscle))
    return items
