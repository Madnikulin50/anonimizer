

import json
import base64
import io
from mimesis import Person, Generic
import pagan
import requests
import argparse
import os

parser = argparse.ArgumentParser(description='Use generator for anonimize')
parser.add_argument('--photo', help='generate photo', action="count", default=False)

args = parser.parse_args()

symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",
           u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")

tr = {ord(a):ord(b) for a, b in zip(*symbols)}



data = {}
domain = "acme"
mailDomain = "acme.ru"
data['domain'] = domain
data['mail'] = mailDomain
data['user'] = []

fileName = 'anonimize_ussers_acme.json'

usePhoto = args.photo

if os.path.isfile(fileName):
    os.remove(fileName)

def image_to_byte_array(image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

def writeToJson(fn, entry):
    if os.path.isfile(fn):
        # File exists
        with open(fn, 'a+') as outfile:
            outfile.seek(0, os.SEEK_END)
            outfile.seek(outfile.tell() - 1, os.SEEK_SET)
            outfile.truncate()
            outfile.write(',')
            json.dump(entry, outfile)
            outfile.write(']')
    else:
        # Create file
        with open(fn, 'w') as outfile:
            array = []
            array.append(entry)
            json.dump(array, outfile)

person = Person('ru')
generic = Generic('en')

for i in range(1, 250000):

    fn = person.full_name()

    m = fn.translate(tr).replace(" ", ".")
    userName = m
    mail = m + "@" + mailDomain
    imageString = ""
    if usePhoto :
        avatarUrl = person.avatar()
        r = requests.get(avatarUrl)
        imageString = ""
        if r.status_code == 200:
            imageString = base64.b64encode(r.content).decode("utf-8")
        else:
            img = pagan.Avatar(userName, pagan.SHA512)
            img.save('.\\', 't')
            with open(".\\t.png", "rb") as binary_file:
                dataImage = binary_file.read()
            imageString = base64.b64encode(dataImage).decode("utf-8")



    entry = {
        'cn': fn,
        'name': userName,
        'displayName': fn,
        'mail': mail,
        'givenName': fn[: fn.find(' ')],
        'title': person.occupation(),
        "mobile":  person.telephone(),
        "sAMAccountName": userName,
        "company": domain,
        "userPrincipalName": userName + "@" + domain
    }

    if usePhoto:
        entry["photo"] = imageString


    writeToJson(fileName, entry)
    print(i, fn, userName, mail, userName, userName + "@" + domain)
