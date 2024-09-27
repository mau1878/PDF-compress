import streamlit as st
from pdf2image import convert_from_bytes
from PIL import Image
import io

# Function to reduce PDF file size
def reduce_pdf_file_size(pdf_bytes, downsizing_percentage):
  # Convert PDF to images
  images = convert_from_bytes(pdf_bytes)

  # Resize images
  resized_images = []
  for image in images:
      width, height = image.size
      new_width = int(width * (1 - downsizing_percentage / 100))
      new_height = int(height * (1 - downsizing_percentage / 100))
      resized_image = image.resize((new_width, new_height))
      resized_images.append(resized_image)

  # Convert resized images back to a PDF
  pdf_buffer = io.BytesIO()
  images[0].save(pdf_buffer, "PDF", resolution=100.0, save_all=True, append_images=images[1:])
  pdf_buffer.seek(0)

  return pdf_buffer.read()

# Streamlit app
st.title("PDF File Size Reducer")

downsizing_percentage = st.number_input("Enter the downsizing percentage (1-100):", min_value=1, max_value=100)

uploaded_file = st.file_uploader("Choose a PDF file:", type=["pdf"])

if uploaded_file is not None:
  pdf_bytes = uploaded_file.read()
  reduced_pdf_bytes = reduce_pdf_file_size(pdf_bytes, downsizing_percentage)
  st.download_button("Download reduced PDF", reduced_pdf_bytes, "reduced_pdf.pdf")
