import os
original_path = os.environ.get('PATH', '')
new_dir = "/opt/homebrew/bin"

# Update PATH by appending the new directory
new_path = f"{original_path}:{new_dir}"
os.environ['PATH'] = new_path

print(f"Updated PATH: {new_path}")
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from pdf2image import convert_from_path
from PIL import Image


def get_pdf_size(file_path):
    """
    Get the size of a PDF file in KB and MB.

    Args
        file_path (str): The path to the PDF file.

    Returns:
        tuple: File size in KB and MB.
    """
    file_size = os.path.getsize(file_path)
    size_in_kb = file_size / 1024
    size_in_mb = size_in_kb / 1024
    return size_in_kb, size_in_mb


def lower_quality_of_pdf(input_file_path, output_file_path, quality):
    """
    Convert a PDF to images, lower the quality of the images, and then convert the images back to PDF.

    Args:
        input_file_path (str): The path to the input PDF file.
        output_file_path (str): The path to the output PDF file.
        quality (int): The compression quality of the images (1 to 100, where 100 is highest quality).
    """
    # Convert the PDF to images
    images = convert_from_path(input_file_path)

    # List to store the paths of lower quality images
    lower_quality_image_paths = []

    # Lower the quality of each image
    for i, image in enumerate(images):
        # Create a lower-quality image file path
        lower_quality_image_path = f"temp_image_{i}.jpg"
        
        # Save the image with lower quality
        image.save(lower_quality_image_path, 'JPEG', quality=quality)
        
        # Append the path to the list
        lower_quality_image_paths.append(lower_quality_image_path)

    # Create a new PDF file
    pdf_writer = PdfWriter()

    # Add each lower-quality image as a page in the PDF
    # Add each lower-quality image as a page in the PDF
    for image_path in lower_quality_image_paths:
        # Open the image
        img = Image.open(image_path)
        
        # Convert the image to PDF format
        img_pdf = img.convert('RGB')
        
        # Create a temporary PDF file path
        temp_pdf_path = f"temp_pdf_{image_path}.pdf"
        
        # Save the image as a PDF
        img_pdf.save(temp_pdf_path)
        
        # Read the temporary PDF file and add it to the output PDF
        with open(temp_pdf_path, 'rb') as temp_pdf_file:
            temp_pdf_reader = PdfReader(temp_pdf_file)
            for page in temp_pdf_reader.pages:
                # Add the page to the output PDF
                pdf_writer.add_page(page)

        # Remove the temporary PDF file
        os.remove(temp_pdf_path)


    # Save the new PDF file
    with open(output_file_path, 'wb') as output_pdf_file:
        pdf_writer.write(output_pdf_file)

    # Clean up the lower-quality image files
    for image_path in lower_quality_image_paths:
        os.remove(image_path)

    print(f"Lower quality PDF saved to: {output_file_path}")



def main():
    # Declare the file paths
    file_path = "/Users/rotemduvdevani/Documents/Personal Projects/Assignment01.pdf"
    output_file_path = "/Users/rotemduvdevani/Documents/Personal Projects/11Assignment01.pdf"

    # Get PDF file size
    kb, mb = get_pdf_size(file_path)
    print(f"PDF file size: {kb:.2f} KB / {mb:.2f} MB")

   

    # Quality level (1 to 100, where 100 is highest quality)
    quality = 20

    # Call the function to lower the quality of the PDF
    lower_quality_of_pdf(file_path, output_file_path, quality)

    outkb, outmb = get_pdf_size(output_file_path)
   

    if outmb > 30:
        lower_quality_of_pdf(output_file_path,output_file_path,quality)

    print(f"PDF file size: {outkb:.2f} KB / {outmb:.2f} MB")
     


if __name__ == '__main__':
    main()
