from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from textwrap import wrap
from reportlab.lib import colors

BIG_FONT_SIZE = 13
SMALL_FONT_SIZE = 11
MARGIN = 40

def save_as_pdf(data, pdf_file="resume.pdf"):
    """
    Generate a PDF directly using ReportLab with proper text wrapping, pagination, and empty headers for subsequent pages.
    """
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter
    margin = MARGIN
    y = height - margin
    first_page = True

    def draw_line():
        """Draw a horizontal line."""
        nonlocal y
        c.line(margin, y, width - margin, y)
        y -= 20

    def add_wrapped_text_with_styles(prefix=None, text="", font="Helvetica", size=SMALL_FONT_SIZE, bold_prefix=False, wrap_width=90, indent=0):
        """
        Add wrapped text with optional bold prefixes and accurate wrapping logic.
        """
        nonlocal y, first_page

        # Ensure enough space for a new page
        if y < margin + size + 10:
            c.showPage()
            y = height - margin
            first_page = False
            draw_empty_header()

        c.setFont(font, size)

        # Combine prefix and text, if applicable
        full_text = f"{prefix}: {text}" if prefix else text

        # Accurate wrapping
        words = full_text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if c.stringWidth(test_line, font, size) <= (width - 2 * margin - indent):
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        # Draw each line
        for line in lines:
            x = margin + indent
            if prefix and bold_prefix and line.startswith(f"{prefix}:"):
                # Draw prefix in bold
                c.setFont("Helvetica-Bold", size)
                prefix_width = c.stringWidth(f"{prefix}: ", "Helvetica-Bold", size)
                c.drawString(x, y, f"{prefix}: ")
                c.setFont(font, size)
                c.drawString(x + prefix_width, y, line[len(f"{prefix}: "):])
            else:
                c.drawString(x, y, line)
            y -= size + 2

    def draw_empty_header():
        """Draw an empty header on pages after the first."""
        nonlocal y
        if not first_page:
            y = height - margin

    def add_contact_info():
        """
        Add contact information in one line with clickable hyperlinks.
        """
        nonlocal y
        c.setFont("Helvetica", SMALL_FONT_SIZE)

        # Calculate widths of each component
        phone_text = f"{data['header']['contact']['phone']}"
        linkedin_text = f"LinkedIn"
        email_text = f"{data['header']['contact']['email']}"
        website_text = f"{data['header']['contact']['website']}"
        
        phone_width = c.stringWidth(phone_text, "Helvetica", SMALL_FONT_SIZE)
        linkedin_width = c.stringWidth(linkedin_text, "Helvetica", SMALL_FONT_SIZE)
        email_width = c.stringWidth(email_text, "Helvetica", SMALL_FONT_SIZE)
        website_width = c.stringWidth(website_text, "Helvetica", SMALL_FONT_SIZE)

        # Add spacing between components
        spacing = 10  # pixels between each component
        total_width = phone_width + linkedin_width + email_width + website_width + (3 * spacing)
        
        # Calculate starting x position to center everything
        start_x = (width - total_width) / 2

        # Add Phone
        c.drawString(start_x, y, phone_text)
        
        # Add Email
        email_x = start_x + phone_width + spacing
        c.drawString(email_x, y, email_text)
        c.linkURL(f"mailto:{data['header']['contact']['email']}", 
                 (email_x, y - 2, email_x + email_width, y + 10), 
                 relative=0)

        # Add LinkedIn
        linkedin_x = email_x + email_width + spacing
        c.setFillColor(colors.blue)
        c.drawString(linkedin_x, y, linkedin_text)
        c.linkURL(data['header']['contact']['linkedin'], 
                 (linkedin_x, y - 2, linkedin_x + linkedin_width, y + 10), 
                 relative=0)

        # Add Website
        website_x = linkedin_x + linkedin_width + spacing
        c.drawString(website_x, y, website_text)
        c.linkURL(data['header']['contact']['website'],
                 (website_x, y - 2, website_x + website_width, y + 10),
                 relative=0)
        
        c.setFillColor(colors.black)
        y -= 10

    # First Page Header
    c.setFont("Helvetica-Bold", 16)
    c.drawString((width - c.stringWidth(data["header"]["name"], "Helvetica-Bold", 16)) / 2, y, data["header"]["name"])
    y -= 15

    # Add contact info
    add_contact_info()
    draw_line()

    # Summary Section
    add_wrapped_text_with_styles("Summary", data["summary"].strip(), font="Helvetica", size=BIG_FONT_SIZE, bold_prefix=True)
    draw_line()

    # Education Section
    add_wrapped_text_with_styles("Education", font="Helvetica", size=BIG_FONT_SIZE, bold_prefix=True)
    for edu in data["education"]:
        add_wrapped_text_with_styles(text=f"{edu['date']}", prefix=f"{edu['degree']} - {edu['university']}", bold_prefix=True, indent=10)
    draw_line()

    # Technical Skills Section
    if data["skills"]:
        add_wrapped_text_with_styles("Technical Skills", font="Helvetica", size=BIG_FONT_SIZE, bold_prefix=True)
        skills_data = data["skills"]
        for category, skills in skills_data.items():
            add_wrapped_text_with_styles(category, ", ".join(skills), bold_prefix=True, indent=10)
        draw_line()

    # Work Experience Section
    add_wrapped_text_with_styles("Work Experience", font="Helvetica", size=BIG_FONT_SIZE, bold_prefix=True)
    for exp in data["experience"]:
        add_wrapped_text_with_styles(f"{exp['title']} - {exp['company']} ({exp['duration']})", bold_prefix=True)
        for responsibility in exp.get("responsibilities", []):
            add_wrapped_text_with_styles(text=f"- {responsibility}", indent=10)
    draw_line()

    # Project Experience Section
    add_wrapped_text_with_styles("Projects & More", font="Helvetica", size=BIG_FONT_SIZE, bold_prefix=True)
    for project in data["projects"]:
        add_wrapped_text_with_styles(project["name"], project["description"], bold_prefix=True, indent=10)

    # Save the PDF
    c.save()
    print(f"PDF generated: {pdf_file}")
