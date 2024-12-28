from PIL import Image, ImageDraw, ImageFont
from typing import Tuple
import random

def generate_avatar(text: str, path_save: str, size: Tuple[int]) -> None:
    background_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    image = Image.new("RGB", (size[0], size[1]), background_color)
    
    draw = ImageDraw.Draw(image)
    
    try:
        font = ImageFont.truetype("arial.ttf", sum(size) // 4)
    except IOError:
        font = ImageFont.load_default()
    
    # Вычисление размера текста и его позиции
    text_width, text_height = draw.textsize(text, font=font)
    text_x = (size[0] - text_width) // 2
    text_y = (size[1] - text_height) // 2
    
    # Рисование текста на изображении
    draw.text((text_x, text_y), text, fill="white", font=font)
    
    # Сохранение изображения в формате PNG
    image.save(path_save)

if __name__ == "__main__":
    from string_handlers import text_for_generate_avatar_handler
    
    generate_avatar(
        text = text_for_generate_avatar_handler("test nickname"),
        path_save = "server\\avatars\\test_image.png",
        size = (100, 100)
    )
