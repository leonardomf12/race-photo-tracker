import base64
import subprocess
import time
import json

import dash
import requests
from dash import dcc, html, Input, Output, State, callback


# FRONTEND SERVER CONFIG
FRONTEND_PORT = 8050
FRONTEND_ADDRESS = "0.0.0.0"

BACKEND_PORT = 8000
BACKEND_ADDRESS = "backend"
ADDRESS = f"http://{BACKEND_ADDRESS}:{BACKEND_PORT}"

# Start FastAPI server if not already running
def start_backend():
    try:
        response = requests.get(ADDRESS)
        if response.status_code == 200:
            print("Backend is already running.")
            return
    except requests.exceptions.ConnectionError:
        print("Starting backend...")
        subprocess.Popen(["uvicorn", "BackendService.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
        time.sleep(2)  # Give it time to start


# start_backend()


# STATIC OPTIONS
USER_TYPES = ["runner", "photographer"]
RUNNER_INPUT_FIELDS = {
    "email": "email",
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
        multiple=True,
    ),
    html.Br(),
    html.Img(id="image-preview", style={"maxWidth": "300px"}),
    html.Div(id="upload-status"),
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
    response = requests.post(f"{ADDRESS}/submit-data", json=payload)
    return response.json().get("message", "No message returned from server.")


def preview_image(content, filename, status_code):
    status_emojis = {
        200: "✅", 400: "⚠️", 404: "❌", 500: "🔥"
    }
    status_display = f"{status_emojis.get(status_code, 'ℹ️')} {status_code}"

    return html.Div([
        html.Div([
            html.H3(f"{filename} → {status_display}", style={'textAlign': 'center'}),
            html.Img(src=content, style={'maxWidth': '50%', 'height': 'auto', 'display': 'block', 'margin': 'auto'})
        ]),
    ])


@app.callback(
    Output("upload-status", "children"),
    # Output("image-preview", "src"),
    Input("upload-image", "contents"),
    State("upload-image", "filename"),
    *[State("input_{}".format(field_name), "value") for field_name, field_type in RUNNER_INPUT_FIELDS.items()],
    prevent_initial_call=True
)
def upload_image(contents, filenames, email, bib_number):  #FIXME: signature explicitly enums / orders the fields defined in RUNNER_INPUT_FIELDS. If we change those, this will break (and defeat the purpose of having them defined with a list for flexibility)
    if contents is None:
        return "Upload failed!", None

    status_codes = {}
    outputs = []

    for content, filename in zip(contents, filenames):
        # Decode the image from Dash
        _, content_string = content.split(',')
        image_data = base64.b64decode(content_string)

        # Send image to backend
        files = {"file": (filename, image_data, "image/png")}
        data = {"metadata": json.dumps({"email": email, "bib_number": bib_number})}

        response = requests.post(f"{ADDRESS}/upload", files=files, data=data)

        # FIXME: I think this breaks if there are multiple files with the same name
        status_codes[filename] = response.status_code
        outputs.append(preview_image(content, filename, status_codes[filename]))

    return outputs


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
# def update_output(list_of_contents, list_of_names, list_of_dates):
#     if list_of_contents is not None:
#         children = [
#             parse_contents(c, n, d) for c, n, d in
#             zip(list_of_contents, list_of_names, list_of_dates)]
#         return children

# Run the app
if __name__ == '__main__':
    app.run(
        host=FRONTEND_ADDRESS,
        port=FRONTEND_PORT,
        debug=True,
    )
