import os
import base64


def get_image_base64(image_path: str) -> str:
    """
    Считывает изображение по указанному пути и возвращает его строковое представление в формате base64.
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Файл не найден: {image_path}")

    with open(image_path, "rb") as image_file:
        image_data = image_file.read()

    encoded_image = base64.b64encode(image_data).decode('utf-8')
    os.remove(image_path)
    return encoded_image