import streamlit as st
import io
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont


st.title('顔認識アプリ')
st.write('顔が映った写真を選択してください')

subscription_key = 'f14388306ac943138e3ea3b7d684f960'
assert subscription_key
face_api_url = 'https://20220111soya.cognitiveservices.azure.com/face/v1.0/detect'

uploaded_file = st.file_uploader("Choose an image...", type="jpg")
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue() #バイナリ取得
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key
    }

    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
    }

    res = requests.post(face_api_url, params=params, headers=headers, data=binary_img)
    results = res.json()
    for result in results:
        rect = result['faceRectangle']
        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'], rect['top']), (rect['left']+rect['width'], rect['top']+rect['height'])], fill=None, outline='green', width=5) 
        atr = result['faceAttributes']
        emo = atr['emotion']
        neu = emo['neutral']
        con = neu * 100
        conc = str(con)        
        textsize = 50
        font = ImageFont.truetype("Arial.ttf", size=textsize)
        txpos = (rect['left'],rect['top']-textsize-5)
        draw.text(txpos, conc, font=font, fill='white')
    st.image(img, caption="Uploaded image.", use_column_width=True)
