# AI-Powered Schema Selection for NL to SQL Pipelines

## Overview

This Streamlit app uses Google Gemini AI to analyze a database schema and extract relevant tables based on a natural language query.

## Features

- Upload a database schema in JSON/YAML format.
- Input a natural language query.
- Get relevant tables and columns from the schema.
- Debugging support with raw AI responses.

## Installation

1. **Clone the Repository**:
   ```sh
   git clone
   cd schema-nl2sql
   ```
2. **Create a Virtual Environment (Optional)**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate  # Windows
   ```
3. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```
4. **Set Up API Key**:
   Create a `.env` file and add your Google API key:
   ```sh
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Usage

1. **Run the App**:
   ```sh
   streamlit run app.py
   ```
2. **Upload a Schema File** (JSON/YAML).
3. **Enter a Query** and click "Enter".
4. **View Extracted Schema Information**.

## Example Schema

```json
{
  "students": {
    "columns": ["id", "name", "age", "grade"],
    "primary_key": "id"
  }
}
```

## Debugging

- **Missing API Key?** Check `.env` file.
- **Invalid JSON Response?** Review raw AI output.
- **Schema Not Loading?** Ensure correct file format.

## License

MIT License.
