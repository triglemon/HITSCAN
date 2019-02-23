import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth

g_auth = GoogleAuth()
drive = GoogleDrive(g_auth)

# pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Robert\AppData\Local\Tesseract-OCR\tesseract.exe'
with Image.open('page.png') as img:
    filtered_img = img.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(filtered_img)
img = enhancer.enhance(2)
img = img.convert('1')
img.save('page_2.png')
with Image.open('page_2.png') as img:
    text = pytesseract.image_to_string(img)
print(text)


with open('document.docx', 'w') as file:
    file.write(text)

drive_file = drive.CreateFile({'title': 'Image Text'})
drive_file.SetContentString(text)
drive_file.Upload()
