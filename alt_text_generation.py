from langchain import HuggingFaceHub
import os
import pandas as pd
from PIL import Image

def generate_alt_text_for_image(image_path, title, text_before, text_after):
    """
    Generates alternative text for an image using a HuggingFace language model.

    Args:
        image_path (str): Path to the image file.
        title (str): Title of the image.
        text_before (str): Text before the image.
        text_after (str): Text after the image.

    Returns:
        str: The generated alternative text for the image.
    """
    try:
        HUGGINGFACEHUB_API_TOKEN = "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"
        
        # Initialize the HuggingFaceHub model
        llm_model = HuggingFaceHub(
            repo_id="mistralai/Mistral-7B-Instruct-v0.2",
            model_kwargs={'temperature': 0.5, 'max_new_tokens': 100},
            huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN
        )
        
        prompt = f"""
        You are given an image with a title and context. The image is named: {image_path}.
        Title: {title}
        Text before the image: {text_before}
        Text after the image: {text_after}
        
        Generate a one-liner alternative text that describes the image in a meaningful way.
        """
        
        response = llm_model(prompt)
        split_response = response.split("Generate a one-liner alternative text that describes the image in a meaningful way.")
        alt_text = split_response[-1].strip()
        
        print(f"Generated alt text for {image_path}: {alt_text}")
        return alt_text
    except Exception as e:
        print(f"Error generating alt text for image {image_path}: {e}")
        return "Alternative text not available"

def process_csv_and_generate_alt_texts(input_csv, output_csv):
    """
    Processes a CSV file containing image context and generates alternative text for each image.

    Args:
        input_csv (str): Path to the input CSV file with image context.
        output_csv (str): Path to save the updated CSV with alt text.
    """
    try:
        df = pd.read_csv(input_csv)
        updated_rows = []

        for _, row in df.iterrows():
            image_name = row['image_name']
            title = row.get('title', '')
            text_before = row.get('text_before', '')
            text_after = row.get('text_after', '')
            image_path = os.path.join('extracted_image', image_name)

            alt_text = generate_alt_text_for_image(image_path, title, text_before, text_after)
            updated_row = row.to_dict()
            updated_row['alt_text'] = alt_text
            updated_rows.append(updated_row)

        updated_df = pd.DataFrame(updated_rows)
        updated_df.to_csv(output_csv, index=False)
        print(f"Alt text updated and saved to {output_csv}")
    except Exception as e:
        print(f"Error processing CSV and generating alt texts: {e}")
