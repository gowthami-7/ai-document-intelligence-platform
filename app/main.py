import streamlit as st

from pypdf import PdfReader
from docx import Document

from io import BytesIO
import re
import html

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor

from services.ai_service import (
    summarize_document,
    extract_information,
    classify_document,
    generate_content,
    analyze_document_context,
    analyze_user_requirement,
    parse_presentation
)

from services.quality_service import (
    validate_output,
    evaluate_output
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Document Intelligence",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE
# ============================================================

if "document_processed" not in st.session_state:
    st.session_state.document_processed = False

if "document_text" not in st.session_state:
    st.session_state.document_text = ""

if "processed_file_signature" not in st.session_state:
    st.session_state.processed_file_signature = ""

if "user_requirement" not in st.session_state:
    st.session_state.user_requirement = ""

if "last_result" not in st.session_state:
    st.session_state.last_result = ""

if "last_result_title" not in st.session_state:
    st.session_state.last_result_title = ""


# ============================================================
# PREMIUM UI
# ============================================================

st.markdown(
    """
    <style>

    .stApp {

        background:
            radial-gradient(
                circle at 8% 5%,
                rgba(91, 76, 220, 0.24),
                transparent 28%
            ),
            radial-gradient(
                circle at 92% 8%,
                rgba(24, 150, 255, 0.18),
                transparent 30%
            ),
            radial-gradient(
                circle at 50% 100%,
                rgba(92, 58, 210, 0.10),
                transparent 35%
            ),
            linear-gradient(
                135deg,
                #070b18 0%,
                #0b1124 45%,
                #080d1c 100%
            );

        color: #f7f9ff;
    }

    .block-container {

        max-width: 1220px;

        padding-top: 2.5rem;

        padding-bottom: 4rem;
    }

    p,
    li,
    label {

        color: #dce5f7;
    }

    h1 {

        color: #ffffff !important;

        font-size: 3.15rem !important;

        font-weight: 800 !important;

        letter-spacing: -1.5px;

        line-height: 1.1;
    }

    h2 {

        color: #ffffff !important;

        font-size: 2rem !important;

        font-weight: 750 !important;
    }

    h3 {

        color: #f8faff !important;

        font-weight: 700 !important;
    }

    .stCaption {

        color: #9fb1d2 !important;
    }

    .hero-badge {

        display: inline-block;

        padding: 7px 14px;

        margin-bottom: 14px;

        border-radius: 999px;

        background:
            rgba(67, 105, 220, 0.15);

        border:
            1px solid rgba(92, 145, 255, 0.35);

        color:
            #9ec7ff;

        font-size:
            0.85rem;

        font-weight:
            700;
    }

    .hero-subtitle {

        color: #c0cee7;

        font-size: 1.08rem;

        line-height: 1.75;

        max-width: 880px;
    }

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                #11182f 0%,
                #090f20 100%
            );

        border-right:
            1px solid rgba(89, 133, 235, 0.20);
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {

        color:
            #ffffff !important;
    }

    hr {

        border-color:
            rgba(105, 135, 210, 0.18) !important;
    }

    .stButton > button {

        min-height:
            46px;

        border-radius:
            12px;

        border:
            1px solid rgba(91, 151, 255, 0.45);

        background:
            linear-gradient(
                135deg,
                #315cf6,
                #7048e8
            );

        color:
            #ffffff;

        font-weight:
            700;

        box-shadow:
            0 9px 28px rgba(52, 91, 230, 0.22);

        transition:
            all 0.2s ease;
    }

    .stButton > button:hover {

        border-color:
            #74b0ff;

        box-shadow:
            0 12px 34px rgba(75, 119, 255, 0.38);

        transform:
            translateY(-1px);
    }

    [data-testid="stFileUploader"] {

        background:
            linear-gradient(
                135deg,
                rgba(28, 48, 91, 0.90),
                rgba(15, 27, 57, 0.92)
            );

        border:
            1px solid rgba(73, 137, 255, 0.45);

        border-radius:
            19px;

        padding:
            14px;

        box-shadow:
            0 15px 40px rgba(0, 0, 0, 0.25);
    }

    [data-testid="stFileUploader"] section {

        background:
            transparent !important;
    }

    [data-testid="stFileUploaderDropzone"] {

        background:
            rgba(15, 28, 59, 0.80) !important;

        border:
            1px dashed rgba(83, 155, 255, 0.70) !important;

        border-radius:
            14px !important;
    }

    textarea {

        background:
            #111a31 !important;

        color:
            #f6f8ff !important;

        border:
            1px solid rgba(95, 137, 232, 0.38) !important;

        border-radius:
            13px !important;
    }

    textarea::placeholder {

        color:
            #7183a7 !important;
    }

    textarea:focus {

        border:
            1px solid #5b9cff !important;

        box-shadow:
            0 0 0 1px #5b9cff !important;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {

        background:
            linear-gradient(
                145deg,
                rgba(23, 38, 76, 0.91),
                rgba(12, 22, 48, 0.94)
            );

        border:
            1px solid rgba(89, 130, 230, 0.30);

        border-radius:
            18px;

        box-shadow:
            0 12px 35px rgba(0, 0, 0, 0.20);
    }

    [data-testid="stMetric"] {

        background:
            linear-gradient(
                145deg,
                rgba(28, 47, 91, 0.95),
                rgba(14, 25, 53, 0.95)
            );

        border:
            1px solid rgba(82, 133, 238, 0.34);

        border-radius:
            16px;

        padding:
            18px;
    }

    [data-testid="stMetricLabel"] {

        color:
            #9eb1d5 !important;
    }

    [data-testid="stMetricValue"] {

        color:
            #ffffff !important;

        font-weight:
            800 !important;
    }

    [data-testid="stAlert"] {

        border-radius:
            14px;

        border:
            1px solid rgba(88, 143, 245, 0.32);
    }

    [data-testid="stExpander"] {

        background:
            rgba(17, 29, 58, 0.86);

        border:
            1px solid rgba(88, 130, 220, 0.30);

        border-radius:
            15px;
    }

    .stDownloadButton > button {

        background:
            linear-gradient(
                135deg,
                #1e3e82,
                #3431a7
            );

        color:
            #ffffff;

        border:
            1px solid rgba(96, 159, 255, 0.45);

        border-radius:
            11px;

        font-weight:
            700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DOCUMENT EXTRACTION
# ============================================================

def extract_pdf_text(uploaded_file):

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:

            text += page_text + "\n"

    return text


def extract_docx_text(uploaded_file):

    document = Document(uploaded_file)

    text = ""

    for paragraph in document.paragraphs:

        if paragraph.text.strip():

            text += paragraph.text + "\n"

    return text


def extract_txt_text(uploaded_file):

    return uploaded_file.read().decode(
        "utf-8",
        errors="replace"
    )


def extract_text(uploaded_file):

    file_name = uploaded_file.name.lower()

    if file_name.endswith(".pdf"):

        return extract_pdf_text(uploaded_file)

    elif file_name.endswith(".docx"):

        return extract_docx_text(uploaded_file)

    elif file_name.endswith(".txt"):

        return extract_txt_text(uploaded_file)

    return None


# ============================================================
# PDF TEXT CLEANING
# ============================================================

def clean_pdf_text(text):

    if not text:

        return ""

    replacements = {

        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2212": "-",
        "\u2022": "-",
        "\u00a0": " ",
        "\u2026": "...",
        "\u2192": "->",
        "\u2190": "<-",
        "\u00b7": "-",
        "\u2011": "-",
    }

    for old, new in replacements.items():

        text = text.replace(
            old,
            new
        )

    # Remove characters that Helvetica cannot safely encode
    text = text.encode(
        "latin-1",
        errors="replace"
    ).decode(
        "latin-1"
    )

    text = html.escape(text)

    text = re.sub(
        r"\*\*(.*?)\*\*",
        r"<b>\1</b>",
        text
    )

    text = re.sub(
        r"\*(.*?)\*",
        r"<i>\1</i>",
        text
    )

    return text


# ============================================================
# CREATE PDF
# ============================================================

def create_pdf(
    title,
    output,
    requirement=""
):

    buffer = BytesIO()

    pdf = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=22,
        leading=27,
        textColor=colors.HexColor("#2457D6"),
        alignment=TA_LEFT,
        spaceAfter=8
    )

    subtitle_style = ParagraphStyle(
        "CustomSubtitle",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=19,
        textColor=colors.HexColor("#222222"),
        spaceAfter=12
    )

    section_style = ParagraphStyle(
        "CustomSection",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2457D6"),
        spaceBefore=8,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=16,
        textColor=colors.HexColor("#222222"),
        spaceAfter=5
    )

    requirement_style = ParagraphStyle(
        "RequirementStyle",
        parent=body_style,
        fontName="Helvetica-Oblique",
        fontSize=10,
        leading=15,
        textColor=colors.HexColor("#444444")
    )

    footer_style = ParagraphStyle(
        "FooterStyle",
        parent=body_style,
        fontSize=8.5,
        textColor=colors.HexColor("#777777")
    )

    story = []

    # TITLE

    story.append(
        Paragraph(
            "AI Document Intelligence",
            title_style
        )
    )

    story.append(
        Paragraph(
            clean_pdf_text(title),
            subtitle_style
        )
    )

    story.append(
        Spacer(1, 4)
    )

    # USER REQUIREMENT

    if requirement:

        story.append(
            Paragraph(
                "User Requirement",
                section_style
            )
        )

        story.append(
            Paragraph(
                clean_pdf_text(requirement),
                requirement_style
            )
        )

        story.append(
            Spacer(1, 8)
        )

    # AI RESULT

    story.append(
        Paragraph(
            "AI Analysis Result",
            section_style
        )
    )

    for raw_line in output.splitlines():

        line = raw_line.strip()

        if not line:

            story.append(
                Spacer(1, 6)
            )

            continue

        if line.upper().startswith("SLIDE "):

            story.append(
                Paragraph(
                    clean_pdf_text(line),
                    section_style
                )
            )

            continue

        if line.upper() == "CONTENT:":

            continue

        if line.startswith("###"):

            heading = line.lstrip("#").strip()

            story.append(
                Paragraph(
                    clean_pdf_text(heading),
                    section_style
                )
            )

            continue

        if line.startswith("##"):

            heading = line.lstrip("#").strip()

            story.append(
                Paragraph(
                    clean_pdf_text(heading),
                    section_style
                )
            )

            continue

        if line.startswith("#"):

            heading = line.lstrip("#").strip()

            story.append(
                Paragraph(
                    clean_pdf_text(heading),
                    section_style
                )
            )

            continue

        if line.startswith("- "):

            line = "- " + line[2:]

        elif line.startswith("* "):

            line = "- " + line[2:]

        story.append(
            Paragraph(
                clean_pdf_text(line),
                body_style
            )
        )

    story.append(
        Spacer(1, 18)
    )

    story.append(
        Paragraph(
            "Generated by AI Document Intelligence Platform",
            footer_style
        )
    )

    pdf.build(story)

    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# CREATE POWERPOINT
# ============================================================

def create_presentation(
    slides,
    presentation_title="AI Generated Presentation"
):

    prs = Presentation()

    prs.slide_width = Inches(13.333)

    prs.slide_height = Inches(7.5)

    # --------------------------------------------------------
    # COLORS
    # --------------------------------------------------------

    background_color = RGBColor(
        8,
        13,
        31
    )

    title_color = RGBColor(
        255,
        255,
        255
    )

    body_color = RGBColor(
        218,
        228,
        247
    )

    accent_color = RGBColor(
        91,
        116,
        255
    )

    # --------------------------------------------------------
    # TITLE SLIDE
    # --------------------------------------------------------

    title_slide = prs.slides.add_slide(
        prs.slide_layouts[6]
    )

    background = title_slide.background

    background.fill.solid()

    background.fill.fore_color.rgb = background_color

    title_box = title_slide.shapes.add_textbox(
        Inches(1),
        Inches(2.0),
        Inches(11.3),
        Inches(1.5)
    )

    title_frame = title_box.text_frame

    title_frame.clear()

    paragraph = title_frame.paragraphs[0]

    paragraph.text = presentation_title

    paragraph.font.size = Pt(32)

    paragraph.font.bold = True

    paragraph.font.color.rgb = title_color

    paragraph.alignment = 1

    subtitle_box = title_slide.shapes.add_textbox(
        Inches(1.5),
        Inches(3.7),
        Inches(10.3),
        Inches(1.2)
    )

    subtitle_frame = subtitle_box.text_frame

    subtitle_frame.clear()

    subtitle = subtitle_frame.paragraphs[0]

    subtitle.text = (
        "Generated by AI Document Intelligence"
    )

    subtitle.font.size = Pt(18)

    subtitle.font.color.rgb = body_color

    subtitle.alignment = 1

    # --------------------------------------------------------
    # CONTENT SLIDES
    # --------------------------------------------------------

    for slide_data in slides:

        slide = prs.slides.add_slide(
            prs.slide_layouts[6]
        )

        slide.background.fill.solid()

        slide.background.fill.fore_color.rgb = (
            background_color
        )

        # Accent bar

        bar = slide.shapes.add_shape(
            1,
            Inches(0),
            Inches(0),
            Inches(0.18),
            Inches(7.5)
        )

        bar.fill.solid()

        bar.fill.fore_color.rgb = accent_color

        bar.line.fill.background()

        # Title

        title_box = slide.shapes.add_textbox(
            Inches(0.75),
            Inches(0.55),
            Inches(11.7),
            Inches(0.9)
        )

        title_frame = title_box.text_frame

        title_frame.clear()

        title = title_frame.paragraphs[0]

        title.text = slide_data.get(
            "title",
            "Untitled Slide"
        )

        title.font.size = Pt(27)

        title.font.bold = True

        title.font.color.rgb = title_color

        # Content

        content_box = slide.shapes.add_textbox(
            Inches(0.95),
            Inches(1.65),
            Inches(11.2),
            Inches(5.1)
        )

        text_frame = content_box.text_frame

        text_frame.clear()

        text_frame.word_wrap = True

        content_items = slide_data.get(
            "content",
            []
        )

        if not content_items:

            paragraph = text_frame.paragraphs[0]

            paragraph.text = (
                "No detailed content was generated."
            )

            paragraph.font.size = Pt(18)

            paragraph.font.color.rgb = body_color

        else:

            for index, item in enumerate(
                content_items
            ):

                if index == 0:

                    paragraph = text_frame.paragraphs[0]

                else:

                    paragraph = text_frame.add_paragraph()

                paragraph.text = item

                paragraph.font.size = Pt(19)

                paragraph.font.color.rgb = body_color

                paragraph.space_after = Pt(12)

                paragraph.level = 0

                paragraph.text = "• " + paragraph.text

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    buffer = BytesIO()

    prs.save(buffer)

    buffer.seek(0)

    return buffer.getvalue()


# ============================================================
# DISPLAY AI RESULT
# ============================================================

def display_ai_result(
    title,
    output,
    source_text,
    requirement="",
    presentation=False
):

    st.session_state.last_result = output

    st.session_state.last_result_title = title

    st.divider()

    st.subheader(title)

    st.success(
        "AI processing completed successfully."
    )

    # --------------------------------------------------------
    # RESULT
    # --------------------------------------------------------

    with st.container(border=True):

        st.markdown(
            "### 📄 AI Analysis Result"
        )

        st.markdown(output)

    # --------------------------------------------------------
    # PRESENTATION DOWNLOAD
    # --------------------------------------------------------

    if presentation:

        slides = parse_presentation(
            output
        )

        if slides:

            st.divider()

            st.subheader(
                "🎞️ Presentation Generated"
            )

            st.success(
                f"Successfully created {len(slides)} presentation slides."
            )

            ppt_title = "AI Generated Presentation"

            if slides[0].get("title"):

                ppt_title = slides[0]["title"]

            ppt_data = create_presentation(
                slides,
                ppt_title
            )

            st.download_button(
                label="📥 Download PowerPoint Presentation",
                data=ppt_data,
                file_name="ai_generated_presentation.pptx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "presentationml.presentation"
                ),
                use_container_width=True
            )

            # Slide preview

            with st.expander(
                "👁️ Preview Generated Slides"
            ):

                for index, slide in enumerate(
                    slides,
                    start=1
                ):

                    st.markdown(
                        f"### Slide {index} — {slide['title']}"
                    )

                    for item in slide["content"]:

                        st.write(
                            f"• {item}"
                        )

                    if index < len(slides):

                        st.divider()

        else:

            st.warning(
                "The AI generated content, but the presentation "
                "structure could not be detected. Please try again."
            )

    # --------------------------------------------------------
    # PDF DOWNLOAD
    # --------------------------------------------------------

    st.write("")

    try:

        pdf_data = create_pdf(
            title,
            output,
            requirement
        )

        st.download_button(
            label="📥 Download AI Result as PDF",
            data=pdf_data,
            file_name="ai_document_result.pdf",
            mime="application/pdf",
            use_container_width=True
        )

    except Exception as error:

        st.error(
            "PDF generation failed."
        )

        st.code(
            str(error)
        )

    # --------------------------------------------------------
    # VALIDATION
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🛡️ Output Validation"
    )

    try:

        validation = validate_output(
            output,
            source_text
        )

        if validation["status"] == "PASS":

            st.success(
                validation["message"]
            )

        elif validation["status"] == "WARNING":

            st.warning(
                validation["message"]
            )

        else:

            st.error(
                validation["message"]
            )

        with st.container(border=True):

            for check in validation["checks"]:

                st.write(check)

    except Exception as error:

        st.warning(
            "Output validation could not be completed."
        )

        st.caption(
            str(error)
        )

    # --------------------------------------------------------
    # QUALITY EVALUATION
    # --------------------------------------------------------

    st.subheader(
        "📊 Quality Evaluation"
    )

    try:

        evaluation = evaluate_output(
            output,
            source_text
        )

        q1, q2, q3, q4 = st.columns(4)

        with q1:

            st.metric(
                "Overall",
                f"{evaluation['overall']}%"
            )

        with q2:

            st.metric(
                "Relevance",
                f"{evaluation['relevance']}%"
            )

        with q3:

            st.metric(
                "Consistency",
                f"{evaluation['consistency']}%"
            )

        with q4:

            st.metric(
                "Factuality",
                f"{evaluation['factuality']}%"
            )

    except Exception as error:

        st.warning(
            "Quality evaluation could not be completed."
        )

        st.caption(
            str(error)
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title(
        "🤖 AI Platform"
    )

    st.caption(
        "Intelligent document analysis"
    )

    st.divider()

    st.subheader(
        "📂 Supported Files"
    )

    st.write("📄 PDF")
    st.write("📝 DOCX")
    st.write("📃 TXT")

    st.divider()

    st.subheader(
        "🧠 AI Capabilities"
    )

    st.write("✨ Summarization")
    st.write("🔍 Information Extraction")
    st.write("🏷️ Classification")
    st.write("✍️ Content Generation")
    st.write("🔗 Context Analysis")

    st.divider()

    st.subheader(
        "📦 Output Formats"
    )

    st.write("📄 PDF")
    st.write("📊 PowerPoint")

    st.divider()

    st.subheader(
        "🛡️ Quality Layer"
    )

    st.write("✓ Output Validation")
    st.write("✓ Quality Evaluation")
    st.write("✓ Source-aware Analysis")

    st.divider()

    st.caption(
        "AI Document Intelligence Platform"
    )


# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="hero-badge">✦ INTELLIGENT DOCUMENT ANALYSIS</div>',
    unsafe_allow_html=True
)

st.markdown(
    "# 🤖 AI Document Intelligence"
)

st.markdown(
    """
    <div class="hero-subtitle">
        Transform documents into actionable intelligence.
        Upload a document, define your requirement, and use
        AI-powered analysis to understand, classify and
        generate useful information from your document.
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")


# ============================================================
# WORKFLOW
# ============================================================

st.subheader(
    "⚡ Intelligent Workflow"
)

w1, w2, w3, w4 = st.columns(4)

with w1:

    with st.container(border=True):

        st.markdown("### 01")

        st.markdown(
            "**📤 Upload**"
        )

        st.caption(
            "Add your document"
        )


with w2:

    with st.container(border=True):

        st.markdown("### 02")

        st.markdown(
            "**🎯 Understand**"
        )

        st.caption(
            "Define your requirement"
        )


with w3:

    with st.container(border=True):

        st.markdown("### 03")

        st.markdown(
            "**🧠 Generate**"
        )

        st.caption(
            "AI executes the task"
        )


with w4:

    with st.container(border=True):

        st.markdown("### 04")

        st.markdown(
            "**🛡️ Validate**"
        )

        st.caption(
            "Check output quality"
        )


# ============================================================
# UPLOAD
# ============================================================

st.divider()

st.subheader(
    "📄 Upload Your Document"
)

st.caption(
    "Supported formats: PDF, DOCX and TXT"
)

uploaded_file = st.file_uploader(
    "Choose your document",
    type=[
        "pdf",
        "docx",
        "txt"
    ],
    label_visibility="collapsed"
)


# ============================================================
# FILE SIGNATURE
# ============================================================

current_signature = ""

if uploaded_file is not None:

    current_signature = (
        f"{uploaded_file.name}_{uploaded_file.size}"
    )

    if (
        current_signature
        != st.session_state.processed_file_signature
    ):

        st.session_state.document_processed = False

        st.session_state.document_text = ""

        st.session_state.processed_file_signature = ""

        st.session_state.last_result = ""

        st.session_state.last_result_title = ""

        st.session_state.user_requirement = ""


# ============================================================
# USER REQUIREMENT
# ============================================================

if uploaded_file is not None:

    st.divider()

    st.subheader(
        "🎯 What do you want from this document?"
    )

    st.caption(
        "Your requirement controls what the AI actually produces."
    )

    requirement = st.text_area(
        "User Requirement",
        value=st.session_state.user_requirement,
        placeholder=(
            "Example: Create a 10-slide presentation "
            "for college students. Keep the language "
            "simple and highlight the most important findings."
        ),
        height=140,
        label_visibility="collapsed"
    )

    st.session_state.user_requirement = requirement

    st.write("")

    proceed_clicked = st.button(
        "🚀 Proceed & Analyze Document",
        type="primary",
        use_container_width=True
    )

    if proceed_clicked:

        if not requirement.strip():

            st.warning(
                "Please enter your user requirement before proceeding."
            )

            st.session_state.document_processed = False

        else:

            with st.spinner(
                "Processing your document..."
            ):

                try:

                    document_text = extract_text(
                        uploaded_file
                    )

                    if (
                        document_text
                        and document_text.strip()
                    ):

                        st.session_state.document_text = (
                            document_text
                        )

                        st.session_state.document_processed = True

                        st.session_state.processed_file_signature = (
                            current_signature
                        )

                        st.session_state.user_requirement = (
                            requirement
                        )

                        st.session_state.last_result = ""

                        st.session_state.last_result_title = ""

                        st.success(
                            f"✓ Document uploaded successfully: "
                            f"{uploaded_file.name}"
                        )

                    else:

                        st.session_state.document_processed = False

                        st.error(
                            "The document appears to be empty "
                            "or no readable text could be extracted."
                        )

                except Exception as error:

                    st.session_state.document_processed = False

                    st.error(
                        "The document could not be processed."
                    )

                    st.code(
                        str(error)
                    )


# ============================================================
# DOCUMENT WORKSPACE
# ============================================================

if (
    uploaded_file is not None
    and st.session_state.document_processed
):

    document_text = (
        st.session_state.document_text
    )

    requirement = (
        st.session_state.user_requirement
    )

    # --------------------------------------------------------
    # DOCUMENT READY
    # --------------------------------------------------------

    st.divider()

    st.success(
        f"✓ Document ready for AI analysis — "
        f"{uploaded_file.name}"
    )

    # --------------------------------------------------------
    # DOCUMENT OVERVIEW
    # --------------------------------------------------------

    st.subheader(
        "📊 Document Overview"
    )

    word_count = len(
        document_text.split()
    )

    character_count = len(
        document_text
    )

    file_extension = (
        uploaded_file.name
        .split(".")[-1]
        .upper()
    )

    m1, m2, m3 = st.columns(3)

    with m1:

        st.metric(
            "Words",
            f"{word_count:,}"
        )

    with m2:

        st.metric(
            "Characters",
            f"{character_count:,}"
        )

    with m3:

        st.metric(
            "File Type",
            file_extension
        )

    # --------------------------------------------------------
    # ACTIVE REQUIREMENT
    # --------------------------------------------------------

    st.subheader(
        "🎯 Active User Requirement"
    )

    with st.container(border=True):

        st.info(
            requirement
        )

    # --------------------------------------------------------
    # REQUIREMENT DETECTION
    # --------------------------------------------------------

    requirement_type = analyze_user_requirement(
        requirement
    )

    if requirement_type == "presentation":

        st.success(
            "🎞️ Presentation request detected — "
            "the Content Generation tool will create "
            "actual slide content and a downloadable PowerPoint."
        )

    # --------------------------------------------------------
    # EXTRACTED TEXT
    # --------------------------------------------------------

    with st.expander(
        "📖 View Extracted Document Text"
    ):

        st.text_area(
            "Extracted Content",
            document_text,
            height=350,
            label_visibility="collapsed"
        )

    # --------------------------------------------------------
    # AI TOOLS
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "🧠 AI Document Intelligence"
    )

    st.caption(
        "Every operation uses your document and active user requirement."
    )

    # --------------------------------------------------------
    # SUMMARIZATION
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.markdown(
                "### ✨ Summarization"
            )

            st.write(
                "Generate a structured and concise "
                "summary from the document."
            )

            summarize_clicked = st.button(
                "✨ Generate Summary",
                use_container_width=True,
                key="summarize_button"
            )

    # --------------------------------------------------------
    # INFORMATION EXTRACTION
    # --------------------------------------------------------

    with col2:

        with st.container(border=True):

            st.markdown(
                "### 🔍 Information Extraction"
            )

            st.write(
                "Extract people, organizations, dates, "
                "locations and important facts."
            )

            extraction_clicked = st.button(
                "🔍 Extract Information",
                use_container_width=True,
                key="extraction_button"
            )

    # --------------------------------------------------------
    # CLASSIFICATION
    # --------------------------------------------------------

    col3, col4 = st.columns(2)

    with col3:

        with st.container(border=True):

            st.markdown(
                "### 🏷️ Classification"
            )

            st.write(
                "Identify the most appropriate "
                "document category."
            )

            classification_clicked = st.button(
                "🏷️ Classify Document",
                use_container_width=True,
                key="classification_button"
            )

    # --------------------------------------------------------
    # CONTENT GENERATION
    # --------------------------------------------------------

    with col4:

        with st.container(border=True):

            st.markdown(
                "### ✍️ Content Generation"
            )

            if requirement_type == "presentation":

                st.write(
                    "Create the requested presentation "
                    "and generate an actual PowerPoint file."
                )

                content_button_text = (
                    "🎞️ Create Presentation"
                )

            else:

                st.write(
                    "Generate the requested content "
                    "according to your requirement."
                )

                content_button_text = (
                    "✍️ Generate Requested Content"
                )

            content_clicked = st.button(
                content_button_text,
                use_container_width=True,
                key="content_button"
            )

    # --------------------------------------------------------
    # CONTEXT ANALYSIS
    # --------------------------------------------------------

    st.write("")

    with st.container(border=True):

        st.markdown(
            "### 🔗 Context-Aware Document Analysis"
        )

        st.write(
            "Perform a combined analysis while preserving "
            "the document context throughout the process."
        )

        context_clicked = st.button(
            "🔗 Analyze Document Context",
            use_container_width=True,
            key="context_button"
        )

    # --------------------------------------------------------
    # AI EXECUTION
    # --------------------------------------------------------

    if summarize_clicked:

        with st.spinner(
            "Generating summary according to your requirement..."
        ):

            try:

                output = summarize_document(
                    document_text,
                    requirement
                )

                display_ai_result(
                    "✨ AI-Generated Summary",
                    output,
                    document_text,
                    requirement
                )

            except Exception as error:

                st.error(
                    "Summary generation failed."
                )

                st.code(
                    str(error)
                )

    elif extraction_clicked:

        with st.spinner(
            "Extracting information according to your requirement..."
        ):

            try:

                output = extract_information(
                    document_text,
                    requirement
                )

                display_ai_result(
                    "🔍 Extracted Information",
                    output,
                    document_text,
                    requirement
                )

            except Exception as error:

                st.error(
                    "Information extraction failed."
                )

                st.code(
                    str(error)
                )

    elif classification_clicked:

        with st.spinner(
            "Classifying document..."
        ):

            try:

                output = classify_document(
                    document_text,
                    requirement
                )

                display_ai_result(
                    "🏷️ Document Classification",
                    output,
                    document_text,
                    requirement
                )

            except Exception as error:

                st.error(
                    "Classification failed."
                )

                st.code(
                    str(error)
                )

    elif content_clicked:

        if requirement_type == "presentation":

            with st.spinner(
                "Creating your presentation..."
            ):

                try:

                    output = generate_content(
                        document_text,
                        requirement
                    )

                    display_ai_result(
                        "🎞️ AI-Generated Presentation",
                        output,
                        document_text,
                        requirement,
                        presentation=True
                    )

                except Exception as error:

                    st.error(
                        "Presentation generation failed."
                    )

                    st.code(
                        str(error)
                    )

        else:

            with st.spinner(
                "Generating the requested content..."
            ):

                try:

                    output = generate_content(
                        document_text,
                        requirement
                    )

                    display_ai_result(
                        "✍️ AI-Generated Content",
                        output,
                        document_text,
                        requirement
                    )

                except Exception as error:

                    st.error(
                        "Content generation failed."
                    )

                    st.code(
                        str(error)
                    )

    elif context_clicked:

        with st.spinner(
            "Running context-aware analysis..."
        ):

            try:

                output = analyze_document_context(
                    document_text,
                    requirement
                )

                display_ai_result(
                    "🔗 Context-Aware Analysis",
                    output,
                    document_text,
                    requirement
                )

            except Exception as error:

                st.error(
                    "Context-aware analysis failed."
                )

                st.code(
                    str(error)
                )


# ============================================================
# EMPTY STATE
# ============================================================

if uploaded_file is None:

    st.divider()

    with st.container(border=True):

        st.markdown(
            "### 📄 Ready when you are"
        )

        st.write(
            "Upload a PDF, DOCX or TXT document "
            "to begin intelligent document analysis."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🤖 AI Document Intelligence Platform  •  "
    "Document Analysis  •  AI Generation  •  "
    "PowerPoint Generation  •  Quality Validation"
)