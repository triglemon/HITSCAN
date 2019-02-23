import cv2
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Robert\AppData\Local\Tesseract-OCR\tesseract.exe'


def show_webcam(mirror=False):
    last_text = ""
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)
        text = pytesseract.image_to_string(img)
        if not text == last_text:
            last_text = text
            print(text)
        cv2.imshow('my webcam', img)
        if cv2.waitKey(1) == 27:
            break  # esc to quit
    cv2.destroyAllWindows()


def main():
    show_webcam(mirror=False)


if __name__ == '__main__':
    main()