import datetime
import subprocess
import time


import base64
import dash
import requests
from dash import dcc, html, Input, Output, State, callback


# Start FastAPI server if not already running
def start_backend():
    try:
        response = requests.get("http://localhost:8000")
        if response.status_code == 200:
            print("Backend is already running.")
            return
    except requests.exceptions.ConnectionError:
        print("Starting backend...")
        subprocess.Popen(["uvicorn", "BackEndService.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
        time.sleep(2)  # Give it time to start

start_backend()

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
    ]),
    html.Div([
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
        html.Button("Submit", id="submit-btn"),
        html.Div(id="runner-outputs"),
    ]),
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
        multiple=False,
    ),
    html.Br(),
    html.Img(id="image-preview", style={"maxWidth": "300px"}),
    html.Div(id="upload-status"),
    # html.Div(id="image-upload-outputs"),
])


# integrating with backend!
@callback(
    Output("runner-outputs", "children"),
    Input("submit-btn", "n_clicks"),
    *[State("input_{}".format(field_name), "value") for field_name, field_type in RUNNER_INPUT_FIELDS.items()],
    prevent_initial_call=True
)
def send_request(n_clicks, *inputs):
    payload = {field_name: value for field_name, value in zip(RUNNER_INPUT_FIELDS.keys(), inputs)}
    response = requests.post("http://localhost:8000/submit-data", json=payload)
    return response.json().get("message", "No message returned from server.")



@app.callback(
    Output("upload-status", "children"),
    Output("image-preview", "src"),
    Input("upload-image", "contents"),
    State("upload-image", "filename"),
    prevent_initial_call=True
)
def upload_image(contents, filename):
    if contents is not None:
        # Decode the image from Dash
        _, content_string = contents.split(',')
        image_data = base64.b64decode(content_string)

        # Send image to backend
        files = {"file": (filename, image_data, "image/png")}
        response = requests.post("http://localhost:8000/upload", files=files)

        if response.status_code == 200:
            return "Upload Successful!", contents
        else:
            return "Upload Failed!", None

# # parse image upload contents
# def parse_contents(contents, filename, date):
#     return html.Div([
#         html.H5(filename),
#         html.H6(datetime.datetime.fromtimestamp(date)),
#
#         # HTML images accept base64 encoded strings in the same format
#         # that is supplied by the upload
#         html.Img(src=contents),
#         html.Hr(),
#         html.Div('Raw Content'),
#         html.Pre(contents[0:200] + '...', style={
#             'whiteSpace': 'pre-wrap',
#             'wordBreak': 'break-all'
#         })
#     ])
#
#


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
