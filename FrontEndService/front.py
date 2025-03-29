import dash
from dash import dcc, html, Input, Output, callback

# STATIC OPTIONS
USER_TYPES = ["runner", "photographer"]
RUNNER_INPUT_FIELDS = {
    "race_name": "text",
    "bib_number": "number",
}

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server  # For deployment

# App layout
app.layout = html.Div([
    html.Div([
        html.H1("Race Photo Tracker"),
        html.Label("Select a user type:"),
        dcc.Dropdown(
            id='category-dropdown',
            options=[{'label': user_type, 'value': user_type.capitalize()} for user_type in USER_TYPES],
            value=USER_TYPES[0],
            clearable=False
        ),
        html.H1("Input your information:"),
        *[
            dcc.Input(
                id="input_{}".format(field_name),
                type=field_type,
                placeholder="input type {}".format(field_type),
            )
            for field_name, field_type in RUNNER_INPUT_FIELDS.items()
        ],
    ]),
    html.Div(id="out-all-types"),
])

# Callbacks
@callback(
    Output("out-all-types", "children"),
    [Input("input_{}".format(field_name), "value") for field_name, field_type in RUNNER_INPUT_FIELDS.items()],
)
def cb_render(*vals):
    return " | ".join((str(val) for val in vals if val))


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
