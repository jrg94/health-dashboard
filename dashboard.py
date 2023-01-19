import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.io as pio
from dash import Input, Output, callback, dcc, html

import callbacks
from layouts import home_layout, intellectual_layout, physical_layout

TRC_LOGO = "https://avatars.githubusercontent.com/u/42280715"
pio.templates[pio.templates.default].layout.colorway = px.colors.qualitative.G10

# App initialization
app = dash.Dash(
    __name__,
    title="Grifski Wellness Dashboard",
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
                [html.Div("Physical")],
                href="/physical-wellness",
                active="exact",
            )
        ),
        dbc.NavItem(
            dbc.NavLink(
                [html.Div("Intellectual")],
                href="/intellectual-wellness",
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
                dbc.NavbarBrand("Grifski Wellness Dashboard", className="ms-2")
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
    html.Div(id="page-content")
])


@callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/":
        return home_layout
    elif pathname == "/physical-wellness":
        return physical_layout
    elif pathname == "/intellectual-wellness":
        return intellectual_layout
    else:
        return "404"


if __name__ == '__main__':
    app.run_server(debug=True)
