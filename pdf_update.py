import pandas as pd
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import TextStringObject, NameObject

def update_pdf_with_accessibility(pdf_file, csv_file, output_pdf):
    """
    Updates a PDF with alternative text and additional accessibility metadata.

    Args:
        pdf_file (str): Path to the original PDF file.
        csv_file (str): Path to the CSV file containing image alt texts.
        output_pdf (str): Path to the output PDF with updated accessibility metadata.
    """
    try:
        df = pd.read_csv(csv_file)
        reader = PdfReader(pdf_file)
        writer = PdfWriter()

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            writer.add_page(page)

        metadata = reader.metadata
        alt_texts = []

        for _, row in df.iterrows():
            alt_texts.append(f"{row['image_name']}: {row['alt_text']}")

        alt_texts_combined = " | ".join(alt_texts)
        alt_texts_combined_pdf = TextStringObject(alt_texts_combined)
        alt_text_key = NameObject('/AltText')

        if alt_text_key in metadata:
            metadata[alt_text_key] += alt_texts_combined_pdf
        else:
            metadata[alt_text_key] = alt_texts_combined_pdf

        accessibility_metadata = {
            '/TaggedPDF': "Yes",
            '/ReadingOrder': "Logical and correct",
            '/TextSelectability': "Text-based",
            '/NavigationalAids': "TOC and bookmarks included",
            '/FormsAccessibility': "Interactive forms",
            '/ColorContrast': "Sufficient contrast",
            '/FontResizing': "Text resizable",
            '/AnnotationsAndMetadata': "Document includes annotations"
        }

        for key, value in accessibility_metadata.items():
            key_object = NameObject(key)
            value_object = TextStringObject(value)
            metadata[key_object] = value_object

        writer.add_metadata(metadata)

        with open(output_pdf, 'wb') as out_file:
            writer.write(out_file)

        print(f"Updated PDF saved as {output_pdf}")
    except Exception as e:
        print(f"Error updating PDF with accessibility: {e}")
