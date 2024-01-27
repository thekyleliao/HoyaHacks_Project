from taipy.gui import Gui
import taipy as tp
from PIL import Image
from io import BytesIO
from exif import Image as ExifImage
import os


def create_image(image_path):
    image_format = "PNG"
    if (os.path.splitext(image_path)[1] == ".jpg"): image_format = "JPEG"

    image = Image.open(image_path)
    buffer = BytesIO()
    image.save(buffer, format=image_format)
    return buffer.getvalue()

content = ""
image = create_image("placeholder_image.png")

exif_tags = [
    "make",
    "model",
    "datetime_original",
    "gps_latitude",
    "gps_latitude_ref",
    "gps_longitude",
    "gps_longitude_ref",
    "gps_altitude",
]

make = ""
model = ""
datetime = ""
location = ""

new_make = ""
new_model = ""
new_datetime = ""
new_location = ""

page = """
<|container|
<|text-center|
<|card|
# CTFpy
### Upload images here and see their metadata

<|{content}|file_selector|label=Upload Image|extensions=.png,.jpg|on_action=upload_file|>

<|{image}|image|width=10vw|>

### Metadata

<center>Make: <|{make}|text|></center>

Model: <|{model}|text|>

DateTime: <|{datetime}|text|>

Location: <|{location}|text|>

### Edit Metadata

Make: <|{new_make}|input|>

Model: <|{new_model}|input|>

DateTime: <|{new_datetime}|input|>

Location: <|{new_location}|input|>


<iframe width="600" height="400" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"
        src="https://www.openstreetmap.org/export/embed.html?bbox=<{long}|text|,<{lat}|text|>,<{long}|text|>,<{lat}|text|>&layer=mapnik">
</iframe>

<|{None}|file_download|label=Download|on_action=create_new_file|>

<|
"""

def dms_to_decimal(degrees, minutes, seconds, direction):
    decimal_degrees = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if direction == 'S' or direction == 'W':
        decimal_degrees = -decimal_degrees
    return decimal_degrees


def upload_file(state):
    state.image = create_image(state.content)
    get_metadata(state)

def get_metadata(state):
    with open(state.content, "rb") as input_file:
        img = ExifImage(input_file)
    
    state.make = img.get("make")
    state.model = img.get("model")

    datetime_raw = img.get("datetime_original")
    state.datetime = datetime_raw

    latitude, latitude_ref = img.get("gps_latitude"), img.get("gps_latitude_ref")
    longitude, longitude_ref = img.get("gps_longitude"), img.get("gps_longitude_ref")
    altitude = img.get("gps_altitude")

    state.location = str(int(latitude[0])) + "'" + str(int(latitude[1])) + "'" + str(latitude[2]) + "\"" + latitude_ref + " "
    state.location += str(int(longitude[0])) + "'" + str(int(longitude[1])) + "'" + str(longitude[2]) + "\"" + longitude_ref

    latitude_deg = int(latitude.split("'")[0])
    latitude_min = int(latitude.split("'")[1].split("'")[0])
    latitude_sec = float(latitude.split("'")[1].replace(' ', '').replace('"', ''))

    longitude_deg = int(longitude.split("'")[0])
    longitude_min = int(longitude.split("'")[1].split("'")[0])
    longitude_sec = float(longitude.split("'")[1].replace(' ', '').replace('"', ''))


    latDecimal = dms_to_decimal(latitude_deg, latitude_min, latitude_sec, latitude_ref)
    longitude_decimal = dms_to_decimal(longitude_deg, longitude_min, longitude_sec, longitude_ref)

    iframe_code = f"""<iframe width="600" height="400" frameborder="0" src="https://www.openstreetmap.org/export/embed.html?bbox={state.long},{state.lat},{state.long},{state.lat}&layer=mapnik"></iframe>"""
    state.iframe.value = iframe_code


def create_new_file(state):
    with open(state.content, "rb") as input_file:
        img = ExifImage(input_file)
    
    img.make = state.new_make
    img.model = state.new_model
    img.datetime = state.new_datetime
    
    parsed_location = ""
    for i in range(len(state.new_location)):
        if (state.new_location[i].isnumeric() or state.new_location[i] == '.' or state.new_location[i] in "NSEW"):
            parsed_location += state.new_location[i]
        else:
            parsed_location += ' '
    
    location_list = parsed_location.split()
    print(location_list)
    
    img.gps_latitude = (location_list[0], location_list[1], location_list[2])
    img.gps_latitude_ref = location_list[3]
    img.gps_longitude = (location_list[4], location_list[5], location_list[6])
    img.gps_longitude_ref = location_list[7]

    with open(state.content, "wb") as output_file:
        output_file.write(img.get_file())
    
    Download(state, content = bytes(output_file, "UFT-8"))


if __name__ == "__main__":
    Gui(page=page).run(use_reloader=True)
