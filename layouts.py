import dash_bootstrap_components as dbc
from dash import dcc, html

import utils

home_layout = html.Div([
    html.H1("Grifski Wellness Dashboard"),
    html.P(
        """
        Welcome to my wellness dashboard. I use this space to track my wellness goals
        using pretty pictures. Below, you can find quick links to the various wellness domains
        as defined by OSU's Nine Dimensions of Wellness.
        """
    ),    
    dbc.Row(
        [
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Physical Wellness"),
                        dbc.CardBody(
                            [
                                html.P(
                                    """
                                    OSU's Nine Dimensions of Wellness outlines physical wellness
                                    as the following: "The physically well person gets an adequate 
                                    amount of sleep, eats a balanced and nutritious diet, engages 
                                    in exercise for 150 minutes per week, attends regular medical 
                                    check-ups and practices safe and healthy sexual relations."
                                    In this domain, I track all of my health related metrics
                                    such as exercise and weight.
                                    """
                                ),
                                dbc.Button("Learn More", href="/physical-wellness"),
                            ]
                        )
                    ],
                ),
            ),
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader("Intellectual Wellness"),
                        dbc.CardBody(
                            [
                                html.P(
                                    """
                                    TBD.
                                    """
                                ),
                                dbc.Button("Learn More", href="/intellectual-wellness"),
                            ]
                        )
                    ],
                )
            )
        ]
    )
])

physical_layout = html.Div(
    [
        html.H1("Physical Wellness"),
        html.P(
            """
            Welcome to the physical wellness page! Feel free to use the dropdown to pick a 
            window of time besides "All Time" to filter the various time series plots.
            """
        ),
        html.H2("Table of Contents"),
        html.Ol([
            html.Li(html.A("Highlights", href="#highlights")),
            html.Li(html.A("Exercise", href="#exercise")),
            html.Ol([
                html.Li(html.A("Exercise Sets and Reps", href="#exercise-sets-and-reps")),
                html.Li(html.A("Lift Volume", href="#lift-volume")),
                html.Li(html.A("Projected One Rep Maximum", href="#projected-1rm")),
                html.Li(html.A("Workout History", href="#workout-history")),
            ]),
            html.Li(html.A("Health", href="#health")),
            html.Ol([
                html.Li(html.A("Steps", href="#steps")),
                html.Li(html.A("Weight", href="#weight")),
                html.Li(html.A("Sleep", href="#sleep")),
            ])
        ]),
        html.H2(f"{utils.get_number_of_records():,} Days of Highlights", id="highlights"),
        dbc.CardGroup(
            [
                utils.create_highlight_card("Steps", "steps / day", "Steps Highlights"),
                utils.create_highlight_card("Weight", "lbs", "Weight Highlights"),
                utils.create_highlight_card("Total Sleep (minutes)", "minutes", "Sleep Highlights"),
                utils.create_highlight_card("Resting Heart Rate", "bpm", "Resting Heart Rate Highlights"),
            ],
            className="pb-2 pt-2",
        ),
        html.H2("Exercise", id="exercise"),
        html.P(
            """
            One of the core components of physical wellness is exercise. As a result, I've
            decided to track a bit of my own exercise here. The bulk of it is lifting, but
            there are some cardio exercises as well.
            """
        ),
        html.H3("Exercise Sets and Reps", id="exercise-sets-and-reps"),
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
                dcc.Graph(figure=utils.create_fatique_plot()),
                dbc.Accordion(
                    id="exercise-sets-reps",
                    class_name="pb-3",
                    style={"minHeight": "60px"}
                ),
            ],
            color="primary",
            spinner_style={"height": "50px", "width": "50px"}
        ),
        html.H3("Lift Volume", id="lift-volume"),
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
        html.H3("Projected One Rep Maximum", id="projected-1rm"),
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
        html.H3("Workout History", id="workout-history"),
        html.P(
            """
            This is a quick calendar view of all my workouts. The heatmaps show days where 
            I did less or more workouts. I borrowed this figure from calplot. I don't really
            love it since I can't figure out how to make it dynamic. That said, it gets the job done.
            """
        ),
        dcc.Graph(figure=utils.create_calendar_plot()),
        html.H2("Health", id="health"),
        html.P(
            """
            Broadly speaking, another major aspect of physical wellness is overall health.
            Here, I track weight, body fat, sleep, steps, and heart rate metrics.
            """    
        ),
        html.H3("Steps", id="steps"),
        html.P(
            """
            To no one's surprise, the primary use of a Fitbit is to track steps.
            As someone who has been wearing one since 2015, you can really see how
            my trend in activities changes over time. To get a better feel for the
            data, I use a rolling mean of 30 days. It gives a nice "monthly" trend
            line. 
            """
        ),
        dbc.Spinner(
            [
                dcc.Graph(id="steps-overview"),
            ],
            color="primary",
            spinner_style={"height": "50px", "width": "50px"}
        ),
        html.H3("Weight", id="weight"),
        html.P(
            """
            For a few years now, I've been tracking my weight on and off with a bluetooth
            scale. The results of those measurements can be found here. One thing that would
            be cool to do would be to mark off signficant events on the timeline to show
            when and why changes occured.
            """
        ),
        dbc.Spinner(
            [
                dcc.Graph(id="weight-overview"),
                dcc.Graph(id="weight-histogram")
            ],
            color="primary",
            spinner_style={"height": "50px", "width": "50px"}
        ),
        html.H3("Sleep", id="sleep"),
        html.P(
            """
            One of the perks of using a FitBit for so long is that I also can track my sleep.
            It seems as I get older, I sleep more—at least for now. We'll see what happens when
            I start to have kids.
            """
        ),
        dbc.Spinner(
            [
                dcc.Graph(id="sleep-overview"),
            ],
            color="primary",
            spinner_style={"height": "50px", "width": "50px"}
        )
    ]
)


intellectual_layout = html.Div(
    html.P("TBD")
)
