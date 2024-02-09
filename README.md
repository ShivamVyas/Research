# Test Engineering Model Prototype

## Introduction
This prototype is designed for organizations to fine-tune their test engineering processes and needs. It integrates Python programming with OpenAI's GPT-4, enabling users to input test engineering queries and receive comprehensive responses, aiding in test case development and automation of repetitive testing tasks.

## Features
- **Integration with OpenAI GPT-4**: Leverages OpenAI Model for processing test engineering queries.
- **Automated Test Case Generation**: Provides code templates for efficient and accurate automated testing.
- **Multi-format Document Parsing**: Supports PDF and DOCX files.
- **Custom User Interface**: Interactive and user-friendly interface using Streamlit.

## Installation
1. **Python Requirements**: Ensure Python is installed on your system.
2. **Install Dependencies**: Use the provided `requirements.txt` to install necessary libraries. Run the following command in your terminal:
   ```bash
   pip install -r requirements.txt

This command installs all required libraries such as streamlit, urllib, Pillow, docx2txt, PyPDF2, dotenv, and langchain.
3. Environment Variables: Set up an .env file with your OpenAI API key.

## Usage
1. **Setup Terminal:** C:\...\Summer-Research-1.1>
2. **Launch Streamlit UI:** Execute the following script in terminal to initiate the Streamlit interface.
   ```bash
   streamlit run app.py
3. **API Key Configuration:** Input your OpenAI API key in the Streamlit sidebar.
4. **Document Upload (Optional):** Upload PDF or DOCX files for analysis.
5. **Querying:** Submit test engineering queries to obtain responses and code templates.

## How It Works
The prototype integrates various Python libraries and OpenAI's GPT-4 model.
It processes user queries related to test engineering using uploaded documents.
Generates responses and code templates tailored for test cases.

## Customization
You can modify the Streamlit UI styles using the top bar in the application.
Adjust GPT models within app.py for different response details or specificities.

## Support
For any issues or queries, please refer to the documentation of the libraries used.

## License

### MIT License

Copyright (c) 2023 Shivam Vyas
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

> [!WARNING]
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

### OpenAI API Terms
Usage of the OpenAI API, as integrated into this project, is subject to [OpenAI's terms and conditions](https://openai.com/api/policies/terms/). By using this project, you agree to comply with all terms set forth by OpenAI for API usage. It is the responsibility of the individual or organization using this project to ensure compliance with these terms.

> [!NOTE]
> OpenAI's API terms include guidelines on data usage, privacy, and restrictions on certain types of content. Users of this project should review these terms in detail to understand their obligations and restrictions.
