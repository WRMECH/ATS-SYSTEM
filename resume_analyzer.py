import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import numpy as np

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

class ResumeAnalyzer:
    def __init__(self):
        self.field_keywords = {
            'Software Engineering': [
                'python', 'java', 'javascript', 'react', 'node.js', 'sql', 'git',
                'docker', 'kubernetes', 'aws', 'api', 'database', 'frontend',
                'backend', 'full-stack', 'agile', 'scrum', 'testing', 'debugging',
                'html', 'css', 'mongodb', 'postgresql', 'redis', 'microservices'
            ],
            'Data Analyst': [
                'python', 'r', 'sql', 'excel', 'tableau', 'power bi', 'pandas',
                'numpy', 'matplotlib', 'seaborn', 'statistics', 'data visualization',
                'machine learning', 'regression', 'classification', 'clustering',
                'etl', 'data mining', 'business intelligence', 'analytics',
                'spss', 'sas', 'hadoop', 'spark', 'data warehouse'
            ],
            'Consultant': [
                'consulting', 'strategy', 'business analysis', 'project management',
                'stakeholder management', 'client relations', 'problem solving',
                'presentation', 'communication', 'leadership', 'change management',
                'process improvement', 'market research', 'financial analysis',
                'risk assessment', 'vendor management', 'negotiation',
                'strategic planning', 'business development'
            ]
        }
        
        self.load_models()
    
    def load_models(self):
        """Load trained models if they exist"""
        try:
            if os.path.exists('models/field_classifier.pkl'):
                with open('models/field_classifier.pkl', 'rb') as f:
                    self.field_classifier = pickle.load(f)
            else:
                self.field_classifier = None
                
            if os.path.exists('models/vectorizer.pkl'):
                with open('models/vectorizer.pkl', 'rb') as f:
                    self.vectorizer = pickle.load(f)
            else:
                self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        except Exception as e:
            print(f"Error loading models: {e}")
            self.field_classifier = None
            self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        if not isinstance(text, str):
            text = str(text)
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and extra whitespace
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def extract_skills(self, text):
        """Extract skills from resume text"""
        text = self.preprocess_text(text)
        skills_found = {}
        
        for field, keywords in self.field_keywords.items():
            field_skills = []
            for keyword in keywords:
                if keyword.lower() in text:
                    field_skills.append(keyword)
            skills_found[field] = field_skills
        
        return skills_found
    
    def get_field_recommendations(self, resume_text):
        """Get field recommendations based on resume content"""
        if self.field_classifier is not None and hasattr(self.vectorizer, 'vocabulary_'):
            try:
                # Use trained model
                text_vector = self.vectorizer.transform([self.preprocess_text(resume_text)])
                probabilities = self.field_classifier.predict_proba(text_vector)[0]
                
                field_names = self.field_classifier.classes_
                recommendations = dict(zip(field_names, probabilities))
            except Exception as e:
                print(f"Error using trained model: {e}")
                recommendations = self._keyword_based_recommendations(resume_text)
        else:
            # Use keyword-based approach
            recommendations = self._keyword_based_recommendations(resume_text)
        
        return recommendations
    
    def _keyword_based_recommendations(self, resume_text):
        """Fallback keyword-based recommendations"""
        skills_found = self.extract_skills(resume_text)
        total_skills = sum(len(skills) for skills in skills_found.values())
        
        if total_skills == 0:
            recommendations = {field: 0.33 for field in self.field_keywords.keys()}
        else:
            recommendations = {
                field: len(skills) / total_skills 
                for field, skills in skills_found.items()
            }
        
        # Normalize to ensure sum equals 1
        total_score = sum(recommendations.values())
        if total_score > 0:
            recommendations = {k: v/total_score for k, v in recommendations.items()}
        
        return recommendations
    
    def analyze_resume(self, resume_text, target_field):
        """Perform comprehensive resume analysis"""
        skills_found = self.extract_skills(resume_text)
        target_skills = skills_found.get(target_field, [])
        required_skills = self.field_keywords.get(target_field, [])
        
        # Calculate match percentage
        match_percentage = (len(target_skills) / len(required_skills)) * 100 if required_skills else 0
        
        # Requirements analysis
        requirements_met = target_skills
        requirements_missing = [skill for skill in required_skills if skill not in target_skills]
        
        # Generate suggestions
        suggestions = self.generate_suggestions(requirements_missing, target_field, resume_text)
        
        # Skills analysis
        skills_analysis = {}
        for skill in required_skills:
            if skill in target_skills:
                skills_analysis[skill] = 1.0
            else:
                # Check for partial matches
                skill_score = self.calculate_skill_score(skill, resume_text)
                skills_analysis[skill] = skill_score
        
        return {
            'match_percentage': match_percentage,
            'requirements_met': requirements_met,
            'requirements_missing': requirements_missing,
            'suggestions': suggestions,
            'skills_analysis': skills_analysis
        }
    
    def calculate_skill_score(self, skill, resume_text):
        """Calculate skill score based on context and related terms"""
        text = self.preprocess_text(resume_text)
        
        # Direct match
        if skill.lower() in text:
            return 1.0
        
        # Related terms scoring
        related_terms = {
            'python': ['programming', 'coding', 'development', 'script', 'django', 'flask'],
            'sql': ['database', 'query', 'data', 'mysql', 'postgresql', 'oracle'],
            'machine learning': ['ml', 'ai', 'artificial intelligence', 'model', 'algorithm'],
            'project management': ['pm', 'agile', 'scrum', 'planning', 'coordination'],
            'javascript': ['js', 'web development', 'frontend', 'react', 'angular', 'vue'],
            'data visualization': ['charts', 'graphs', 'dashboard', 'reporting', 'visual'],
            'consulting': ['advisory', 'strategy', 'client', 'business', 'recommendations']
        }
        
        skill_lower = skill.lower()
        if skill_lower in related_terms:
            score = 0
            for term in related_terms[skill_lower]:
                if term in text:
                    score += 0.2
            return min(score, 0.8)  # Max 0.8 for related terms
        
        return 0.0
    
    def generate_suggestions(self, missing_skills, target_field, resume_text):
        """Generate improvement suggestions"""
        suggestions = []
        
        if not missing_skills:
            suggestions.append(f"Excellent! Your resume covers most required skills for {target_field}")
            return suggestions
        
        # Categorize missing skills
        technical_skills = []
        soft_skills = []
        tools_platforms = []
        
        soft_skill_keywords = ['communication', 'leadership', 'problem solving', 'teamwork', 'presentation']
        tool_keywords = ['aws', 'docker', 'kubernetes', 'tableau', 'power bi', 'git', 'jira']
        
        for skill in missing_skills[:10]:  # Limit to top 10 missing skills
            if skill.lower() in soft_skill_keywords:
                soft_skills.append(skill)
            elif skill.lower() in tool_keywords:
                tools_platforms.append(skill)
            else:
                technical_skills.append(skill)
        
        if technical_skills:
            suggestions.append(f"Consider adding technical skills: {', '.join(technical_skills[:5])}")
        
        if tools_platforms:
            suggestions.append(f"Include experience with tools/platforms: {', '.join(tools_platforms[:3])}")
        
        if soft_skills:
            suggestions.append(f"Highlight soft skills: {', '.join(soft_skills[:3])}")
        
        # Field-specific suggestions
        if target_field == 'Software Engineering':
            suggestions.extend([
                "Include specific programming projects with GitHub links",
                "Mention software development methodologies (Agile, Scrum)",
                "Add details about system architecture and scalability",
                "Include code quality practices (testing, code reviews)"
            ])
        elif target_field == 'Data Analyst':
            suggestions.extend([
                "Include data analysis projects with quantifiable results",
                "Mention specific datasets or business problems you've solved",
                "Add experience with statistical analysis and A/B testing",
                "Include data visualization examples and dashboards"
            ])
        elif target_field == 'Consultant':
            suggestions.extend([
                "Highlight client-facing experience and business impact",
                "Include examples of process improvements or cost savings",
                "Add details about stakeholder management and communication",
                "Mention industry expertise and domain knowledge"
            ])
        
        # General suggestions based on resume content
        text_lower = resume_text.lower()
        if 'project' not in text_lower:
            suggestions.append("Add a projects section to showcase practical experience")
        
        if len(resume_text.split()) < 300:
            suggestions.append("Expand your resume with more detailed descriptions")
        
        if not re.search(r'\d+%|\d+\+|increased|improved|reduced', text_lower):
            suggestions.append("Include quantifiable achievements and metrics")
        
        return suggestions[:8]  # Limit to 8 suggestions

    def load_training_data_for_analysis(self):
        """Load training data for better field recommendations"""
        try:
            from dataset_loader import load_dataset
            df = load_dataset()
            
            if df is not None and len(df) > 0:
                # Update field keywords based on actual dataset
                for field in df['job_field'].unique():
                    field_samples = df[df['job_field'] == field]['resume_text'].tolist()
                    # Extract common keywords from field samples
                    field_text = ' '.join(field_samples).lower()
                    # This could be enhanced with more sophisticated keyword extraction
                    
                return df
            else:
                return None
                
        except Exception as e:
            print(f"Warning: Could not load training data for analysis: {e}")
            return None
