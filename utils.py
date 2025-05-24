
from docx import Document
from datetime import datetime
import io

def generate_docx(name, age, gender, symptoms, activity, exposure, smoking, hrv):
    doc=Document()
    doc.add_heading('AMAL Report',0)
    doc.add_paragraph(f'Date: {datetime.today().strftime("%Y-%m-%d")}')
    doc.add_paragraph(f'Patient: {name}, Age: {age}, Gender: {gender}')
    doc.add_heading('Clinical Info',level=1)
    doc.add_paragraph(f'Symptoms: {symptoms or "N/A"}')
    doc.add_paragraph(f'Activity: {activity}')
    doc.add_paragraph(f'Exposure: {exposure or "N/A"}')
    doc.add_paragraph(f'Smoking: {smoking}')
    doc.add_paragraph(f'HRV: {hrv or "N/A"} ms')
    doc.add_heading('Diagnosis',level=1)
    doc.add_paragraph('Pneumonia detected based on simulated heatmap.')
    doc.add_heading('Recommendations',level=1)
    doc.add_paragraph('- Correlate clinically.')
    doc.add_paragraph('- Consider treatment.')
    buf=io.BytesIO(); doc.save(buf)
    return buf.getvalue()
