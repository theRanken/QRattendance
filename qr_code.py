import qrcode
import os
from app import BASE
from flask import send_file as view
import io

def generate_code(*args:str, mat_no:str)->str:
    #Instantiate the qr maker object
    qr = qrcode.QRCode(version = 1, box_size = 10, border = 5)

    #Get All the supplied fields and add to the QR information
    for arg in args:
        qr.add_data(arg)

    #strip slashes in 'mat_no'
    mat_no = mat_no.replace('/', '')
    #create a file path with student's matric number as image name
    file_path =  f'media/QR_CODES/{mat_no}.png'
    #Get the full path and replace the backslashes with forward slashes
    full_path = os.path.join(BASE, file_path)
    full_path = full_path.replace('\\','/')
    #Make QR code and save image to the genrated folder  
    qr.make(fit = True)
    img = qr.make_image(fill_color = 'black', back_color = 'white')
    img.save(full_path)

    return full_path

def get_qr_code(file:str):
    # Convert binary format to images or files data
    with open(file, 'rb') as file:
        #read data from file
        picture_data = file.read()
    return picture_data

def to_picture(img):
    img = io.BytesIO(img)
    return view(img, mimetype="image/png")

def clean_image(path:str):
    #checking if file exist or not
    if(os.path.isfile(path)):
        #os.remove() function to remove the file
        os.remove(path)
        #Printing the confirmation message of deletion
        print("File Deleted successfully")
    else:
        print("File does not exist")
    #Showing the message instead of throwig an error