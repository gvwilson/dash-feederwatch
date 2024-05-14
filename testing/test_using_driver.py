import dash
from dash import html


def test_001_child_with_0(dash_duo):
    app = dash.Dash(__name__)
    app.layout = html.Div(id="nully-wrapper", children=0)

    dash_duo.start_server(app)

    dash_duo.wait_for_text_to_equal("#nully-wrapper", "0", timeout=4)

    assert dash_duo.find_element("#nully-wrapper").text == "0"

    assert dash_duo.get_logs() == [], "browser console should contain no error"

    dash_duo.percy_snapshot("test_001_child_with_0-layout")
