import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from io import BytesIO

st.title("Stamp Foto Dokumentasi BUMDES")

uploaded_file = st.file_uploader("Upload Foto", type=["jpg","jpeg","png"])

bumdes = st.text_input("Nama BUMDES")
lokasi = st.text_input("Lokasi")
keterangan = st.text_input("Keterangan")

if uploaded_file and bumdes and lokasi and keterangan:

    img = Image.open(uploaded_file)
    draw = ImageDraw.Draw(img)

    font_size = int(img.height / 25)

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()

    now = datetime.now()
    tanggal = now.strftime("%d-%m-%Y")
    jam = now.strftime("%H:%M:%S")

    text = (
        f"BUMDES : {bumdes}\n"
        f"LOKASI : {lokasi}\n"
        f"KETERANGAN : {keterangan}\n"
        f"TANGGAL : {tanggal}    JAM : {jam}"
    )

    bbox = draw.multiline_textbbox((0,0), text, font=font)

    text_width = bbox[2]-bbox[0]
    text_height = bbox[3]-bbox[1]

    padding = int(font_size / 2)

    x = int(img.width * 0.02)
    y = img.height - text_height - (padding * 3)

    draw.rectangle(
        (x-padding, y-padding, x+text_width+padding, y+text_height+padding),
        fill=(0,0,0)
    )

    draw.multiline_text((x,y), text, fill="white", font=font)

    st.image(img)

    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)

    st.download_button(
        "Download Foto",
        data=buffer,
        file_name="foto_dokumentasi.jpg",
        mime="image/jpeg"
    )
