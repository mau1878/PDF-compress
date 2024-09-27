import streamlit as st
import fitz  # PyMuPDF
import io

def compress_pdf(input_pdf, scale_percentage):
    # Load the PDF
    pdf_document = fitz.open(stream=input_pdf.read(), filetype="pdf")
    
    # Output PDF
    output_pdf_stream = io.BytesIO()
    
    # Write the new PDF to the output stream
    writer = fitz.Document()

    # Loop through each page and compress
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        pix = page.get_pixmap(matrix=fitz.Matrix(scale_percentage / 100, scale_percentage / 100))  # Resize page
        img_bytes = pix.tobytes(output="png")
        
        # Create a new page in the writer object from the image
        img_pdf = fitz.open(stream=img_bytes, filetype="png")
        writer.insert_pdf(img_pdf)
    
    # Save the compressed PDF
    writer.save(output_pdf_stream)
    writer.close()
    
    return output_pdf_stream

# Streamlit UI
st.title("PDF Size Reducer")

# Upload PDF file
uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

if uploaded_file:
    # Scale input
    scale = st.slider("Select size reduction percentage", min_value=10, max_value=100, value=50)
    
    if st.button("Reduce PDF Size"):
        # Compress the PDF
        output_pdf_stream = compress_pdf(uploaded_file, scale)
        
        # Create a download link for the compressed PDF
        st.success("PDF size reduced successfully!")
        st.download_button(label="Download Reduced PDF", data=output_pdf_stream.getvalue(), file_name="reduced_size.pdf", mime="application/pdf")
