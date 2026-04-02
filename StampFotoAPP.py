import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from io import BytesIO

st.title("Stamp Foto Dokumentasi BUMDES")

# fungsi untuk memecah teks agar turun baris
def wrap_text(draw, text, font, max_width):
    lines = []
    words = text.split(" ")
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        bbox = font.getbbox(test_line)
        width = bbox[2] - bbox[0]

        if width <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "

    lines.append(current_line.strip())
    return lines


uploaded_file = st.file_uploader("Upload Foto", type=["jpg","jpeg","png"])

bumdes = st.text_input("Nama BUMDES")
lokasi = st.text_input("Lokasi / Alamat")
keterangan = st.text_input("Keterangan")

if uploaded_file and bumdes and lokasi and keterangan:

    img = Image.open(uploaded_file)
    draw = ImageDraw.Draw(img)

    # ukuran font otomatis
    font_size = int(min(img.width, img.height) / 28)
    font_size = max(20, min(font_size, 55))

    try:
        font = ImageFont.truetype("DejaVuSans-Bold.ttf", font_size)
    except:
        font = ImageFont.load_default()

    now = datetime.now()
    tanggal = now.strftime("%d-%m-%Y")
    jam = now.strftime("%H:%M:%S")

    max_text_width = int(img.width * 0.9)

    # auto wrap lokasi & keterangan
    lokasi_lines = wrap_text(draw, f"LOKASI : {lokasi}", font, max_text_width)
    ket_lines = wrap_text(draw, f"KETERANGAN : {keterangan}", font, max_text_width)

    lines = []
    lines.append(f"BUMDES : {bumdes}")
    lines.extend(lokasi_lines)
    lines.extend(ket_lines)
    lines.append(f"TANGGAL : {tanggal}")

    # hitung ukuran teks
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

    # kotak background
    draw.rectangle(
        (x-padding, y-padding, x+max_width+padding, y+total_height+padding),
        fill=(0,0,0)
    )

    # tulis teks
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

    # nama file otomatis dari BUMDES
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
