from exif import Image as ExifImage

filename = "image.jpg"

EXIF_TAGS = [
    "artist",
    "make",
    "model",
    "datetime_original",
    "gps_latitude",
    "gps_latitude_ref",
    "gps_longitude",
    "gps_longitude_ref",
    "gps_altitude",
]

with open(filename, "rb") as input_file:
    img = ExifImage(input_file)

img.artist = "Sahib"

for tag in EXIF_TAGS:
    value = img.get(tag)
    print("{}: {}".format(tag, value))
