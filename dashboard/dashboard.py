import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from constants import *


# App initialization
app = dash.Dash(
    __name__,
    title="Health Dashboard",
    use_pages=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
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
                [
                    html.Div(page["name"],
                             className="ms-2"),
                ],
                href=page["path"],
                active="exact",
            )
        )
        for page in dash.page_registry.values()
    ],
    pills=True,
)

logo = html.A(
    dbc.Row(
        [
            dbc.Col(html.Img(src=TRC_LOGO, height="30px")),
            dbc.Col(dbc.NavbarBrand(
                "Grifski Health Dashboard", className="ms-2")),
        ],
        align="center",
        className="g-0",
    ),
    href="https://jeremygrifski.com",
    style={"textDecoration": "none"},
)

# App layout
app.layout = dbc.Container([
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
    dash.page_container
])

if __name__ == '__main__':
    app.run_server(debug=True)
