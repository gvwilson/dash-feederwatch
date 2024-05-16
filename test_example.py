from dash import Dash, Input, Output, callback, callback_context
from contextvars import copy_context
from dash._callback_context import context_value
from dash._utils import AttributeDict


Current = [0]


app = Dash(__name__)


@app.callback(
    Output("left", "value"),
    Input("right", "value")
)
def right_to_left(right):
    Current[0] = right + 1
    return Current[0]


@app.callback(
    Output("right", "value"),
    Input("left", "value")
)
def left_to_right(left):
    Current[0] = left + 1
    return Current[0]


def test_right_to_left():
    def run_callback():
        print(f"in callback type(context_value) {type(context_value)}")
        context_value.set(AttributeDict(**{"triggered_inputs": [{"right": "value"}]}))
        return right_to_left(0)

    ctx = copy_context()
    print(f"in test type(ctx) {type(ctx)}")
    output = ctx.run(run_callback)
    assert output == 1


if __name__ == "__main__":
    print(right_to_left(Current[0]))
    print(left_to_right(Current[0]))
