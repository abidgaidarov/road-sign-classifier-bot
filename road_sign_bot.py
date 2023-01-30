#import libraries
import aiogram
from aiogram.types import ContentType, Message
from aiogram.dispatcher.filters import Command
from aiogram import Bot, executor, Dispatcher, types

import os
import io
import cv2
import config
import secrets
import logging
import requests
import numpy as np
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
from torchvision import transforms
import torchvision.models as models
from torchvision import transforms as T


# Configure logging
logging.basicConfig(level=logging.INFO)


# Initialize bot and dispatcher
API_TOKEN = config.TOKEN
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Load first trained PyTorch model (YOLO)
model1 = torch.hub.load('ultralytics/yolov5', 
                        'custom', 
                        path='weights_model1.pt', 
                        force_reload=True)


# Function to crop the photos and collect them in the list
def crop_photo(photo_file):
    result = model1(photo_file)
    crops = result.crop(save=False)
    list_of_crops = []
    for n in range(len(crops)):
        extracted_image = crops[n]['im']
        converted_iamge = cv2.cvtColor(extracted_image, 
                                       cv2.COLOR_BGR2RGB)
        img = Image.fromarray(converted_iamge)
        list_of_crops.append(img)
    return list_of_crops


# Load second trained PyTorch model (ResNet50)
model2 = models.resnet50(pretrained=True)
model2.fc = nn.Linear(in_features=2048, 
                      out_features=102)
model2.load_state_dict(torch.load('weights_model2.pt', 
                                  map_location=torch.device('cpu')))
model2.eval()


# Load the dataset with classes
model2_df = pd.read_excel('classes_description.xlsx')
model2_df['class'] = model2_df['class'].astype('int')


# Function to classify iamges
def classify_photo(cropped_photo_path):
    transform = T.Compose([T.Resize((256, 256)), 
                           T.ToTensor()]) 
    img = Image.open(cropped_photo_path) 
    x = transform(img)
    x = x.unsqueeze(0) 
    output = model2(x.to('cpu')) 
    pred = torch.argmax(output, 1)
    return pred


# Function to extract description
def extract_descriptive(predicted_class):
    row = model2_df[model2_df['class']==predicted_class]
    return f"""CATEGORY: {row['category'].item()}, \nDESCRIPTION: {row['descriptive'].item()}"""


# Start command handler
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    user_name = message.from_user.full_name
    await message.reply(f"Hello, {user_name}! 🤖 I'm SignVision, your personal road sign detection and classification expert. 🦾 Powered by AI and computer vision technologies, I can help you identify the road signs in your photos with just a snap. Let's get started! 🚦")

URI_INFO = f"https://api.telegram.org/bot{API_TOKEN}/getFile?file_id="
URI = f"https://api.telegram.org/file/bot{API_TOKEN}/"

if not os.path.exists('static'):
    os.mkdir('static')


# Sent photo handler    
@dp.message_handler(content_types=['photo'])
async def classify(msg: types.Message):
    file_id = msg.photo[-1].file_id
    resp = requests.get(URI_INFO + file_id)
    img_path = resp.json()['result']['file_path']
    img = requests.get(URI+img_path)
    img = Image.open(io.BytesIO(img.content))
    model1_crop = crop_photo(img)

    if len(model1_crop) == 0:
        await msg.answer('I cannot classify it. 🧐 Please try sending another photo.')
    else:
        try:
            for n in model1_crop:
                img_name = secrets.token_hex(8)
                n.save(f'static/{img_name}.png', format='PNG')
                await msg.answer_photo(photo=open(f'static/{img_name}.png', 'rb'))

                predicted_class = classify_photo(f'static/{img_name}.png').item()
                os.remove(f'static/{img_name}.png')
                final_result = extract_descriptive(int(predicted_class))
                await msg.answer(final_result)
        except:
            await msg.answer('I am not sure what sign it is. 🤗 Please try sending another photo.')
    
    url = 'https://memepedia.ru/wp-content/uploads/2020/09/b2b7c451cbddc634ecc0dc37031fb4d6.jpg'
    response = requests.get(url)
    with open('temp.jpg', 'wb') as f:
        f.write(response.content)
    await msg.answer_photo(photo=open('temp.jpg', 'rb'))

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)