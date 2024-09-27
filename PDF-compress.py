import streamlit as st
import fitz  # PyMuPDF
import io

def compress_pdf(input_pdf, scale_percentage):
    # Load the PDF
    pdf_document = fitz.open(stream=input_pdf.read(), filetype="pdf")
    
    # Output PDF stream
    output_pdf_stream = io.BytesIO()
    
    # Create a new PDF writer object
    writer = fitz.open()

    # Loop through each page in the PDF and resize
    for page_num in range(len(pdf_document)):
        page = pdf_document.load_page(page_num)
        
        # Resize the page to a smaller size
        mat = fitz.Matrix(scale_percentage / 100, scale_percentage / 100)  # Scale matrix
        pix = page.get_pixmap(matrix=mat)  # Get image of the resized page
        
        # Create a new page in the writer with the size of the resized image
        new_page = writer.new_page(width=pix.width, height=pix.height)
        
        # Insert the image into the new page
        new_page.insert_image(fitz.Rect(0, 0, pix.width, pix.height), pixmap=pix)
    
    # Save the compressed PDF to the output stream
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
