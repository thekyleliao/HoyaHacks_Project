from taipy.gui import Gui, notify
import pandas as pd
from PIL import Image
from io import BytesIO

original_image = None
content = None

# Definition of the page
page = """
# Getting started with Taipy GUI

<|{content}|file_selector|label=Select Image|extensions=.png,.jpg|on_action=on_file_upload|>

<|{original_image}|image|>
"""

def on_button_action(state):
    notify(state, 'info', f'The text is: {state.text}')
    state.text = "Button Pressed"

def on_change(state, var_name, var_value):
    if var_name == "text" and var_value == "Reset":
        state.text = ""
        return

def on_file_upload(state):
    image = Image.open(state.content)
    buf = BytesIO()
    image.save(buf, format="PNG")
    state.original_image = buf.getvalue()


Gui(page).run()