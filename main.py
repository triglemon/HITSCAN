import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth


g_auth = GoogleAuth()
drive = GoogleDrive(g_auth)

try:
    with open('tesseract_cmd') as path_file:
        path = path_file.read()
        pytesseract.pytesseract.tesseract_cmd = path
except FileNotFoundError:
    print("No alternate file found")


with Image.open('test data/page.png') as img:
    filtered_img = img.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(filtered_img)
img = enhancer.enhance(2)
img = img.convert('1')
img.save('test data/page_2.png')
with Image.open('test data/page_2.png') as img:
    text = pytesseract.image_to_string(img)
print(text)


with open('test data/document.docx', 'w') as file:
    file.write(text)

drive_file = drive.CreateFile({'title': 'Image Text'})
drive_file.SetContentString(text)
drive_file.Upload()
