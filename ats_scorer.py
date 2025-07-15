import re
from datetime import datetime
import pandas as pd
import os

class ATSScorer:
    def __init__(self):
        self.scoring_criteria = {
            'contact_info': 10,
            'professional_summary': 8,
            'work_experience': 25,
            'education': 10,
            'skills': 20,
            'keywords_match': 15,
            'formatting': 7,
            'length': 5
        }
    
    def calculate_ats_score(self, resume_text, target_field):
        """Calculate comprehensive ATS score"""
        scores = {}
        
        # Contact Information (10 points)
        scores['contact_info'] = self.score_contact_info(resume_text)
        
        # Professional Summary (8 points)
        scores['professional_summary'] = self.score_professional_summary(resume_text)
        
        # Work Experience (25 points)
        scores['work_experience'] = self.score_work_experience(resume_text)
        
        # Education (10 points)
        scores['education'] = self.score_education(resume_text)
        
        # Skills (20 points)
        scores['skills'] = self.score_skills(resume_text, target_field)
        
        # Keywords Match (15 points)
        scores['keywords_match'] = self.score_keywords_match(resume_text, target_field)
        
        # Formatting (7 points)
        scores['formatting'] = self.score_formatting(resume_text)
        
        # Length (5 points)
        scores['length'] = self.score_length(resume_text)
        
        # Calculate total score
        total_score = sum(scores.values())
        
        # Save analysis history
        self.save_analysis_history(resume_text, target_field, total_score, scores)
        
        return min(100, max(0, total_score))
    
    def score_contact_info(self, text):
        """Score contact information completeness"""
        score = 0
        text_lower = text.lower()
        
        # Email - Fixed regex pattern
        if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
            score += 4
        
        # Phone number - Fixed regex pattern
        phone_patterns = [
            r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b',  # 123-456-7890 or 123.456.7890 or 123 456 7890
            r'$$\d{3}$$\s?\d{3}[-.\s]?\d{4}',      # (123) 456-7890
            r'\+\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}',  # +1-123-456-7890
            r'\b\d{10}\b'  # 1234567890
        ]
        
        for pattern in phone_patterns:
            if re.search(pattern, text):
                score += 3
                break
        
        # LinkedIn or professional profile
        if 'linkedin' in text_lower or 'github' in text_lower or 'portfolio' in text_lower:
            score += 3
        
        return score
    
    def score_professional_summary(self, text):
        """Score professional summary/objective"""
        text_lower = text.lower()
        summary_keywords = ['summary', 'objective', 'profile', 'about', 'overview']
        
        for keyword in summary_keywords:
            if keyword in text_lower:
                # Check if it's substantial (more than just the heading)
                lines = text.split('\n')
                for i, line in enumerate(lines):
                    if keyword in line.lower() and i + 1 < len(lines):
                        next_lines = ' '.join(lines[i+1:i+4])
                        if len(next_lines.split()) > 10:
                            return 8
                return 4
        
        return 0
    
    def score_work_experience(self, text):
        """Score work experience section"""
        score = 0
        text_lower = text.lower()
        
        # Check for experience section
        experience_keywords = ['experience', 'employment', 'work history', 'career', 'professional experience']
        has_experience_section = any(keyword in text_lower for keyword in experience_keywords)
        
        if has_experience_section:
            score += 10
        
        # Count job positions (look for date patterns)
        date_patterns = [
            r'\b\d{4}\s*[-–]\s*\d{4}\b',  # 2020-2023
            r'\b\d{4}\s*[-–]\s*present\b',  # 2020-present
            r'\b(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w*\s+\d{4}\b',  # Month Year
            r'\b\d{1,2}/\d{4}\b'  # MM/YYYY
        ]
        
        job_count = 0
        for pattern in date_patterns:
            matches = re.findall(pattern, text_lower)
            job_count += len(matches)
        
        # Score based on number of positions
        if job_count >= 3:
            score += 15
        elif job_count >= 2:
            score += 10
        elif job_count >= 1:
            score += 5
        
        return min(25, score)
    
    def score_education(self, text):
        """Score education section"""
        text_lower = text.lower()
        education_keywords = ['education', 'degree', 'university', 'college', 'bachelor', 'master', 'phd', 'diploma']
        
        score = 0
        for keyword in education_keywords:
            if keyword in text_lower:
                score += 2
                break
        
        # Check for graduation year
        if re.search(r'\b(19|20)\d{2}\b', text):
            score += 3
        
        # Check for GPA (optional but good)
        if re.search(r'gpa|grade point average', text_lower):
            score += 2
        
        # Check for relevant coursework or certifications
        if any(word in text_lower for word in ['coursework', 'certification', 'certified', 'course']):
            score += 3
        
        return min(10, score)
    
    def score_skills(self, text, target_field):
        """Score skills section"""
        text_lower = text.lower()
        
        # Check for skills section
        if 'skill' in text_lower:
            base_score = 5
        else:
            base_score = 0
        
        # Import field keywords from resume_analyzer
        try:
            from resume_analyzer import ResumeAnalyzer
            analyzer = ResumeAnalyzer()
            field_keywords = analyzer.field_keywords.get(target_field, [])
        except ImportError:
            # Fallback keywords if import fails
            field_keywords = {
                'Software Engineering': ['python', 'java', 'javascript', 'react', 'sql'],
                'Data Analyst': ['sql', 'python', 'excel', 'tableau', 'analytics'],
                'Consultant': ['strategy', 'analysis', 'consulting', 'management']
            }.get(target_field, [])
        
        # Count relevant skills
        skills_found = sum(1 for skill in field_keywords if skill.lower() in text_lower)
        skill_score = min(15, skills_found * 1.5)
        
        return base_score + skill_score
    
    def score_keywords_match(self, text, target_field):
        """Score keyword matching for target field"""
        try:
            from resume_analyzer import ResumeAnalyzer
            analyzer = ResumeAnalyzer()
            field_keywords = analyzer.field_keywords.get(target_field, [])
        except ImportError:
            # Fallback keywords if import fails
            field_keywords = {
                'Software Engineering': ['python', 'java', 'javascript', 'react', 'sql', 'git', 'aws'],
                'Data Analyst': ['sql', 'python', 'excel', 'tableau', 'analytics', 'statistics'],
                'Consultant': ['strategy', 'analysis', 'consulting', 'management', 'client']
            }.get(target_field, [])
        
        text_lower = text.lower()
        matches = sum(1 for keyword in field_keywords if keyword.lower() in text_lower)
        
        # Score based on percentage of keywords matched
        match_percentage = matches / len(field_keywords) if field_keywords else 0
        return match_percentage * 15
    
    def score_formatting(self, text):
        """Score formatting and structure"""
        score = 0
        
        # Check for proper sections (headers)
        sections = ['experience', 'education', 'skills', 'summary']
        section_count = sum(1 for section in sections if section in text.lower())
        score += min(4, section_count)
        
        # Check for bullet points or structured lists
        if '•' in text or '·' in text or re.search(r'^\s*[-*]\s', text, re.MULTILINE):
            score += 2
        
        # Check for proper capitalization
        if re.search(r'[A-Z][a-z]', text):
            score += 1
        
        # Penalize excessive formatting issues
        if text.count('\n\n\n') > 5:  # Too many empty lines
            score -= 1
        
        return max(0, min(7, score))
    
    def score_length(self, text):
        """Score resume length appropriateness"""
        word_count = len(text.split())
        
        if 300 <= word_count <= 800:  # Optimal length
            return 5
        elif 200 <= word_count < 300 or 800 < word_count <= 1200:  # Acceptable
            return 3
        elif word_count < 200:  # Too short
            return 1
        else:  # Too long
            return 2
    
    def save_analysis_history(self, resume_text, target_field, total_score, detailed_scores):
        """Save analysis results for analytics"""
        try:
            history_data = {
                'timestamp': datetime.now().isoformat(),
                'target_field': target_field,
                'ats_score': total_score,
                'word_count': len(resume_text.split()),
                'match_percentage': detailed_scores.get('keywords_match', 0) * (100/15),  # Convert to percentage
                **{f'score_{k}': v for k, v in detailed_scores.items()}
            }
            
            # Create data directory if it doesn't exist
            os.makedirs('data', exist_ok=True)
            
            # Append to history file
            history_file = 'data/analysis_history.csv'
            if os.path.exists(history_file):
                df = pd.read_csv(history_file)
                df = pd.concat([df, pd.DataFrame([history_data])], ignore_index=True)
            else:
                df = pd.DataFrame([history_data])
            
            df.to_csv(history_file, index=False)
        except Exception as e:
            print(f"Error saving analysis history: {e}")
    
    def get_detailed_breakdown(self, resume_text, target_field):
        """Get detailed breakdown of ATS scoring"""
        scores = {}
        
        scores['contact_info'] = self.score_contact_info(resume_text)
        scores['professional_summary'] = self.score_professional_summary(resume_text)
        scores['work_experience'] = self.score_work_experience(resume_text)
        scores['education'] = self.score_education(resume_text)
        scores['skills'] = self.score_skills(resume_text, target_field)
        scores['keywords_match'] = self.score_keywords_match(resume_text, target_field)
        scores['formatting'] = self.score_formatting(resume_text)
        scores['length'] = self.score_length(resume_text)
        
        # Calculate percentages
        breakdown = {}
        for category, score in scores.items():
            max_score = self.scoring_criteria[category]
            percentage = (score / max_score) * 100 if max_score > 0 else 0
            breakdown[category] = {
                'score': score,
                'max_score': max_score,
                'percentage': min(100, percentage)
            }
        
        return breakdown
