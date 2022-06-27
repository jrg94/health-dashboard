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

# Create plot
fig = px.line(df, x="Date", y="Volume", facet_col="Exercise", facet_col_wrap=3)

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
    dcc.Graph(id="custom-height", figure=fig)
])

if __name__ == '__main__':
  app.run_server(debug=True)
