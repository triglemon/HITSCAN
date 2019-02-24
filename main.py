import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import cv2


def get_best_text(image, iter: int):
    rot_angle = 90 // iter
    
    best_angle = None
    best_conf = 0
    for i in range(iter):
        rot = image.rotate( i * rot_angle, expand=1 )
        print("angle = {0}\n".format(i*rot_angle))
        # rot = rot.convert("RGB")
        # confs = pytesseract.image_to_data(rot, output_type=pytesseract.Output.DICT)["conf"]

        rot.show()

        # #convert non-integer entries to 0
        # for i in range(len(confs)):
        #     # print(confs[i], " <- item\n")
        #     # print(type(confs[i]), " <- type\n")
        #     if type(confs[i]) != int:
        #         confs[i] = 0

        output = pytesseract.image_to_osd(rot, output_type='dict')
        confidence1 = output["script_conf"]
        confidence2 = output["script_conf"]
        # confidence = sum(confs)/len(confs)
        # print("confidence = {0}, sum = {1}, len = {2}\n".format(confidence, sum(confs), len(confs)))
        # print(pytesseract.image_to_osd(rot))
        if confidence1 + confidence2 > best_conf:
            best_angle = i*rot_angle
            best_conf = confidence1 + confidence2
    rot = image.rotate(best_angle)
    return pytesseract.image_to_string(rot)

# Transcribing image to text
def transcribe(image_path, mode: int, drive=None):
    with Image.open(image_path) as img:
        img = img.convert('RGB')
    img = img.filter(ImageFilter.MedianFilter())
    img = ImageEnhance.Contrast(img)
    img = img.enhance(2)
    img = img.convert('1')

    text = pytesseract.image_to_string(img)

    # Modes: 0 -> print; 1 -> save local docx; 2 -> upload to drive 3 -> debug
    if mode == 0:
        print(text)

    elif mode == 1:
        with open('test data/document.docx', 'w') as file:
            file.write(text)

    elif mode == 2:
        drive_file = drive.CreateFile({'title': 'Image Text'})
        drive_file.SetContentString(text)
        drive_file.Upload()
    
    elif mode == 3: # debug
        # display image
        img.show()
        # Get bounding box estimates
        print(pytesseract.image_to_boxes(img))

        # Get verbose data including boxes, confidences, line and page numbers
        print(pytesseract.image_to_data(img))

        # Get information about orientation and script detection
        print(pytesseract.image_to_osd(img))
    elif mode == 4:
        print(get_best_text(img, 9))


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
    mode = int(input("Modes: 0 -> print; 1 -> save local docx; 2 -> upload to drive; 3 -> debug\n"))
    if mode == 2:
        # Google api permissions authentication
        g_auth = GoogleAuth()
        drive = GoogleDrive(g_auth)
    transcribe(path, mode, drive)


if __name__ == '__main__':
    main()
