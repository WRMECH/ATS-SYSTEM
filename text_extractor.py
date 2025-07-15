import PyPDF2
import docx
import io
import streamlit as st

class TextExtractor:
    def __init__(self):
        pass
    
    def extract_text(self, uploaded_file):
        """Extract text from uploaded file based on file type"""
        try:
            file_type = uploaded_file.type
            
            if file_type == "application/pdf":
                return self.extract_from_pdf(uploaded_file)
            elif file_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                return self.extract_from_docx(uploaded_file)
            elif file_type == "text/plain":
                return self.extract_from_txt(uploaded_file)
            else:
                st.error(f"Unsupported file type: {file_type}")
                return ""
        except Exception as e:
            st.error(f"Error extracting text: {str(e)}")
            return ""
    
    def extract_from_pdf(self, uploaded_file):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
            text = ""
            
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            return text.strip()
        except Exception as e:
            st.error(f"Error reading PDF: {str(e)}")
            return ""
    
    def extract_from_docx(self, uploaded_file):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(io.BytesIO(uploaded_file.read()))
            text = ""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            
            return text.strip()
        except Exception as e:
            st.error(f"Error reading DOCX: {str(e)}")
            return ""
    
    def extract_from_txt(self, uploaded_file):
        """Extract text from TXT file"""
        try:
            return uploaded_file.read().decode('utf-8')
        except Exception as e:
            st.error(f"Error reading TXT: {str(e)}")
            return ""
    
    def clean_extracted_text(self, text):
        """Clean and normalize extracted text"""
        # Remove excessive whitespace
        import re
        text = re.sub(r'\n+', '\n', text)
        text = re.sub(r'\s+', ' ', text)
        
        # Remove common PDF artifacts
        text = text.replace('\x0c', '')  # Form feed character
        
        return text.strip()
