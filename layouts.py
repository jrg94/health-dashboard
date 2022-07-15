import datetime

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc, html
from plotly_calplot import calplot

import utils

# Load data
df = utils.load_data()

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
    fatigue = fatigue.sort_values(
        "Cumulative Volume / Average Project 1RM", ascending=True)
    fig = px.bar(fatigue, y="Cumulative Volume / Average Project 1RM")

# Home plots
days = df.groupby("Date").agg({"Exercise": "count"}).reset_index()
fig2 = calplot(
    days,
    x="Date",
    y="Exercise",
    colorscale="blues",
    years_title=True
)

home_layout = html.Div([
    html.H2("Lift Volume"),
    html.P(
        """
        For the sake of tracking, I define lift volume as the weight of the lift multiplied by 
        the number of total reps across all sets. Volumes are computed for all exercises and
        are grouped by muscle below. 
        """
    ),
    dbc.Spinner(
        dbc.Accordion(
            id="exercise-volume-over-time",
            class_name="pb-3",
            style={"min-height": "60px"}
        ),
        color="primary",
        spinner_style={"height": "50px", "width": "50px"}
    ),
    html.H2("Projected One Rep Maximum"),
    html.P(
        """
        Projected 1RM is computed by using the standard 1RM formula to
        determine the maximum amount of weight you could probably lift. 
        This is a more useful metric for tracking progress than volume
        because it gives you a better idea how how you're building muscle.
        Plots are still somewhat erratic because I don't always lift to
        failure. To make the chart a bit easier to read, I use an expanding
        maximum which is a line that basically always trends up. That way, 
        easy days don't effect my actual projected 1RM. In reality, the
        trendline represents my peak 1RM, so it's not something I'd ever
        attempt.
        """
    ),
    dbc.Spinner(
        dbc.Accordion(id="1rm-over-time", class_name="pb-3",
                      style={"minHeight": "60px"}),
        color="primary",
        spinner_style={"height": "50px", "width": "50px"}
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

workout_layout = html.Div(
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
                          class_name="pb-3", style={"minHeight": "60px"}),
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
