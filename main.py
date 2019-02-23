import pytesseract
from PIL import Image, ImageEnhance, ImageFilter


pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Robert\AppData\Local\Tesseract-OCR\tesseract.exe'
with Image.open("label_meme.jpg") as img:
    filtered_img = img.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(filtered_img)
img = enhancer.enhance(2)
img = img.convert('1')
img.save('label_meme2.jpg')
with Image.open('label_meme2.jpg') as img:
    text = pytesseract.image_to_string(img)
print(text)
