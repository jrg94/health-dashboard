import datetime
import dash
import pandas as pd
import plotly.express as px
from dash import html, dcc

# App initialization
app = dash.Dash(
  __name__,
  title="Dashboard Template"
)

# Special line of code for Heroku
server = app.server

# Load data
df = pd.read_csv("dashboard/data/exercises.csv")
df["Date"] = pd.to_datetime(df["Date"])
df["Volume"] = df["Weight"] * df["Total Reps"]
df["Projected 1RM"] = df["Weight"] * (1 + (df["Reps"] / 30))

# Create plot
fig = px.line(df, x="Date", y="Volume", color="Exercise", facet_col="Muscle Groups", facet_col_wrap=2, title="Lift Volume by Exercise Over Time")
fig2 = px.line(df, x="Date", y="Projected 1RM", color="Exercise", facet_col="Muscle Groups", facet_col_wrap=2, title="Projected 1RM by Exercise Over Time")
last_three_months = df[df["Date"] >= datetime.date.today() - pd.offsets.MonthBegin(3)]
fig3 = px.line(last_three_months, x="Date", y="Volume", color="Exercise", facet_col="Muscle Groups", facet_col_wrap=2, title="Lift Volume by Exercise Over Last Three Months")
fig4 = px.line(last_three_months, x="Date", y="Projected 1RM", color="Exercise", facet_col="Muscle Groups", facet_col_wrap=2, title="Projected 1RM by Exercise Over Last Three Months")

# App layout
app.layout = html.Div([
    html.H1("Dashboard Template"),
    html.P(
        """
        Welcome to The Renegade Coder template for Dash apps!
        Place your HTML here to create your own dashboard. 
        Make use of the graphs component of dcc to load Plotly
        graphs. 
        """
    ),
    dcc.Graph(className="custom-height", figure=fig),
    dcc.Graph(className="custom-height", figure=fig2),
    dcc.Graph(className="custom-height", figure=fig3),
    dcc.Graph(className="custom-height", figure=fig4)
])

if __name__ == '__main__':
  app.run_server(debug=True)
