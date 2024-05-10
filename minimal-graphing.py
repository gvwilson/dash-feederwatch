'''Minimal graphing example to try to understand click behavior.'''

from dash import Dash, Input, Output, callback, dcc, html, _dash_renderer
import dash_mantine_components as dmc
import plotly.express as px
import sys

import util


PAGE_SIZE = 15
DISPLAY_GRAPH = 'graph'
DISPLAY_SELECTED = 'selected'
WIDTH_LABEL = 1
WIDTH_DROPDOWN = 4
ALLOWED = {'clickData', 'hoverData', 'selectedData'}

def main(name):
    '''Main driver.'''
    assert (len(sys.argv) == 2) and (sys.argv[1] in ALLOWED), f'choice must be in {ALLOWED}'
    choice = sys.argv[1]
    birds, species, regions = util.load_data()
    species_labels = util.make_labels(species, 'species_id', 'en_us')
    regions_labels = util.make_labels(regions, 'region', 'name')
    components = create_components(birds, species_labels, regions_labels)
    app = do_layout(name, components, choice)
    create_callbacks(birds, choice)
    app.run(debug=True)


def create_components(birds, species_labels, regions_labels):
    '''Create dashboard components (use component IDs as dict keys).'''
    temp = birds.groupby(['region', 'species_id']).agg(num = ('num', 'sum')).reset_index()
    fig = px.scatter(temp, x='region', y='species_id', size='num')
    fig.update_layout(clickmode='select')
    return {
        DISPLAY_GRAPH: dcc.Graph(figure=fig, id=DISPLAY_GRAPH),
        DISPLAY_SELECTED: html.Pre(id=DISPLAY_SELECTED),
    }


def do_layout(name, components, choice):
    '''Lay out components using Mantine.'''
    # https://github.com/snehilvj/dash-mantine-components/issues/240
    _dash_renderer._set_react_version('18.2.0')
    app = Dash(name)
    app.layout = dmc.MantineProvider(children=[
        # title
        dmc.Title('FeederWatch with Interactive Graph'),
        # text display of details of point selected in graph
        dmc.Grid(children=[
            dmc.GridCol(html.Div(f'{choice}:'), span=WIDTH_LABEL),
            dmc.GridCol(components[DISPLAY_SELECTED], span=WIDTH_DROPDOWN),
        ]),
        # graph
        dmc.Grid(children=[dmc.GridCol(components[DISPLAY_GRAPH])]),
    ])
    return app



def create_callbacks(birds, choice):
    '''Connect component callbacks.'''
    # Change text showing selected data when a point is clicked in the graph
    @callback(
        Output(DISPLAY_SELECTED, 'children'),
        Input(DISPLAY_GRAPH, choice)
    )
    def update_selection(arg):
        print(f"update_selection({arg})", file=sys.stderr)
        return str(arg)


if __name__ == '__main__':
    main(__name__)
