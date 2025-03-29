import datetime

import dash
from dash import dcc, html, Input, Output, State, callback

# STATIC OPTIONS
USER_TYPES = ["runner", "photographer"]
RUNNER_INPUT_FIELDS = {
    "race_name": "text",
    "bib_number": "number",
}
PHOTOGRAPHER_INPUT_FIELDS = {
    "race_name": "text",
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
            id='user-type-selector',
            options=[{'label': user_type.capitalize(), 'value': user_type} for user_type in USER_TYPES],
            value=USER_TYPES[0],
            clearable=False
        )
    ]),
    html.Div(id='dynamic-layout'),
])


# pick layout dynamically
@callback(
    Output('dynamic-layout', 'children'),
    Input('user-type-selector', 'value')
)
def update_layout(selected_layout):
    if selected_layout == "runner":
        return html.Div([
            html.H1("Input your information:"),
            *[
                dcc.Input(
                    id="input_{}".format(field_name),
                    type=field_type,
                    placeholder="input type {}".format(field_type),
                )
                for field_name, field_type in RUNNER_INPUT_FIELDS.items()
            ],
            html.Br(),
            html.Div(id="runner-outputs"),
        ]),
    elif selected_layout == 'photographer':
        return html.Div([
            html.H1("Input your information:"),
            *[
                dcc.Input(
                    id="input_{}".format(field_name),
                    type=field_type,
                    placeholder="input type {}".format(field_type),
                )
                for field_name, field_type in PHOTOGRAPHER_INPUT_FIELDS.items()
            ],
            html.Br(),
            dcc.Upload(
                id='upload-image',
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            html.Br(),
            html.Div(id="photographer-outputs"),
            html.Br(),
            html.Div(id="image-upload-outputs"),
        ]),
    else:
        return html.Div()  # Default empty layout


# render the input values to screen
@callback(
    Output("runner-outputs", "children"),
    [Input("input_{}".format(field_name), "value") for field_name, field_type in RUNNER_INPUT_FIELDS.items()], suppress_callback_exceptions=True
)
def render_runner_outputs(*vals):
    return " | ".join((str(val) for val in vals if val))


@callback(
    Output("photographer-outputs", "children"),
    [Input("input_{}".format(field_name), "value") for field_name, field_type in PHOTOGRAPHER_INPUT_FIELDS.items()], suppress_callback_exceptions=True
)
def render_photographer_outputs(*vals):
    return " | ".join((str(val) for val in vals if val))


# parse image upload contents
def parse_contents(contents, filename, date):
    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        # HTML images accept base64 encoded strings in the same format
        # that is supplied by the upload
        html.Img(src=contents),
        html.Hr(),
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])


@callback(Output('image-upload-outputs', 'children'),
              Input('upload-image', 'contents'),
              State('upload-image', 'filename'),
              State('upload-image', 'last_modified'))
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
