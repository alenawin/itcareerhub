from dash import Dash, html, dcc
from dash import Input, Output, callback
import plotly.express as px

df = px.data.gapminder()

continents = sorted(df["continent"].unique())

dropdown = [
    {"label": continent, "value": continent}
    for continent in continents
]

app = Dash()

header = html.H1("Gapminder: распределение lifeExp по континенту")

app.layout = html.Div([
    header,
    dcc.Dropdown(
       id="continent-dropdown",
       options=dropdown,
       value=continents[0],
       clearable=False,
    ),
    dcc.Graph(id="lifeexp-histogram"),
])

@callback(
    Output("lifeexp-histogram", "figure"),
    Input("continent-dropdown", "value"),
)
def update_histogram(selected_continent):

    filtered_df = df[df["continent"] == selected_continent]

    fig = px.histogram(
        filtered_df,
        x="lifeExp",
        nbins=20,
        title=f"Распределение lifeExp для континента: {selected_continent}",
        labels={
            "lifeExp": "Ожидаемая продолжительность жизни",
            "count": "Количество наблюдений"}
    )

    return fig

app.run(debug=True)