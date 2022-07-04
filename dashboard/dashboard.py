import datetime
import dash
import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output
from plotly_calplot import calplot

# App initialization
app = dash.Dash(
  __name__,
  title="Health Dashboard"
)

# Special line of code for Heroku
server = app.server

# Load data
df = pd.read_csv("dashboard/data/exercises.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Volume"] = df["Weight"] * df["Total Reps"]
df["Projected 1RM"] = df["Weight"] * (1 + (df["Reps"] / 30))

# Plots
fatigue = df[df["Date"] >= datetime.date.today() - pd.offsets.Day(2)] \
  .groupby("Muscle Groups") \
  .agg({"Volume": "sum", "Projected 1RM": "mean"})
missing = set(df["Muscle Groups"].unique()) - set(fatigue.index)
fatigue["Cumulative Volume / Average Project 1RM"] = fatigue["Volume"] / fatigue["Projected 1RM"]
for muscle in missing:
  fatigue.loc[muscle] = 0
fatigue = fatigue.sort_values("Cumulative Volume / Average Project 1RM", ascending=True)
fig = px.bar(fatigue, y="Cumulative Volume / Average Project 1RM")

days = df.groupby("Date").agg({"Exercise": "count"}).reset_index()
fig2 = calplot(days, x="Date", y="Exercise", colorscale="blues", years_title=True)

def exercise_sets_reps(df):
  exercise_plots = []
  for exercise in sorted(df["Exercise"].unique()):
    curr_exercise = df[df["Exercise"] == exercise]
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

# App layout
app.layout = html.Div([
    html.H1("Health Dashboard"),
    html.P(
        """
        Welcome to my Health Dashboard. I use this space to track my health and fitness progress
        using pretty pictures. Use the dropdown to pick a window of time besides "All Time".
        """
    ),
    dcc.Dropdown(["All Time", "Last Three Months"], "All Time", id="dropdown"),
    html.H2("Lift Volume"),
    html.P(
      """
      For the sake of tracking, I define lift volume as the weight of the lift multiplied by 
      the number of total reps across all sets. Volumes are computed for all exercises and
      are grouped by muscle below. 
      """
    ),
    dcc.Graph(id="exercise-volume-over-time", className="custom-height"),
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
    dcc.Graph(id="1rm-over-time", className="custom-height"),
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
    html.H2("Calendar View"),
    html.P(
      """
      This is a quick calendar view of all my workouts. The heatmaps show days where 
      I did less or more workouts. I borrowed this figure from calplot. I don't really
      love it since I can't figure out how to make it dynamic. That said, it gets the job done.
      """
    ),
    dcc.Graph(figure=fig2),
    html.H2("Exercise Sets and Reps"),
    html.P(
      """
      This last section is just bookkeeping for me. It's hard to remember how much weight I did
      last, so I made plots of the individual exercise by set and rep.
      """
    ),
    html.Div(exercise_sets_reps(df))
])

@app.callback(
  Output("exercise-volume-over-time", "figure"),
  Input("dropdown", "value")
)
def update_exercise_volume(dropdown_value):
  display_order = {"Muscle Groups": sorted(df["Muscle Groups"].unique()), "Exercise": sorted(df["Exercise"].unique())}
  if dropdown_value == "Last Three Months":
    last_three_months = df[df["Date"] >= datetime.date.today() - pd.offsets.MonthBegin(3)]
    return px.line(
      last_three_months, 
      x="Date", 
      y="Volume", 
      color="Exercise", 
      facet_col="Muscle Groups", 
      facet_col_wrap=2, 
      title="Lift Volume by Muscle Group: Last Three Months",
      category_orders=display_order
    )
  return px.line(
    df, 
    x="Date", 
    y="Volume", 
    color="Exercise", 
    facet_col="Muscle Groups", 
    facet_col_wrap=2, 
    title="Lift Volume by Muscle Group: All Time",
    category_orders=display_order
  )

@app.callback(
  Output("1rm-over-time", "figure"),
  Input("dropdown", "value")
)
def update_1rm(dropdown_value):
  if dropdown_value == "Last Three Months":
    last_three_months = df[df["Date"] >= datetime.date.today() - pd.offsets.MonthBegin(3)]
    return px.line(
      last_three_months, 
      x="Date", 
      y="Projected 1RM", 
      color="Exercise", 
      facet_col="Muscle Groups", 
      facet_col_wrap=2, 
      title="Projected 1RM by Muscle Group: Last Three Months"
    )
  return px.line(
    df, 
    x="Date", 
    y="Projected 1RM", 
    color="Exercise", 
    facet_col="Muscle Groups", 
    facet_col_wrap=2, 
    title="Projected 1RM by Muscle Group: All Time"
  )


if __name__ == '__main__':
  app.run_server(debug=True)
