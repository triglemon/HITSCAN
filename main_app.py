import pytesseract
from PIL import ImageEnhance, ImageFilter
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
from tkinter import *
import tkinter
from tkinter import filedialog
<<<<<<< HEAD
=======
from functools import partial
>>>>>>> 8b1e4ca1765a9ec5a41d074e7850ea0a8c76852a
import PIL.Image


g_auth = GoogleAuth()
drive = GoogleDrive(g_auth)
var = None


def open_file(tkinter_root):
    absolute_path = filedialog.askopenfilename(initialdir="/", title="Select file",
                                               filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))
    print(absolute_path)
    tkinter_root.filename = absolute_path.replace("C:/Users/Robert/PycharmProjects/hackerhack/Paper-Scanner/", "")


def get_best_text(image, iter: int):
    rot_angle = 90 // iter
    
    best_angle = None
    best_conf = 0
    for i in range(iter):
        rot = image.rotate( i * rot_angle, expand=1 )
        print("angle = {0}\n".format(i*rot_angle))
        confs = pytesseract.image_to_data(rot, output_type=pytesseract.Output.DICT)["conf"]
        
        rot.show()

        # convert non-integer entries to 0
        for i in range(len(confs)):
            # print(confs[i], " <- item\n")
            # print(type(confs[i]), " <- type\n")
            if type(confs[i]) != int:
                confs[i] = 0

        confidence = sum(confs)/len(confs)
        print("confidence = {0}, sum = {1}, len = {2}\n".format(confidence, sum(confs), len(confs)))
        if confidence > best_conf:
            best_angle = i*rot_angle
    rot = image.rotate(best_angle)
    return pytesseract.image_to_string(rot)


# Transcribing image to text
def transcribe(path, doc_bool, drive_bool, tilt_bool):
    print(path)
    with PIL.Image.open(path) as img:
        img = img.convert('RGB')
    img = img.filter(ImageFilter.MedianFilter())
    img = ImageEnhance.Contrast(img)
    img = img.enhance(2)
    img = img.convert('1')

    text = pytesseract.image_to_string(img)

    if tilt_bool:
        print(get_best_text(img, 9))

    else:
        print(text)
        if doc_bool:
            with open('test data/document.docx', 'w') as file:
                file.write(text)
        if drive_bool:
            drive_file = drive.CreateFile({'title': 'Image Text'})
            drive_file.SetContentString(text)
            drive_file.Upload()


def main():
    try:
        with open('tesseract_cmd') as path_file:
            path = path_file.read()
            pytesseract.pytesseract.tesseract_cmd = path
    except FileNotFoundError:
        print("No alternate file found")

    app = tkinter.Tk()
    app.wm_title('HITSCAN')
    app.filename = None

    img_button = Button(app, text='Browse', width=5, command=partial(open_file, app))
    img_button.grid(row=1, column=1)

    doc_var = tkinter.IntVar()
    doc_box = Checkbutton(app, text="Include .docx", variable=doc_var)
    doc_box.grid(row=2, column=1)

    drive_var = tkinter.IntVar()
    drive_box = Checkbutton(app, text="Clone to Google Drive", variable=drive_var) # drive there
    drive_box.grid(row=3, column=1)

    tilt_var = tkinter.IntVar()
    tilt_box = Checkbutton(app, text="Image has tilt", variable=tilt_var)
    tilt_box.grid(row=4, column=1)

    process_button = Button(app, text="Process", width=5, command=partial(transcribe, *('test data/page.png',
                                                                                        doc_var.get(),
                                                                                        drive_var.get(),
                                                                                        tilt_var.get())))
    process_button.grid(row=5, column=1)
    app.mainloop()


if __name__ == '__main__':
    main()
