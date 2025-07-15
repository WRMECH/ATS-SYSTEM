import os
import nltk
import streamlit as st

def setup_environment():
    """Setup the environment for the resume screening system"""
    
    # Create necessary directories
    directories = ['data', 'models', 'uploads']
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"Created directory: {directory}")
    
    # Download NLTK data
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("NLTK data downloaded successfully")
    except Exception as e:
        print(f"Error downloading NLTK data: {e}")
    
    # Create sample training data if it doesn't exist
    sample_data_file = 'data/sample_training_data.csv'
    if not os.path.exists(sample_data_file):
        import pandas as pd
        
        sample_data = {
            'resume_text': [
                'Python developer with 3 years experience in Django, Flask, and machine learning',
                'Data analyst with expertise in SQL, Python, Tableau, and statistical analysis',
                'Management consultant with experience in strategy, process improvement, and client relations',
                'Full-stack developer proficient in React, Node.js, and database design',
                'Business analyst with skills in data visualization, Excel, and business intelligence'
            ],
            'job_field': [
                'Software Engineering',
                'Data Analyst',
                'Consultant',
                'Software Engineering',
                'Data Analyst'
            ]
        }
        
        df = pd.DataFrame(sample_data)
        df.to_csv(sample_data_file, index=False)
        print(f"Created sample training data: {sample_data_file}")
    
    print("Setup completed successfully!")

if __name__ == "__main__":
    setup_environment()
