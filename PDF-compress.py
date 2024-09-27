import streamlit as st
import fitz  # PyMuPDF
import io

def compress_pdf(input_pdf, scale_percentage):
    # Convert Streamlit UploadedFile to BytesIO
    input_pdf_stream = io.BytesIO(input_pdf.read())  # Convert to BytesIO
    input_pdf_stream.seek(0)  # Move to the start of the file stream
    
    # Load the PDF from the input stream
    pdf_document = fitz.open(stream=input_pdf_stream, filetype="pdf")
    
    # Output PDF stream
    output_pdf_stream = io.BytesIO()
    
    # Create a new PDF writer object
    writer = fitz.open()

    # Loop through each page in the PDF
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        
        # Extract the images and compress them
        img_list = page.get_images(full=True)
        for img_index, img in enumerate(img_list):
            xref = img[0]
            base_image = pdf_document.extract_image(xref)
            img_bytes = base_image["image"]
            
            # Create a Pixmap directly from the image bytes
            img_pix = fitz.Pixmap(img_bytes)
            
            # Create a scaling matrix
            scale_matrix = fitz.Matrix(scale_percentage / 100, scale_percentage / 100)
            
            # Scale the pixmap using the matrix to create a new scaled pixmap
            scaled_pix = fitz.Pixmap(img_pix, img_pix.alpha)  # Retain alpha channel if exists
            scaled_pix = scaled_pix.resample(scale_matrix)  # Resample the image with the scale matrix

            # Replace the image in the PDF
            page.replace_image(xref, scaled_pix)
        
        # Add the updated page to the new writer
        writer.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
    
    # Save the compressed PDF to the output stream
    writer.save(output_pdf_stream)
    writer.close()
    
    # Move the output stream to the start
    output_pdf_stream.seek(0)
    
    return output_pdf_stream

# Streamlit UI
st.title("PDF Size Reducer")

# Upload PDF file
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    # Scale input
    scale = st.slider("Select image reduction percentage", min_value=10, max_value=100, value=50)
    
    if st.button("Reduce PDF Size"):
        # Compress the PDF
        output_pdf_stream = compress_pdf(uploaded_file, scale)
        
        # Create a download link for the compressed PDF
        st.success("PDF size reduced successfully!")
        st.download_button(label="Download Reduced PDF", data=output_pdf_stream, file_name="reduced_size.pdf", mime="application/pdf")
