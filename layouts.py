import datetime

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import dcc, html
from plotly_calplot import calplot
from constants import WEIGHTLIFTING_URL

import utils

# Load data
df = utils.load_data(WEIGHTLIFTING_URL)

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
    colorscale="greens",
    years_title=True,
    showscale=True
)
fig2.update_layout(width=None)

home_layout = html.Div([
    html.H2("Home"),
    html.P(
        """
        Here on the homepage, you can find quick links to the various health and fitness pages.
        """
    ),
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Lifting"),
                        dbc.CardBody(
                            [
                                html.P(
                                    """
                                    During the week, I try to get a lift in. Check out the
                                    lifting page for all the pretty pictures I make to track
                                    my progress.
                                    """
                                ),
                                dbc.Button("Learn More", href="/lifting"),
                            ]
                        )
                    ],
                    color="light"         
                ),
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Fitbit"),
                        dbc.CardBody(
                            [
                                html.P(
                                    """
                                    One of the devices I use to track my health is the Fitbit.
                                    I've been using one since 2015, so there's tons of useful
                                    data I can track like weight, steps, and calories. Use the
                                    link below to see some pretty pictures of my Fitbit data.
                                    """  
                                ),
                                dbc.Button("Learn More", href="/fitbit"),
                            ]
                        )
                    ],
                    color="light"
                )
            )
        ]
    )
])

lifting_layout = html.Div(
    [
        html.H2("Exercise Sets and Reps"),
        html.P
        (
            """
                This section is just bookkeeping for me. It's hard to remember how much weight I did
                last, so I made plots of the individual exercise by set and rep. Also, to help myself
                out, I track my muscle fatigue on a 48-hour interval. It's a bit rudimentary, but 
                basically I compute a ratio of muscle group volume (sum) against the projected 1RM 
                (mean). This is a pretty sloppy metric since I don't find 1RM very accurate and the 
                aggregate functions are somewhat misleading, but I don't really think it needs to be 
                that accurate. Regardless, it's not like I have a scientific way of assessing fatique 
                anyway.
                """
        ),
        dbc.Spinner(
            [
                dcc.Graph(figure=fig),
                dbc.Accordion(
                    id="exercise-sets-reps",
                    class_name="pb-3", 
                    style={"minHeight": "60px"}
                ),
            ],
            color="primary",
            spinner_style={"height": "50px", "width": "50px"}
        ),
        html.H2("Lift Volume"),
        html.P(
            """
            For the sake of tracking, I define lift volume as the weight of the lift multiplied by 
            the number of total reps across all sets. Volumes are computed for all exercises and
            are grouped by muscle below. Given the noisiness of the data, I use a pretty relaxed
            fit line to show the overall trends of the data (lowess=default). If you're interested in
            a quick overview of the data, I summed the volumes for every single exercise below.
            Colors are obviously duplicated, but you can double click the legend to single any
            one exercise out. 
            """
        ),
        dbc.Spinner(
            [
                dcc.Graph(id="volume-overview"),
                dbc.Accordion(
                    id="exercise-volume-over-time",
                    class_name="pb-3",
                    style={"min-height": "60px"}
                )
            ],
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
            failure, so I opted for an expanding maximum trendline which is a 
            line that basically always trends up. That way, easy days don't 
            affect my actual projected 1RM. In reality, the trendline represents 
            my peak 1RM, so it's not something I'd ever attempt. As with volume,
            there's also a quick overview plot here. Same rules apply. Only
            difference is that the points are maxed rather than summed.
            """
        ),
        dbc.Spinner(
            [
                dcc.Graph(id="projected-1rm-overview"),
                dbc.Accordion(
                    id="1rm-over-time", 
                    class_name="pb-3",
                    style={"minHeight": "60px"}
                )
            ],
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
    ]
)

fitbit_layout = html.Div(
    [
        html.H2("Steps"),
        html.P(
            """
            To no one's surprise, the primary use of a Fitbit is to track steps.
            As someone who has been wearing one since 2015, you can really see how
            my trend in activities changes over time. 
            """
        ),
        dbc.Spinner(
            dcc.Graph(id="steps-overview"),
        )
    ]
)
