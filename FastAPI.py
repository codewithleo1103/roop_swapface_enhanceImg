from fastapi import FastAPI, File
import re

# from get_information import get_extract_infor_id, save
import uvicorn
from starlette.requests import Request
import cv2
import glob
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import os
import base64
import time
from PIL import Image
from io import BytesIO
import string
from roop import core

import random 

# create env 
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

buff = BytesIO()
input_folder = "./data_input"
results = "./results"

@app.post("/generate_img")
def predict(request:Request,image:bytes = File(...)):
    if request.method == "POST":
        stringg = string.ascii_lowercase
        digits = string.digits
        name = ''
        for i in range(20):
            name += random.choice(stringg)
        name = f"{name}_{str(random.choice(digits))}"
        start_time = time.time()

        image = Image.open(BytesIO(image))
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) 
        cv2.imwrite(f"{input_folder}/{name}.jpg", image)
        all_template = glob.glob(f"./image_template_2/*")
        template_systhetic = random.choice(all_template)
        basename_systhetic = os.path.basename(template_systhetic).split('.')[0]
        basename_systhetic = re.sub(r'\d', '', basename_systhetic)
        try:
            out_img = core.test(image, template_systhetic)
            cv2.imwrite(f"{results}/{name}.jpg", out_img)
            _, buffer = cv2.imencode(".JPG", out_img)
            base64_img = base64.b64encode(buffer).decode()
        except:
            base64_img = None
        print(f"TIME EACH PROCESS IMAGE: {round(time.time()-start_time, 2)}")
        import torch
        torch.cuda.empty_cache()
        return {"msg": "success",
                "name_clothing": basename_systhetic,
                "image": base64_img}       

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0",port=5001)
