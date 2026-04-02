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

    # AUTO RESIZE FONT STABIL
    font_size = int(min(img.width, img.height) / 30)
    font_size = max(20, min(font_size, 60))

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

    # HITUNG UKURAN TEKS (ANTI ERROR STREAMLIT CLOUD)
    text_width, text_height = draw.multiline_textsize(text, font=font)

    padding = int(font_size / 2)

    x = int(img.width * 0.02)
    y = img.height - text_height - (padding * 3)

    # KOTAK HITAM BACKGROUND
    draw.rectangle(
        (x-padding, y-padding, x+text_width+padding, y+text_height+padding),
        fill=(0,0,0)
    )

    # TULISAN
    draw.multiline_text((x,y), text, fill="white", font=font)

    st.image(img)

    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)

    # NAMA FILE DARI BUMDES
    nama_file = bumdes.replace(" ", "_")
    nama_file = "".join(c for c in nama_file if c.isalnum() or c == "_")

    timestamp = now.strftime("%Y%m%d_%H%M%S")

    file_name = f"{nama_file}_{timestamp}.jpg"

    st.download_button(
        "Download Foto",
        data=buffer,
        file_name=file_name,
        mime="image/jpeg"
    )
