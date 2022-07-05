import datetime
import dash
from dash import html, dcc, callback, Input, Output
import pandas as pd
import plotly.express as px


dash.register_page(__name__)

# Load data
df = pd.read_csv("dashboard/data/exercises.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Volume"] = df["Weight"] * df["Total Reps"]
df["Projected 1RM"] = df["Weight"] * (1 + (df["Reps"] / 30))

# Create plots
fatigue = df[df["Date"] >= datetime.date.today() - pd.offsets.Day(2)] \
  .groupby("Muscle Groups") \
  .agg({"Volume": "sum", "Projected 1RM": "mean"})
missing = set(df["Muscle Groups"].unique()) - set(fatigue.index)
fatigue["Cumulative Volume / Average Project 1RM"] = fatigue["Volume"] / fatigue["Projected 1RM"]
for muscle in missing:
  fatigue.loc[muscle] = 0
fatigue = fatigue.sort_values("Cumulative Volume / Average Project 1RM", ascending=True)
fig = px.bar(fatigue, y="Cumulative Volume / Average Project 1RM")

# Setup layout
layout = html.Div([
    html.H2("Muscle Fatigue"),
    html.P(
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
    html.H2("Exercise Sets and Reps"),
    html.P(
      """
      This last section is just bookkeeping for me. It's hard to remember how much weight I did
      last, so I made plots of the individual exercise by set and rep.
      """
    ),
    html.Div(id="exercise-sets-reps"),
])

@callback(
  Output("exercise-sets-reps", "children"),
  Input("dropdown", "value")
)
def update_exercise_sets_reps(dropdown_value):
  exercise_plots = []
  curr = df
  if dropdown_value == "Last Three Months":
    curr = df[df["Date"] >= datetime.date.today() - pd.offsets.MonthBegin(3)]
  for muscle in sorted(curr["Muscle Groups"].unique()):
    exercise_plots.append(html.H3(muscle))
    curr_muscle = curr[curr["Muscle Groups"] == muscle]
    for exercise in sorted(curr_muscle["Exercise"].unique()):
      curr_exercise = curr_muscle[curr_muscle["Exercise"] == exercise]
      figure = px.line(
        curr_exercise, 
        x="Date", 
        y="Weight", 
        facet_col="Sets", 
        color="Reps",
        title=exercise,
        category_orders={
          "Sets": sorted(curr_exercise["Sets"].unique()), # Ensures only existing sets are shown
          "Reps": sorted(df["Reps"].unique()) # Ensures colors are constant between plots
        },
        markers=True
      )
      exercise_plots.append(dcc.Graph(figure=figure))
  return exercise_plots
