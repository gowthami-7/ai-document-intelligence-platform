## 🚀 Live Demo

[🌐 Click here to open my AI Document Intelligence Platform](https://ai-document-intelligence-platform-g8fcvuspks4wnxutkilsne.streamlit.app/)
\# AI-Powered Generative Content \& Document Intelligence Platform



\## Project Overview



The AI-Powered Generative Content \& Document Intelligence Platform is a Python-based interactive web application developed to process user-provided documents and generate useful, structured AI outputs.



The application combines document intelligence, natural language processing, prompt engineering, and Generative AI to support document summarization, information extraction, classification, context-aware analysis, and content generation.



It also provides output validation, quality evaluation, and downloadable PDF and PowerPoint outputs.



\---



\## Project Objectives



The system is designed to:



\- Ingest and preprocess text-based documents.

\- Understand user requirements along with document content.

\- Generate structured outputs using Generative AI.

\- Provide prompt-based summarization, extraction, classification, and content generation.

\- Support context-aware multi-step document analysis.

\- Validate generated outputs using automated checks.

\- Evaluate outputs using relevance, consistency, and factuality indicators.

\- Provide an interactive interface for document submission and result review.

\- Allow generated results to be downloaded for further use.



\---



\## Key Features



\### 1. Document Ingestion



Supported document formats:



\- PDF

\- DOCX

\- TXT



The uploaded document is extracted and converted into text before AI processing.



\### 2. Document Summarization



Generates a structured summary based on the uploaded document and the user's requirement.



\### 3. Information Extraction



Extracts relevant information such as:



\- Document type

\- People

\- Organizations

\- Dates

\- Locations

\- Key facts

\- Important terms

\- Important numbers and statistics



\### 4. Document Classification



Classifies the document into an appropriate category and provides:



\- Category

\- Confidence level

\- Reasoning

\- Supporting indicators



\### 5. Context-Aware Document Analysis



Provides a combined analysis containing:



\- Summary

\- Document type

\- Entities

\- Key facts

\- Context

\- Recommended next steps



\### 6. Generative Content



Generates requested content based on the uploaded document and user requirement.



The application can also generate complete slide-by-slide presentation content when a presentation or PowerPoint is requested.



\### 7. Output Validation



Generated responses are checked for:



\- Non-empty output

\- Minimum response length

\- Availability of source document

\- Response detail



\### 8. Quality Evaluation



The application provides automated heuristic indicators for:



\- Relevance

\- Consistency

\- Factuality

\- Overall quality



These are automated indicators intended for application-level quality checking and are not a scientifically validated factuality benchmark.



\### 9. Output Formats



Generated results can be downloaded as:



\- PDF

\- PowerPoint presentation (.pptx)



\---



\## Technology Stack



\### Frontend / User Interface



\- Streamlit



\### Application Logic



\- Python



\### Document Processing



\- pypdf

\- python-docx

\- Python file handling



\### Generative AI



\- OpenRouter API

\- OpenAI-compatible Python client



\### Output Generation



\- ReportLab for PDF generation

\- python-pptx for PowerPoint generation



\### Environment Configuration



\- python-dotenv



\---



\## System Workflow



The application follows this workflow:



1\. User

2\. Document Upload

3\. Document Ingestion

4\. Text Preprocessing

5\. User Requirement

6\. Requirement-Aware Prompt Construction

7\. Generative AI

8\. Structured Output

9\. Output Validation

10\. Quality Evaluation

11\. Result Review and Download



\---



\## Project Structure



```text

project1-final-submission/

|

|-- .env.example

|-- .gitignore

|-- README.md

|-- requirements.txt

|

`-- app/

&#x20;   |

&#x20;   |-- main.py

&#x20;   |

&#x20;   |-- prompts/

&#x20;   |

&#x20;   |-- services/

&#x20;   |   |-- ai\_service.py

&#x20;   |   `-- quality\_service.py

&#x20;   |

&#x20;   `-- utils/

