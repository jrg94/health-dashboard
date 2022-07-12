import datetime

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from constants import *
from dash import Input, Output, callback, dcc, html
from plotly_calplot import calplot

dash.register_page(__name__, path="/")

# Load data
df = pd.read_csv("dashboard/data/exercises.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Volume"] = df["Weight"] * df["Total Reps"]
df["Projected 1RM"] = df["Weight"] * (1 + (df["Reps"] / 30))

# Plots
days = df.groupby("Date").agg({"Exercise": "count"}).reset_index()
fig2 = calplot(days, x="Date", y="Exercise",
               colorscale="blues", years_title=True)

layout = html.Div([
    html.H2("Lift Volume"),
    html.P(
        """
      For the sake of tracking, I define lift volume as the weight of the lift multiplied by 
      the number of total reps across all sets. Volumes are computed for all exercises and
      are grouped by muscle below. 
      """
    ),
    dbc.Spinner(
        dbc.Accordion(id="exercise-volume-over-time", class_name="pb-3"),
        color="primary",
        type="grow",
        size="md"
    ),
    html.H2("Projected One Rep Maximum"),
    html.P(
        """
      Projected 1RM is computed by using the standard 1RM formula to
      determine the maximum amount of weight you could probably lift. 
      This is a more useful metric for tracking progress than volume
      because it gives you a better idea how how you're building muscle.
      Plots are still somewhat erratic because I don't always lift to
      failure. 
      """
    ),
    dbc.Spinner(
        dbc.Accordion(id="1rm-over-time", class_name="pb-3"),
        color="primary",
        type="grow",
        size="md"
    ),
    html.H2("Calendar View"),
    html.P(
        """
      This is a quick calendar view of all my workouts. The heatmaps show days where 
      I did less or more workouts. I borrowed this figure from calplot. I don't really
      love it since I can't figure out how to make it dynamic. That said, it gets the job done.
      """
    ),
    dcc.Graph(figure=fig2),
])


@callback(
    Output("exercise-volume-over-time", "children"),
    Input("dropdown", "value")
)
def update_exercise_volume(dropdown_value):
    items = []
    curr = df
    if dropdown_value == "Last Three Months":
        curr = df[df["Date"] >= datetime.date.today() -
                  pd.offsets.MonthBegin(3)]
    for muscle in sorted(curr["Muscle Groups"].unique()):
        children = []
        children.append(html.H3(muscle))
        children.append(html.P(descriptions.get(muscle, "")))
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
                    title="Lift Volume by Muscle Group: All Time",
                    category_orders=display_order,
                    markers=True,
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
    curr = df
    if dropdown_value == "Last Three Months":
        curr = df[df["Date"] >= datetime.date.today() -
                  pd.offsets.MonthBegin(3)]
    for muscle in sorted(curr["Muscle Groups"].unique()):
        children = []
        children.append(html.H3(muscle))
        children.append(html.P(descriptions.get(muscle, "")))
        curr_muscle = curr[curr["Muscle Groups"] == muscle]
        display_order = {"Exercise": sorted(curr_muscle["Exercise"].unique())}
        children.append(
            dcc.Graph(
                figure=px.line(
                    curr_muscle,
                    x="Date",
                    y="Projected 1RM",
                    color="Exercise",
                    title="Projected 1RM by Muscle Group: All Time",
                    category_orders=display_order,
                    markers=True,
                )
            )
        )
        items.append(dbc.AccordionItem(children, title=muscle))
    return items
