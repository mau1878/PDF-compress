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
            
            # Create a Pillow image from the extracted image bytes
            img = Image.open(io.BytesIO(img_bytes))
            
            # Calculate new dimensions
            new_width = int(img.width * (scale_percentage / 100))
            new_height = int(img.height * (scale_percentage / 100))
            
            # Resize the image using Pillow with LANCZOS filter
            img = img.resize((new_width, new_height), Image.LANCZOS)
            
            # Convert back to BytesIO
            img_bytes_io = io.BytesIO()
            img.save(img_bytes_io, format='PNG')  # Save as PNG or JPEG
            img_bytes_io.seek(0)  # Move to the start of the BytesIO
            
            # Replace the image in the PDF correctly
            page.replace_image(xref, img_bytes_io.getvalue())  # Correct usage with xref and image bytes
        
        # Add the updated page to the new writer
        writer.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
    
    # Save the compressed PDF to the output stream
    writer.save(output_pdf_stream)
    writer.close()
    
    # Move the output stream to the start
    output_pdf_stream.seek(0)
    
    return output_pdf_stream
