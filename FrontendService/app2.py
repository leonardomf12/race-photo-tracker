import dash
from dash import html, dcc, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import subprocess
import requests
import time

from user_photographer import User

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

# Help functions
def runner_content():
    return html.Div([
        html.H4("Runner View"),
        html.Div([
            html.Ul([html.Li(item) for item in user.races])
        ], style={"backgroundColor": "#d1f0ff", "padding": "10px", "borderRadius": "8px"})
    ])

def photographer_content():
    return html.Div([
        html.H4("Photographer View"),
        dbc.Button("Create New Race", id="new-race-btn", className="mb-2"),
        dcc.Upload(id='upload-data', children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]), style={
            'width': '100%', 'height': '60px', 'lineHeight': '60px',
            'borderWidth': '1px', 'borderStyle': 'dashed',
            'borderRadius': '5px', 'textAlign': 'center',
            'margin-bottom': '10px'
        }, multiple=True),
        dbc.Button("Submit Files", id="submit-files-btn", color="success"),
        html.Div(id="upload-output", className="mt-2")
    ])


# Initialize app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], suppress_callback_exceptions=True)
app.title = "Photographer & Runner App"
server = app.server

# User
user = User()

# Layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H2("Race Dashboard"), width=8),
        dbc.Col([
            dbc.Row([
                dcc.Input(id="username", type="text", placeholder="Enter username"),
                dcc.Input(id="password", type="text", placeholder="Enter password"),
                html.Div(id="user-login-info")
            ]),
        ]),
        dbc.Col([
            dbc.Button("Login", id="login-button", color="primary", className="ms-2")
        ])
    ], align="center", className="my-3"),
    html.Hr(), # Horizontal Rule
    dbc.Row([
        dcc.Dropdown(id="role-dropdown", options=[{"label": "runner", "value": "runner"}, {"label": "photographer", "value": "photographer"}], style={"width": "200px"}),
        runner_content(),
        html.Div(style={"height": "50px"}),
        photographer_content()
            ], style={
        "display": "flex",
        "justifyContent": "center",  # horizontal center
        "alignItems": "center",      # vertical center (if needed)
    })
])


# Callback: handle file submission
@app.callback(
    [Output("user-login-info", "children"), Output("user-login-info", "style")],
    Input("login-button", "n_clicks"),
    State("username", "value"),
    State("password", "value"),
    prevent_initial_call=True
)
def login_button(n_clicks, username, password):
    login_status = user.login(username, password)

    if login_status:
        return "Login Successful!", {"color": "green"}
    else:
        return "Login Failed!", {"color": "red"}

# TODO Allow this only after user is logged in
@app.callback(
    Output("content", "children"),
    Input("role-dropdown", "value")
)
def page_content(role):
    if role == "runner":
        return runner_content()
    elif role == "photographer":
        return photographer_content()


if __name__ == "__main__":
    app.run(debug=True)
