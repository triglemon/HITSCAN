import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import cv2


# Transcribing image to text
def transcribe(image_path, mode: int, drive=None):
    with Image.open(image_path) as img_file:
        img = img_file.filter(ImageFilter.MedianFilter())
    img = img.convert('RGB')
    img = ImageEnhance.Contrast(img)
    img = img.enhance(2)
    img = img.convert('1')

    text = pytesseract.image_to_string(img)
    # Modes: 0 -> print; 1 -> save local docx; 2 -> upload to drive 3 -> debug
    if mode == 0:
        print(text)
        img.show()

    if mode == 1:
        with open('test data/document.docx', 'w') as file:
            file.write(text)

    if mode == 2:
        drive_file = drive.CreateFile({'title': 'Image Text'})
        drive_file.SetContentString(text)
        drive_file.Upload()
    
    if mode == 3: # debug
        # Get bounding box estimates
        print(pytesseract.image_to_boxes(img))

        # Get verbose data including boxes, confidences, line and page numbers
        print(pytesseract.image_to_data(img))

        # Get information about orientation and script detection
        print(pytesseract.image_to_osd(img))

def main():
    # Check for alternate path string
    drive = None
    try:
        with open('tesseract_cmd') as path_file:
            path = path_file.read()
            pytesseract.pytesseract.tesseract_cmd = path
    except FileNotFoundError:
        print("No alternate file found")
    path = str(input("Path to img file: "))
    mode = int(input("Modes: (0 -> print; 1 -> save local docx; 2 -> upload to drive)"))
    if mode == 2:
        # Google api permissions authentication
        g_auth = GoogleAuth()
        drive = GoogleDrive(g_auth)
    transcribe(path, mode, drive)


if __name__ == '__main__':
    main()
