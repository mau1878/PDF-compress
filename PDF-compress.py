import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from pdf2image import convert_from_bytes
from PIL import Image
import io

# Function to resize PDF pages
def resize_pdf(input_pdf, scale_percentage):
    # Read the input PDF
    pdf_reader = PdfReader(input_pdf)
    
    # Convert PDF pages to images
    images = convert_from_bytes(input_pdf.read())

    # List to store resized images
    resized_images = []

    # Resize each image based on the scale percentage
    for image in images:
        width, height = image.size
        new_width = int(width * scale_percentage / 100)
        new_height = int(height * scale_percentage / 100)
        resized_image = image.resize((new_width, new_height), Image.ANTIALIAS)
        resized_images.append(resized_image)

    # Convert the resized images back to PDF
    output_pdf_stream = io.BytesIO()
    resized_images[0].save(output_pdf_stream, save_all=True, append_images=resized_images[1:], format='PDF')

    return output_pdf_stream

# Streamlit UI
st.title("PDF Size Reducer")

# Upload PDF file
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    # Scale input
    scale = st.slider("Select size reduction percentage", min_value=10, max_value=100, value=50)
    
    if st.button("Reduce PDF Size"):
        # Resize the PDF
        output_pdf_stream = resize_pdf(uploaded_file, scale)
        
        # Create a download link for the reduced PDF
        st.success("PDF size reduced successfully!")
        st.download_button(label="Download Reduced PDF", data=output_pdf_stream, file_name="reduced_size.pdf", mime="application/pdf")
