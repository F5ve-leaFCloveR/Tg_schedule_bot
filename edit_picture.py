from PIL import Image, ImageDraw, ImageFont
import parser_sut
import time

img = Image.open("patterns\example.jpg")
shedule = parser_sut.parse()

def painter(schedule, img = img):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("arial.ttf", size=13)

    positions_days = {
        "1": 10,
        "2": 190,
        "3": 370,
        "4": 550,
        "5": 730,
        "6": 909,
    }
    positions_time = {
        "1": 108,
        "2": 195,
        "ФЗ": 195,
        "3": 282,
        "4": 369,
        "5": 455,
        "6": 541,
    }

    index = 0
    for i in schedule["day"] :
        x = positions_days[str(i)]
        y = positions_time[schedule["time"][index]]
        position_time = (x, y)
        if schedule["time"][index] == "ФЗ":
            position_info = (x+20, y)
        else:
            position_info = (x+10, y)
        
        time = schedule["time"][index] + " "
        draw.text(position_time, time, "#00CF00", font=font, size=17)

        info = schedule["information"][index].replace("\n\n\n", "\n").replace("\n\n", "\n").rstrip()[1:]
        info = info.split("\n")
        words = info[0].split()
        info_result = ""
        line_length = 0
        for word in words:
            if line_length + len(word) + 2 <= 25:
                info_result += word + " "
                line_length += len(word) + 1
            else:
                info_result += f"\n{word} "
                line_length = len(word) + 1
        for strings in info[1:]:
            info_result += f"\n{strings}"

        draw.text(position_info, info_result, font=font)
        img.save("outputs\image_with_text.jpg")
        index += 1
    
    return True
res = painter(shedule)
