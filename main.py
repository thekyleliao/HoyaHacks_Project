from taipy.gui import Gui
from PIL import Image
from io import BytesIO
from exif import Image as ExifImage
import os

def create_image(image_path):
    image_format = "PNG"
    if (os.path.splitext(image_path)[1] == "jpg"): image_format = "JPG"

    image = Image.open(image_path)
    buffer = BytesIO()
    image.save(buffer, format=image_format)
    return buffer.getvalue()

content = ""
image = create_image("placeholder_image.png")

exif_tags = {
    "make": None,
    "model": None,
    "datetime_original": None,
    "gps_latitude": None,
    "gps_latitude_ref": None,
    "gps_longitude": None,
    "gps_longitude_ref": None,
    "gps_altitude": None
}

exif_info = ["None" for i in range(len(exif_tags))]

page = """
# CTFpy
### Upload images here and see their metadata

<|{content}|file_selector|label=Upload Image|extensions=.png,.jpg|on_action=upload_file|>

<|{image}|image|>

<|{exif_tags}|table|rebuild=True|>
"""

def upload_file(state):
    state.image = create_image(state.content)
    get_metadata(state)

def get_metadata(state):
    with open(state.content, "rb") as input_file:
        img = ExifImage(input_file)
    
    for tag in state.exif_tags:
        value = img.get(tag)
        state.exif_tags[tag] = value

if __name__ == "__main__":
    Gui(page=page).run(use_reloader=True)
