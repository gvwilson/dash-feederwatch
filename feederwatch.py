# Import packages
from dash import Dash, html, dash_table, dcc
import pandas as pd
import plotly.express as px


PAGE_SIZE = 15
DATA_DIR = "cooked"
BIRDS_DATA = f"{DATA_DIR}/birds-ca.csv"
SPECIES_DATA = f"{DATA_DIR}/species-ca.csv"


# Incorporate data
birds = pd.read_csv(BIRDS_DATA)
species = pd.read_csv(SPECIES_DATA)

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='FeederWatch'),
    dash_table.DataTable(data=birds.to_dict('records'), page_size=PAGE_SIZE),
    dcc.Graph(figure=px.histogram(birds, x='region', y='num', histfunc='sum'))

])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
