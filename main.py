import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

# Google api permissions authentication
g_auth = GoogleAuth()
drive = GoogleDrive(g_auth)

# Check for alternate path string
try:
    with open('tesseract_cmd') as path_file:
        path = path_file.read()
        pytesseract.pytesseract.tesseract_cmd = path
except FileNotFoundError:
    print("No alternate file found")


# Transcribing image to text
def transcribe(image_path, mode: int):
    with Image.open(image_path) as img_file:
        img = img_file.filter(ImageFilter.MedianFilter())
    img = ImageEnhance.Contrast(img)
    img = img.enhance(2)
    img = img.convert('1')
    text = pytesseract.image_to_string(img)
# Modes: 0 -> print; 1 -> save local docx; 2 -> upload to drive
    if mode == 0:
        print(text)

    if mode == 1:
        with open('test data/document.docx', 'w') as file:
            file.write(text)

    if mode == 2:
        drive_file = drive.CreateFile({'title': 'Image Text'})
        drive_file.SetContentString(text)
        drive_file.Upload()


def __main__():
    transcribe('test data/page.png', 2)


if __name__ == __main__:
    __main__()
