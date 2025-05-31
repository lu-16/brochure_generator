# Apartment Brochure Generator

Generate a markdown-formatted brochure for any apartment complex website—just by providing its URL!

## Overview

This project scrapes the provided apartment website URL, uses an LLM (Large Language Model) to identify links relevant to apartment features (such as amenities, floorplans, gallery, etc.), and then generates a well-structured brochure based on the collected data.

## Features

- **Automatic Content Extraction:** Scrapes the apartment website for relevant information and links.
- **LLM-Powered Link Selection:** Uses an LLM agent to identify and select only the links that are relevant to apartment features.
- **Brochure Generation:** Another LLM agent organizes the extracted content into a markdown brochure with sections like Welcome, Floorplans, Amenities, Neighborhood, Gallery, and Contact.
- **Streamlit Web App:** User-friendly interface—just enter the apartment website URL and get your brochure!

## Usage

1. **Create and activate a virtual environment:**

   ```zsh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. **Install dependencies:**

   ```zsh
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**

   - Add your secrets to `.streamlit/secrets.toml` (see below for an example).

4. **Run the app:**

   ```zsh
   make start
   ```

5. **Enter the apartment website URL** in the app and let the system generate your brochure!

## Configuration

- **Secrets and API keys** are configured via `.streamlit/secrets.toml`:
  ```toml
  OPENAI_KEY = "your-key-here"
  OPENAI_ENDPOINT = "your-endpoint-here"
  OPENAI_MODEL = "your-model-name"
  ```
- Theme and UI can be customized in `.streamlit/config.toml`.

## License

Licensed under the Apache License 2.0.

---

**Note:** This project is for educational and demonstration purposes. Always respect website terms of service when scraping content.
