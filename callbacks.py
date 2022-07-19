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
    df = utils.load_data(constants.WEIGHTLIFTING_URL)
    curr = utils.time_filter(df, dropdown_value)
    for muscle in sorted(curr["Muscle Groups"].unique()):
        children = []
        children.append(html.H3(muscle))
        curr_muscle = curr[curr["Muscle Groups"] == muscle]
        display_order = {"Exercise": sorted(curr_muscle["Exercise"].unique())}
        figure = px.scatter(
            curr_muscle,
            x="Date",
            y="Volume",
            color="Exercise",
            title=f"Lift Volume by Muscle Group: {dropdown_value}",
            category_orders=display_order,
            symbol="Per Arm",
            trendline="lowess"
        )
        figure.data = [t for t in figure.data if t.mode == "lines"]
        figure.update_traces(showlegend=True)
        children.append(dcc.Graph(figure=figure))
        items.append(dbc.AccordionItem(children, title=muscle))
    return items


@callback(
    Output("1rm-over-time", "children"),
    Input("dropdown", "value")
)
def update_1rm(dropdown_value):
    items = []
    df = utils.load_data(constants.WEIGHTLIFTING_URL)
    curr = utils.time_filter(df, dropdown_value)
    for muscle in sorted(curr["Muscle Groups"].unique()):
        children = []
        children.append(html.H3(muscle))
        curr_muscle = curr[curr["Muscle Groups"] == muscle]
        display_order = {"Exercise": sorted(curr_muscle["Exercise"].unique())}
        figure = px.scatter(
            curr_muscle,
            x="Date",
            y="Projected 1RM",
            color="Exercise",
            title=f"Projected 1RM by Muscle Group: {dropdown_value}",
            category_orders=display_order,
            symbol="Per Arm",
            trendline="expanding",
            trendline_options=dict(function="max")
        )
        figure.data = [t for t in figure.data if t.mode == "lines"]
        figure.update_traces(showlegend=True)
        children.append(dcc.Graph(figure=figure))
        items.append(dbc.AccordionItem(children, title=muscle))
    return items


@callback(
    Output("exercise-sets-reps", "children"),
    Input("dropdown", "value")
)
def update_exercise_sets_reps(dropdown_value):
    items = []
    df = utils.load_data(constants.WEIGHTLIFTING_URL)
    curr = utils.time_filter(df, dropdown_value)
    for muscle in sorted(curr["Muscle Groups"].unique()):
        children = []
        tabs = []
        children.append(html.H3(muscle))
        children.append(html.P(constants.workout_constants.get(
            muscle, {}).get("description", "")))
        curr_muscle = curr[curr["Muscle Groups"] == muscle]
        for exercise in sorted(curr_muscle["Exercise"].unique()):
            tab_children = []
            tab_children.append(html.H4(exercise))
            exercise_constants = constants.workout_constants.get(exercise, {})
            tab_children.append(
                utils.create_video_description_row(exercise_constants))
            figure = utils.plot_exercise_sets_reps(
                df,
                dropdown_value,
                muscle,
                exercise
            )
            tab_children.append(
                utils.create_recent_exercises_table(df, muscle, exercise))
            tab_children.append(dcc.Graph(figure=figure))
            tabs.append(dbc.Tab(tab_children, label=exercise))
        children.append(dbc.Tabs(tabs))
        items.append(dbc.AccordionItem(children=children, title=muscle))
    return items


@callback(
    Output("projected-1rm-overview", "figure"),
    Output("volume-overview", "figure"),
    Input("dropdown", "value")
)
def homepage_overview_plots(dropdown_value):
    df = utils.load_data(constants.WEIGHTLIFTING_URL)
    df = utils.time_filter(df, dropdown_value)
    exercise_groups = df.groupby(["Date", "Exercise"]).agg(
        {"Volume": "sum", "Projected 1RM": "max"}).reset_index()
    fig1 = px.scatter(
        exercise_groups,
        x="Date",
        y="Volume",
        color="Exercise",
        labels={"Volume": "Volume (lbs)"}
    )
    fig2 = px.scatter(
        exercise_groups,
        x="Date",
        y="Projected 1RM",
        color="Exercise",
        labels={"Projected 1RM": "Maximum Projected 1RM (lbs)"}
    )
    return fig2, fig1


@callback(
    Output("steps-overview", "figure"),
    Input("dropdown", "value")
)
def steps_overview_plot(dropdown_value):
    df = utils.load_data(constants.FITBIT_URL)
    df = utils.time_filter(df, dropdown_value)
    fig = px.scatter(
        df,
        x="Date",
        y="Steps",
        trendline="rolling",
        trendline_options=dict(window=30, min_periods=1),
        trendline_color_override=px.colors.qualitative.G10[8]
    )
    return fig

@callback(
    Output("weight-overview", "figure"),
    Output("weight-histogram", "figure"),
    Input("dropdown", "value")
)
def weight_overview_plot(dropdown_value):
    df = utils.load_data(constants.FITBIT_URL)
    df = utils.time_filter(df, dropdown_value)
    df = df.dropna(subset=["Weight"])
    overview = px.scatter(
        df,
        x="Date",
        y="Weight",
        trendline="rolling",
        trendline_options=dict(window=30, min_periods=1),
        trendline_color_override=px.colors.qualitative.G10[8]
    )
    histogram = px.histogram(
        df,
        x="Weight"
    )
    return overview, histogram 
