import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback, Output, Input
from layouts import home_layout, workout_layout
import callbacks

TRC_LOGO = "https://avatars.githubusercontent.com/u/42280715"

# App initialization
app = dash.Dash(
    __name__,
    title="Health Dashboard",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

# Special line of code for Heroku
server = app.server

# Define components
dropdown = dbc.Row(
    [
        dbc.Col(
            [
                dcc.Dropdown(
                    ["All Time", "Last Three Months"],
                    "All Time",
                    id="dropdown"
                ),
            ],
        )
    ],
    className="col-3",
    align="center",
)

navlinks = dbc.Nav(
    [
        dbc.NavItem(
            dbc.NavLink(
                [html.Div("Home")],
                href="/",
                active="exact",
            )
        ),
        dbc.NavItem(
            dbc.NavLink(
                [html.Div("Workout")],
                href="/workout",
                active="exact",
            )
        )
    ],
    pills=True,
)

logo = html.A(
    dbc.Row(
        [
            dbc.Col(html.Img(src=TRC_LOGO, height="30px")),
            dbc.Col(
                    dbc.NavbarBrand("Grifski Health Dashboard", className="ms-2")
            ),
        ],
        align="center",
        className="g-0",
    ),
    href="https://jeremygrifski.com",
    style={"textDecoration": "none"},
)

app.layout = dbc.Container([
    dcc.Location(id="url", refresh=False),
    dbc.Navbar(
        dbc.Container(
            [
                logo,
                navlinks,
                dropdown
            ]
        ),
        color="dark",
        dark="True"
    ),
    html.H1("Health Dashboard"),
    html.P(
        """
            Welcome to my Health Dashboard. I use this space to track my health and fitness progress
            using pretty pictures. Use the dropdown to pick a window of time besides "All Time".
            """
    ),
    html.Div(id="page-content")
])

@callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/":
        return home_layout
    elif pathname == "/workout":
        return workout_layout
    else:
        return "404"

if __name__ == '__main__':
    app.run_server(debug=True)
