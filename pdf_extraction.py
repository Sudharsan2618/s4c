import PyPDF2
import fitz  # PyMuPDF
import os
import csv
import subprocess

def extract_pdf_metadata(pdf_file_path):
    """
    Extracts metadata such as title, author, and creation date from a PDF file.

    Args:
        pdf_file_path (str): Path to the PDF file.

    Returns:
        dict: A dictionary containing the metadata (title, author, creation date, etc.)
    """
    try:
        with open(pdf_file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            metadata = reader.metadata
            total_pages = len(reader.pages)
        
        metadata_info = {
            'title': metadata.title,
            'author': metadata.author,
            'subject': metadata.subject,
            'creator': metadata.creator,
            'producer': metadata.producer,
            'creation_date': metadata.get('/CreationDate', None),
            'modification_date': metadata.get('/ModDate', None),
            'page_count': total_pages
        }
        print(f"Extracted metadata: {metadata_info}")
        return metadata_info
    except Exception as e:
        print(f"Error extracting PDF metadata: {e}")
        return None

def extract_text_from_pdf(pdf_file_path):
    """
    Extracts plain text content from a PDF.

    Args:
        pdf_file_path (str): Path to the PDF file.

    Returns:
        str: Extracted text content.
    """
    try:
        text_content = "Hi"  # Placeholder for actual extraction logic
        print(f"Extracted text: {text_content[:100]}...")  # Show a snippet of the text
        return text_content
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def convert_pdf_to_xml(pdf_file_path, xml_output_path):
    """
    Converts a PDF file to XML format using the pdftohtml tool.

    Args:
        pdf_file_path (str): Path to the PDF file.
        xml_output_path (str): Path to save the output XML file.

    Returns:
        str: The content of the XML file.
    """
    try:
        command = f"pdftohtml -xml {pdf_file_path} {xml_output_path}"
        subprocess.run(command, shell=True, check=True)
        
        with open(xml_output_path, 'r', encoding='utf-8') as xml_file:
            xml_content = xml_file.read()
        
        print(f"XML content saved to {xml_output_path}")
        return xml_content
    except subprocess.SubprocessError as e:
        print(f"PDF conversion failed: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error during PDF to XML conversion: {e}")
        return None

def extract_images_and_context(pdf_file_path, output_folder="extracted_images"):
    """
    Extracts images and their surrounding context (text) from the PDF, saving results to a CSV file.

    Args:
        pdf_file_path (str): Path to the PDF file.
        output_folder (str): Folder to store extracted images.

    Returns:
        str: Path to the generated CSV file containing image names and context.
    """
    try:
        os.makedirs(output_folder, exist_ok=True)
        csv_file_path = "image_context.csv"
        csv_headers = ["image_name", "title", "text_before", "text_after"]

        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_headers)
            writer.writeheader()

            pdf_document = fitz.open(pdf_file_path)
            print(f"Extracting images and context from {pdf_file_path}...")
            
            for page_num in range(len(pdf_document)):
                page = pdf_document[page_num]
                text_blocks = page.get_text("blocks")
                image_list = page.get_images()

                for img_index, image in enumerate(image_list):
                    xref = image[0]
                    base_image = pdf_document.extract_image(xref)
                    
                    if base_image:
                        image_name = f"image_p{page_num + 1}_{img_index + 1}.{base_image['ext']}"
                        image_path = os.path.join(output_folder, image_name)
                        
                        with open(image_path, "wb") as image_file:
                            image_file.write(base_image["image"])
                        
                        image_rect = None
                        for img_info in page.get_images(full=True):
                            if img_info[0] == xref:
                                image_rect = page.get_image_bbox(img_info)
                                break
                        
                        if image_rect:
                            title, text_before, text_after = "", "", ""
                            for block in text_blocks:
                                block_rect = fitz.Rect(block[:4])
                                if block_rect.y1 < image_rect.y0:
                                    title = block[4] if abs(block_rect.y1 - image_rect.y0) < 50 else text_before + block[4] + " "
                                elif block_rect.y0 > image_rect.y1:
                                    text_after += block[4] + " "
                            
                            writer.writerow({
                                "image_name": image_name,
                                "title": title.strip(),
                                "text_before": text_before.strip(),
                                "text_after": text_after.strip()
                            })
            pdf_document.close()

        print(f"Image context CSV generated at: {csv_file_path}")
        return csv_file_path
    except Exception as e:
        print(f"Error extracting images and context: {e}")
        return None
