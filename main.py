import pytesseract
from PIL import Image, ImageEnhance, ImageFilter

im = Image.open("label_meme.jpg") # the second one
im = im.filter(ImageFilter.MedianFilter())
enhancer = ImageEnhance.Contrast(im)
im = enhancer.enhance(2)
im = im.convert('1')
im.save('label_meme2.jpg')
text = pytesseract.image_to_string(Image.open('label_meme2.jpg'))
print(text)
