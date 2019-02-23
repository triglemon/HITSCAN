import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import drive_auth
from googleapiclient.http import MediaFileUpload
import os

#g_auth = drive_auth.auth()

g_auth = GoogleAuth()
drive = GoogleDrive(g_auth)

try:
    if os.path.exists("config.txt"):
        pytesseract.pytesseract.tesseract_cmd = open("config.txt", "r+"
                                                     ).readlines()[0]
with Image.open('page.png') as img:
    filtered_img = img.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(filtered_img)
img = enhancer.enhance(2)
img = img.convert('1')
img.save('page_2.png')
#with Image.open('page_2.png') as img:


# Transcribing image to text
def transcribe(image_path, mode: int, drive=None):
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
    transcribe('test data/page.png', 2, drive)


if __name__ == '__main__':
    __main__()
