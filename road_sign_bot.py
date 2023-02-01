#import libraries
import aiogram
import aiogram.utils
import asyncio
from aiogram.types import ContentType, Message, ParseMode
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
from datetime import datetime

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
        if crops[n]['conf'].item() > 0.8: # confidence level for detection
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
model2.load_state_dict(torch.load('weights2_new.pt', 
                                  map_location=torch.device('cpu')))
model2.eval()


# Load the dataset with classes
model2_df = pd.read_excel('classes_description.xlsx')
model2_df['class'] = pd.Series(model2_df['class']).astype('int')

# Function to classify iamges
def classify_photo(cropped_photo_path):
    transform = T.Compose([T.Resize((256, 256)), 
                           T.ToTensor()]) 
    img = Image.open(cropped_photo_path) 
    x = transform(img)
    x = x.unsqueeze(0) 
    output = model2(x.to('cpu')) 
    pred = torch.argmax(output, 1).item()
    pred_probability = torch.nn.functional.softmax(output, dim=1).max().item()
    return pred, pred_probability


# Function to extract description
def extract_descriptive(predicted_class):
    row = model2_df[model2_df['class']==predicted_class]
    print(row)
    return f"""CATEGORY: {row['category'].item()}, \nDESCRIPTION: {row['descriptive'].item()}"""

# Start command handler
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    user_name = message.from_user.username
    await message.reply(f"Hello, {user_name}! 🤖 I'm SignVision, your personal road sign detection expert. 🦾 Powered by AI and computer vision technologies, I can help you identify the road signs in your photos with just a snap. Let's get started! 🚦")


URI_INFO = f"https://api.telegram.org/bot{API_TOKEN}/getFile?file_id="
URI = f"https://api.telegram.org/file/bot{API_TOKEN}/"

if not os.path.exists('static'):
    os.mkdir('static')

async def delete_message(chat_id, message_id):
    # Delete the message with the specified ID
    await bot.delete_message(chat_id=chat_id, message_id=message_id)

url = 'https://memepedia.ru/wp-content/uploads/2020/09/b2b7c451cbddc634ecc0dc37031fb4d6.jpg'
response = requests.get(url)
with open('temp.jpg', 'wb') as f:
    f.write(response.content)

# Sent photo handler    
@dp.message_handler(content_types=['photo'])
async def classify(msg: types.Message):

    msg_to_delete1 = await bot.send_message(chat_id=msg.chat.id, text='Thinking...🤔')

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    full_name = msg.from_user.full_name
    user_name = msg.from_user.username
    with open("usernames.txt", "a") as file:
        file.write(f"{current_time}: {user_name} - {full_name} \n")

    file_id = msg.photo[-1].file_id
    resp = requests.get(URI_INFO + file_id)
    img_path = resp.json()['result']['file_path']
    img = requests.get(URI+img_path)
    img = Image.open(io.BytesIO(img.content))
    model1_crop = crop_photo(img)

    if len(model1_crop) == 0:
        await delete_message(chat_id=msg.chat.id, message_id=msg_to_delete1.message_id)
        await msg.answer('I cannot detect a sign. 🧐 Please try sending another photo.')

        msg_to_delete2 = await msg.answer_photo(photo=open('temp.jpg', 'rb'))
        await asyncio.sleep(1.5)
        await delete_message(chat_id=msg.chat.id, message_id=msg_to_delete2.message_id)
    elif len(model1_crop) >= 1:
        
        crops_left = len(model1_crop)
        
        for n in model1_crop:

            img_name = secrets.token_hex(8)
            n.save(f'static/{img_name}.png', format='PNG')
            photo=open(f'static/{img_name}.png', 'rb')

            predicted_class = classify_photo(f'static/{img_name}.png')[0]
            predicted_class_probability = classify_photo(f'static/{img_name}.png')[1]
            os.remove(f'static/{img_name}.png')
            final_description = extract_descriptive(int(predicted_class))
            
            try:
                await delete_message(chat_id=msg.chat.id, message_id=msg_to_delete1.message_id)
            except:
                None

            print(f'predicted_class_probability - {predicted_class_probability}')
            print('\n')

            if predicted_class_probability >= 0.65: # confidence level for classification
                crops_left -= 1
                await msg.answer_photo(photo)
                await msg.answer(final_description)
            elif predicted_class_probability < 0.6 and crops_left == 1:
                await msg.answer('I am not sure what sign it is. 🤗 Please try sending another photo.')
                
                msg_to_delete2 = await msg.answer_photo(photo=open('temp.jpg', 'rb'))
                await asyncio.sleep(1.5)
                await delete_message(chat_id=msg.chat.id, message_id=msg_to_delete2.message_id)
                

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=False)

