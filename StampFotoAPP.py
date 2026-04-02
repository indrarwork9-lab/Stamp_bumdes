import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from io import BytesIO
import textwrap

st.title("Stamp Foto Dokumentasi BUMDES")

uploaded_file = st.file_uploader("Upload Foto", type=["jpg","jpeg","png"])

bumdes = st.text_input("Nama BUMDES")
lokasi = st.text_input("Lokasi")
keterangan = st.text_input("Keterangan")

if uploaded_file and bumdes and lokasi and keterangan:

    img = Image.open(uploaded_file)
    draw = ImageDraw.Draw(img)

    # AUTO RESIZE FONT
    font_size = int(min(img.width, img.height) / 28)
    font_size = max(20, min(font_size, 55))

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()

    now = datetime.now()
    tanggal = now.strftime("%d-%m-%Y")
    jam = now.strftime("%H:%M:%S")

    # WRAP TEXT AGAR RAPI
    wrap_width = 40
    ket_wrap = "\n".join(textwrap.wrap(keterangan, wrap_width))

    text = (
        f"BUMDES : {bumdes}\n"
        f"LOKASI : {lokasi}\n"
        f"KETERANGAN : {ket_wrap}\n"
        f"TANGGAL : {tanggal}    JAM : {jam}"
    )

    lines = text.split("\n")

    # HITUNG UKURAN TEKS
    max_width = 0
    total_height = 0

    for line in lines:
        bbox = font.getbbox(line)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        if w > max_width:
            max_width = w

        total_height += h + 5

    padding = int(font_size / 2)

    x = int(img.width * 0.02)
    y = img.height - total_height - (padding * 3)

    # BACKGROUND KOTAK
    draw.rectangle(
        (x-padding, y-padding, x+max_width+padding, y+total_height+padding),
        fill=(0,0,0)
    )

    # TULIS TEKS
    current_y = y
    for line in lines:
        draw.text((x, current_y), line, fill="white", font=font)
        bbox = font.getbbox(line)
        line_height = bbox[3] - bbox[1]
        current_y += line_height + 5

    st.image(img)

    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    buffer.seek(0)

    # NAMA FILE OTOMATIS
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
