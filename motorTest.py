from gpiozero import OutputDevice, Button, LED
from time import sleep
import boto3
import io
from PIL import Image
from pprint import pprint
import os
import datetime
import re
import time
import picamera

motor = OutputDevice(4)
button = Button(14)
led = LED(3)

# connect to aws rekognition
BUCKET = 'itpface'
COLLECTION_ID = 'itpFaces'
s3 = boto3.resource('s3')
client = boto3.client('rekognition')
rekognition = boto3.client('rekognition', region_name='us-east-1')


# take a picture and save as a local file


def take_picture(camera, stream):

    print("Taking image...")
    # Take the actual image we want to keep

    camera.capture(stream, format="jpeg")
    os.system("espeak \"Hello Hello, I am processing your pictures\"  --stdout | aplay -D bluealsa:HCI=hci0,DEV=70:99:1C:07:86:EE,PROFILE=a2dp")
    return Image.open(stream)
    #return(file)

# upload the captured picture to aws and search for matching face
def findName(stream):

    response = rekognition.detect_faces(
        Image={'Bytes':  stream.getvalue()}
    )

    all_faces = response['FaceDetails']

    # Initialize list object
    boxes = []

    image = Image.open(stream)
    # Get image diameters
    image_width = image.size[0]
    image_height = image.size[1]

    # Crop face from image
    for face in all_faces:
        box = face['BoundingBox']
        x1 = int(box['Left'] * image_width) * 0.9
        y1 = int(box['Top'] * image_height) * 0.9
        x2 = int(box['Left'] * image_width + box['Width'] * image_width) * 1.10
        y2 = int(box['Top'] * image_height
                 + box['Height'] * image_height) * 1.10
        image_crop = image.crop((x1, y1, x2, y2))

        stream = io.BytesIO()
        image_crop.save(stream, format="JPEG")
        image_crop_binary = stream.getvalue()

        # Submit individually cropped image to Amazon Rekognition
        response = rekognition.search_faces_by_image(
            CollectionId='itpFaces',
            Image={'Bytes': image_crop_binary}
        )
        face_found = len((response["FaceMatches"]))
        if face_found:
            print('found ' + str(face_found) + 'face')
            matchedFile = response["FaceMatches"][0]["Face"]["ExternalImageId"]
            # b = matchedFile.index(".")
            # returnName = matchedFile[:b]
            return matchedFile
        if not face_found:
            return


def detectEmotion():

    response = client.detect_faces(
        Image={'S3Object': {'Bucket': BUCKET, 'Name': photo}}, Attributes=['ALL'])

    print('Detected faces for ' + photo)
    for faceDetail in response['FaceDetails']:
        for emotion in faceDetail['Emotions']:
            if emotion['Confidence'] > 60:
                print(str(emotion['Type']) + ', ' + str(emotion['Confidence']))


def uploadSingleImg(stream, name):
    # file = open(fileName, 'rb')
    t = str(datetime.datetime.now())
    fileName = re.sub(r'\D', "", t)[4:12] + ".jpeg"

    object = s3.Object('itpface', fileName)
    ret = object.put(Body=stream.getvalue(),
                     Metadata={'FullName': name}
                     )
    response = client.index_faces(CollectionId=COLLECTION_ID,
                                  Image={'S3Object': {
                                      'Bucket': BUCKET, 'Name': fileName}},
                                  ExternalImageId=name,
                                  MaxFaces=2,
                                  QualityFilter="AUTO",
                                  DetectionAttributes=['DEFAULT'])
    print(response)



def main():
    with picamera.PiCamera()as camera:
        camera.resolution = (1024, 768)
        camera.rotation = 90
        camera.start_preview()

        stream = io.BytesIO()

        time.sleep(1)

        while True:  # comment this out if you ar enot using a button
            button.wait_for_press()  # comment this out if you ar not using a button
            print("pressed")
            take_picture(camera, stream)

            name = findName(stream)

            if name:
                response = rekognition.detect_faces(
                    Image={'Bytes': stream.getvalue()}, Attributes=['ALL'])
                    # pprint (response)
                print('Detected faces for ' + str(name))
                os.system("espeak \"Hello" + str(name) +
                          "\" --stdout | aplay -D bluealsa:HCI=hci0,DEV=70:99:1C:07:86:EE,PROFILE=a2dp")
                no_emotion = True
                pprint(response)
                print(response['FaceDetails'][0]['Emotions'])
                for faceDetail in response['FaceDetails']:
                    for emotion in faceDetail['Emotions']:
                        if emotion['Type'] == "SAD":
                            if emotion['Confidence'] > 10:
                            print("looks like you are sad")
            else:
                os.system("espeak \"Seems like I don't know you, Can you tell me your name\"  --stdout | aplay -D bluealsa:HCI=hci0,DEV=70:99:1C:07:86:EE,PROFILE=a2dp")
                name_input = input('What is your name? ')
                uploadSingleImg(stream, name_input)
                #print(fileName)
                print(name_input)
                os.system("espeak \"Hello" + str(name_input)
                          + "\" --stdout | aplay -D bluealsa:HCI=hci0,DEV=70:99:1C:07:86:EE,PROFILE=a2dp")

            button.wait_for_release()  # comment this out if you ar enot using a button
            print("released")

if __name__ == "__main__":
    # execute only if run as a script
    main()

# while True:
#     button.wait_for_press()
#     motor.on()
#     print("turn on motor")
#     led.on()
#     sleep(20)
#     led.off()
#     motor.off()
#     print("turn off motor")
