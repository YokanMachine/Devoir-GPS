# Devoir-GPS

This app reads **EXIF GPS data** from photos and shows where they were taken on a **map**.
If several photos were taken on the same day, it connects them with a line showing your route.

---

## Features

- Upload photos
- Extract EXIF metadata (GPS coordinates)
- Show each photo’s position on an interactive map
- Connect photos from the same day to form a path

---

## Requirements

Install the following before running:

```bash
pip install streamlit pillow folium pandas
```

---

## Run the app

```bash
streamlit run main.py
```

Then open your browser at [http://localhost:8501](http://localhost:8501)

---

## Notes

- Turn on location when taking photos
- Avoid sending images through WhatsApp or Discord (they remove EXIF data)
- Use USB or direct transfer to keep metadata

---

## Credits

- EXIF info: [Adobe](https://www.adobe.com/creativecloud/file-types/image/raster/exif-file.html)
- Pillow EXIF: [Docs](https://pillow.readthedocs.io/en/stable/reference/ExifTags.html)
- Streamlit: [Docs](https://docs.streamlit.io/get-started)
- GPS data extraction: [Stack Overflow](https://stackoverflow.com/questions/72530975/extract-gps-data-using-python-and-pil-is-failing)
- Decimal Degrees: [Wikipedia](https://en.wikipedia.org/wiki/Decimal_degrees)