import streamlit as st
from PyPDF2 import PdfReader
import requests

uploaded_file = st.file_uploader("upload the file", type="pdf")

if uploaded_file:
    def extract_text_pdf(pdf_file):
        reader = PdfReader(pdf_file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text


    extracted_text = extract_text_pdf(uploaded_file)
    print(extracted_text)


def call_openAI(system_content, prompt):
    # Replace these with your actual values
    endpoint = "https://aihackfoundry.openai.azure.com"
    deployment_name = "gpt-4.1"  # e.g., gpt-35-turbo
    api_version = "2025-01-01-preview"  # Use the correct version as per your Azure config
    api_key = "1Wv5D123TqBcuXBu6eyX55vAAcLlIVsHdTBKZNhJmRloBgtCvy8aJQQJ99BEACfhMk5XJ3w3AAAAACOG401o"

    url = f"{endpoint}/openai/deployments/{deployment_name}/chat/completions?api-version={api_version}"

    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }

    data = {
        "messages": [
            {
                "role": "system",
                "content": system_content
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(url=url, headers=headers, json=data, verify=False)

    try:
        response = requests.post(url=url, headers=headers, json=data, verify=False)
        response.raise_for_status()
        result = response.json()

        # Extract only the assistant's message content
        content = result["choices"][0]["message"]["content"]
        print(content)
        return content

    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
        print(response.text)
    except Exception as err:
        print(f"An error occurred: {err}")


st.title("CID Masker - Powered by Open AI")
st.write("Welcome! This tool masks CID data")

if st.button("Mask CID data"):
    with st.spinner("Masking data.."):
        prompt = (f'Given the following user data : {extracted_text}, identify the CID data and masked it with "XXXX", '
                  f'Return only 2 section in tabular format, "Original Data" and "Masked Data" without any explanation.')
        system_prompt = "Act as a experienced analyst identifying CID data"
        insights = call_openAI(system_prompt, prompt)
        st.success("Generated Data")
        st.write(insights)
