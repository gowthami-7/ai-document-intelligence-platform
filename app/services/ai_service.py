import os
import json
from dotenv import load_dotenv
from openai import OpenAI


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()


# ============================================================
# OPENROUTER CLIENT
# ============================================================

api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    raise ValueError(
        "OPENROUTER_API_KEY was not found in the .env file."
    )


client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)


MODEL = "openrouter/free"


# ============================================================
# BASIC AI RESPONSE
# ============================================================

def generate_ai_response(prompt):

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


# ============================================================
# COMMON DOCUMENT RULES
# ============================================================

DOCUMENT_RULES = """
IMPORTANT DOCUMENT RULES:

1. The uploaded document is the primary source of truth.
2. Do not invent names, dates, organizations, statistics,
   events, findings, quotations or facts.
3. Do not add information that is not supported by the document.
4. If requested information is not present, clearly say:
   "Not available in the document."
5. Follow the user's requirement exactly.
6. Respect requested audience, number of items, length,
   tone and format.
7. Do not merely describe what could be produced.
8. Actually produce the requested output.
9. Keep the output professional, useful and easy to read.
"""


# ============================================================
# PROMPT BUILDER
# ============================================================

def build_document_prompt(
    task,
    document_text,
    user_requirement=""
):

    return f"""
You are an advanced AI Document Intelligence system.

Your job is to perform the requested task using the uploaded
document as the primary source.

============================================================
USER REQUIREMENT
============================================================

{user_requirement if user_requirement.strip() else "No additional requirement provided."}

============================================================
TASK
============================================================

{task}

============================================================
DOCUMENT
============================================================

{document_text}

============================================================
RULES
============================================================

{DOCUMENT_RULES}

The user's requirement is not merely background information.

It is an instruction that must directly control your output.

For example:

If the user asks for a presentation:
- Actually create slide-by-slide content.
- Do not only provide a presentation outline.
- Follow the requested number of slides if specified.
- Adapt the language to the requested audience.
- Include only information supported by the document.

If the user asks for a summary:
- Actually summarize the document.
- Follow requested length and audience.

If the user asks for questions:
- Actually generate the requested questions.

If the user asks for notes:
- Actually create notes.

If the user asks for an explanation:
- Actually explain the content at the requested level.

Return the completed result, not instructions about how to create it.
"""


# ============================================================
# SUMMARIZATION
# ============================================================

def summarize_document(
    document_text,
    user_requirement=""
):

    task = """
Create a high-quality structured summary of the document.

Include:

1. Document Overview
2. Main Topics
3. Key Points
4. Important Findings
5. Conclusion

Modify the summary according to the user's requirement.
If the user requests a shorter, simpler, academic, professional
or audience-specific summary, follow that instruction.
"""

    prompt = build_document_prompt(
        task,
        document_text,
        user_requirement
    )

    return generate_ai_response(prompt)


# ============================================================
# INFORMATION EXTRACTION
# ============================================================

def extract_information(
    document_text,
    user_requirement=""
):

    task = """
Extract useful information from the document.

Use the following structure:

Document Type:
People:
Organizations:
Dates:
Locations:
Key Facts:
Important Terms:
Important Numbers or Statistics:

Only include information actually supported by the document.

If a requested category is unavailable, write:
"Not available in the document."

The user's requirement must determine which information
should receive priority.
"""

    prompt = build_document_prompt(
        task,
        document_text,
        user_requirement
    )

    return generate_ai_response(prompt)


# ============================================================
# CLASSIFICATION
# ============================================================

def classify_document(
    document_text,
    user_requirement=""
):

    task = """
Classify the document.

Choose exactly one primary category from:

- Academic/Research
- Business/Corporate
- Technical/Engineering
- Legal/Policy
- Financial
- Educational
- Medical/Healthcare
- News/Article
- Government/Administrative
- Other

Then provide:

Category:
Confidence:
Reasoning:
Supporting Indicators:

Use evidence from the document.

If the user requirement requests a specific classification
perspective, follow it.
"""

    prompt = build_document_prompt(
        task,
        document_text,
        user_requirement
    )

    return generate_ai_response(prompt)


# ============================================================
# PRESENTATION TASK
# ============================================================

