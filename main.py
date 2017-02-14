import json
import datetime
import requests
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont


def parse_json():
    json_data = open("/home/sergiy/python_projects/TV_program/data.json", "r")
    data = json.load(json_data)
    return data["data"]["programs"]


def get_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


def get_time_string(time):
    seconds = ('/Date({}000)/'.format(time)).split('(')[1][:-5]
    return datetime.datetime.fromtimestamp(float(seconds)).strftime('%Y-%m-%d %H:%M:%S')[-8:-3]


def draw_text():
    pass


def create_tag():
    pass


def compose_tags(width, height, tags):
    canvas = Image.new("RGB", (width, height), "#fff")
    offest_y = 0
    for tag in tags:
        canvas.paste(tag, (0, offest_y))
        offest_y += 87
    canvas.save("tv_program.jpeg")


def main():
    programs = parse_json()
    tags = []
    for program in programs:
        tag = create_tag(program["realtime_begin"], program["realtime_end"],
                         program["image"]["preview"], program["title"], program["subtitle"])
        tags.append(tag)
    compose_tags(485, 1900, tags)


main()

