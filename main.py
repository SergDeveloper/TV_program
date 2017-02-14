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


def draw_text(canvas, title, subtitle, begin_time, end_time):
    draw = ImageDraw.Draw(canvas)
    font_text1 = ImageFont.truetype('arial.ttf', 16, encoding="unic")
    font_text2 = ImageFont.truetype('arial.ttf', 14, encoding="unic")
    font_time = ImageFont.truetype('arial.ttf', 14, encoding="unic")
    draw.text((25, 30), begin_time, font=font_time, fill="black")
    draw.text((25, 50), end_time, font=font_time, fill="black")
    draw.text((220, 15), title, font=font_text1, fill="white")
    draw.text((230, 50), subtitle, font=font_text2, fill="black")


def create_tag(time_begin, time_end, image_link, title, subtitle):
    begin_time = get_time_string(time_begin)
    end_time = get_time_string(time_end)
    canvas = Image.new("RGB", (500, 200), "#fff")

    image = get_image(image_link)
    size = (0.15 * image.size[0], 0.15 * image.size[1])
    image.thumbnail(size)
    canvas.paste(image, (100, 0))

    background = Image.new("RGB", (270, 86), "#f33")
    canvas.paste(background, (215, 0))

    draw_text(canvas, title, subtitle, begin_time, end_time)

    return canvas


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
    compose_tags(485, len(programs)*87, tags)


main()