PRESENTATION_TASK = """
The user has requested a PRESENTATION.

You must actually create presentation content.

Do NOT merely provide:
- a presentation idea
- a presentation outline
- suggestions for slides
- instructions for making slides

Instead, create the complete slide-by-slide presentation content.

IMPORTANT OUTPUT FORMAT:

SLIDE 1: <slide title>
CONTENT:
- <concise point>
- <concise point>
- <concise point>

SLIDE 2: <slide title>
CONTENT:
- <concise point>
- <concise point>
- <concise point>

Continue until the complete presentation is finished.

If the user specifies a number of slides, follow it exactly.

If the user does not specify a number, choose an appropriate
number based on the document.

Keep slide content concise and presentation-friendly.

Do not put long paragraphs on slides unless the user's
requirement specifically asks for them.

The presentation should have a logical flow such as:

1. Title / Introduction
2. Background or Context
3. Main Topics
4. Important Information
5. Key Findings
6. Analysis / Discussion
7. Important Evidence
8. Conclusion

Adjust the structure according to the actual document.

If the user specifies an audience such as:
- college students
- school students
- executives
- technical audience

adapt the language and complexity accordingly.

Never invent information.
"""


# ============================================================
# GENERAL CONTENT GENERATION
# ============================================================

def generate_content(
    document_text,
    user_requirement=""
):

    requirement_lower = user_requirement.lower()

    presentation_keywords = [
        "presentation",
        "powerpoint",
        "power point",
        "ppt",
        "slides",
        "slide deck"
    ]

    is_presentation = any(
        keyword in requirement_lower
        for keyword in presentation_keywords
    )

    if is_presentation:

        task = PRESENTATION_TASK

    else:

        task = """
Generate the requested content from the document.

The user's requirement is the main instruction.

If the requirement asks for:
- a report → create the report
- notes → create the notes
- questions → create the questions
- an executive summary → create the executive summary
- an explanation → create the explanation
- an article → create the article
- a study guide → create the study guide
- another specific format → actually create that format

Do not simply recommend or describe the requested output.

Return the completed content.
"""

    prompt = build_document_prompt(
        task,
        document_text,
        user_requirement
    )

    return generate_ai_response(prompt)


# ============================================================
# CONTEXT-AWARE ANALYSIS
# ============================================================

def analyze_document_context(
    document_text,
    user_requirement=""
):

    task = """
Perform context-aware analysis of the document.

Provide:

1. Summary
2. Document Type
3. Key Entities
4. Key Facts
5. Important Context
6. Recommended Next Steps

The recommended next steps must be based on the document
and the user's requirement.

Do not invent facts.
"""

    prompt = build_document_prompt(
        task,
        document_text,
        user_requirement
    )

    return generate_ai_response(prompt)


# ============================================================
# REQUIREMENT ANALYSIS
# ============================================================

def analyze_user_requirement(user_requirement):

    """
    Provides a simple classification of the user's requested
    output format.

    This is intentionally rule-based so that obvious requests
    such as presentation/PPT requests are handled consistently.
    """

    requirement = user_requirement.lower().strip()

    if any(
        word in requirement
        for word in [
            "presentation",
            "powerpoint",
            "power point",
            "ppt",
            "slides",
            "slide deck"
        ]
    ):

        return "presentation"

    if any(
        word in requirement
        for word in [
            "summary",
            "summarize",
            "summarise"
        ]
    ):

        return "summary"

    if any(
        word in requirement
        for word in [
            "question",
            "questions",
            "quiz"
        ]
    ):

        return "questions"

    if any(
        word in requirement
        for word in [
            "notes",
            "study notes",
            "study guide"
        ]
    ):

        return "notes"

    if any(
        word in requirement
        for word in [
            "report"
        ]
    ):

        return "report"

    return "general"


# ============================================================
# PRESENTATION SLIDE PARSER
# ============================================================

def parse_presentation(output):

    """
    Converts the AI presentation response into a list of:

    {
        "title": "...",
        "content": [...]
    }

    This allows the Streamlit application to generate
    an actual PowerPoint file.
    """

    slides = []

    lines = output.splitlines()

    current_slide = None
    current_content = []

    for raw_line in lines:

        line = raw_line.strip()

        if not line:
            continue

        upper_line = line.upper()

        # Detect:
        # SLIDE 1:
        # SLIDE 2:
        # SLIDE 10:
        if upper_line.startswith("SLIDE"):

            if current_slide is not None:

                current_slide["content"] = current_content

                slides.append(
                    current_slide
                )

            title = line

            title = re.sub(
                r"^SLIDE\s*\d+\s*[:\-]\s*",
                "",
                title,
                flags=re.IGNORECASE
            )

            current_slide = {
                "title": title.strip(),
                "content": []
            }

            current_content = []

            continue

        if upper_line.startswith("CONTENT:"):

            continue

        if current_slide is not None:

            if line.startswith("-"):

                content = line[1:].strip()

            elif line.startswith("•"):

                content = line[1:].strip()

            elif line.startswith("*"):

                content = line[1:].strip()

            else:

                content = line

            if content:

                current_content.append(
                    content
                )

    if current_slide is not None:

        current_slide["content"] = current_content

        slides.append(
            current_slide
        )

    return slides


# ============================================================
# IMPORT FOR PARSER
# ============================================================

import re