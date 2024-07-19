import streamlit as st
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

# Load the PDF
pdf_path = 'doc.pdf'

def create_pdf(fields, table_data):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    
    # Fill text fields
    can.drawString(100, 750, f"שם מלא: {fields['full_name']}")
    can.drawString(100, 730, f"תאריך לידה: {fields['dob']}")
    can.drawString(100, 710, f"גובה: {fields['height']} מטר")
    can.drawString(100, 690, f"משקל: {fields['weight']} קג")
    
    # Fill table
    start_y = 640
    for row in table_data:
        can.drawString(100, start_y, row['question'])
        can.drawString(300, start_y, 'כן' if row['answer'] else 'לא')
        if not row['answer']:
            can.drawString(400, start_y, row['details'])
        start_y -= 20
    
    can.save()
    
    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    
    # Read the existing PDF
    existing_pdf = PdfReader(pdf_path)
    output = PdfWriter()
    
    # Add the "watermark" (which is the new pdf) on the existing page
    new_pdf = PdfReader(packet)
    page = existing_pdf.pages[0]
    page.merge_page(new_pdf.pages[0])
    output.add_page(page)
    
    # Finally, write "output" to a real file
    output_stream = BytesIO()
    output.write(output_stream)
    output_stream.seek(0)
    
    return output_stream

st.title("Edit PDF Document")

# Text fields
fields = {
    'full_name': st.text_input("שם מלא:"),
    'dob': st.text_input("תאריך לידה:"),
    'height': st.text_input("גובה (מטר):"),
    'weight': st.text_input("משקל (קג):")
}


# Table data
table_data = [
    {'question': 'קוצב לב', 'answer': st.checkbox('קוצב לב', key='q1'), 'details': st.text_input('פרטים (קוצב לב)', key='d1') if not st.checkbox('קוצב לב', key='a1') else ''},
    {'question': 'מסתם לב מלאכותי', 'answer': st.checkbox('מסתם לב מלאכותי', key='q2'), 'details': st.text_input('פרטים (מסתם לב מלאכותי)', key='d2') if not st.checkbox('מסתם לב מלאכותי', key='a2') else ''}
    # Add other fields similarly with unique keys
]

if st.button("Save as PDF"):
    pdf_stream = create_pdf(fields, table_data)
    st.download_button(label="Download PDF", data=pdf_stream, file_name="edited_document.pdf", mime="application/pdf")
