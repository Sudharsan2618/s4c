from pdf_extraction import extract_pdf_metadata, extract_images_and_context
from alt_text_generation import process_csv_and_generate_alt_texts
from pdf_update import update_pdf_with_accessibility

def main(pdf_file_path):
    """
    Main function to execute the entire process: extract metadata, generate alt text, and update PDF.

    Args:
        pdf_file_path (str): Path to the PDF file to be processed.
    """
    try:
        metadata = extract_pdf_metadata(pdf_file_path)
        print("PDF Metadata:", metadata)

        csv_file_path = extract_images_and_context(pdf_file_path)
        print(f"Images and context data extracted to '{csv_file_path}'")

        input_csv = csv_file_path
        output_csv = input_csv.replace('.csv', '_with_alt_text.csv')
        process_csv_and_generate_alt_texts(input_csv, output_csv)
        print(f"Alt text generated and saved to '{output_csv}'")

        output_pdf = pdf_file_path.replace('.pdf', '_with_accessibility.pdf')
        update_pdf_with_accessibility(pdf_file_path, output_csv, output_pdf)
        print(f"Updated PDF saved as '{output_pdf}'")

    except Exception as e:
        print(f"Error in main execution: {e}")

if __name__ == "__main__":
    pdf_file_path = "sample2.pdf"
    main(pdf_file_path)
