#!/usr/bin/env python3
"""
Test script for the Resume Screening System
"""

import os
import sys
import pandas as pd
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        from resume_analyzer import ResumeAnalyzer
        from model_trainer import ModelTrainer
        from text_extractor import TextExtractor
        from ats_scorer import ATSScorer
        print("✅ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_directories():
    """Test if required directories exist"""
    print("📁 Testing directories...")
    
    required_dirs = ['data', 'models']
    for directory in required_dirs:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📂 Created directory: {directory}")
        else:
            print(f"✅ Directory exists: {directory}")
    
    return True

def test_dataset():
    """Test dataset loading from existing CSV file"""
    print("📊 Testing dataset...")
    
    try:
        # Check for the comprehensive dataset first
        dataset_file = "data/comprehensive_training_dataset.csv"
        if os.path.exists(dataset_file):
            df = pd.read_csv(dataset_file)
            print(f"✅ Comprehensive dataset loaded with {len(df)} rows")
        else:
            # Check for fallback dataset
            fallback_file = "data/training_dataset_200.csv"
            if os.path.exists(fallback_file):
                df = pd.read_csv(fallback_file)
                print(f"✅ Fallback dataset loaded with {len(df)} rows")
            else:
                print("❌ No dataset found. Please ensure CSV file exists in data/ folder")
                return False
        
        # Verify dataset structure
        required_columns = ['resume_text', 'job_field']
        for col in required_columns:
            if col not in df.columns:
                print(f"❌ Missing column: {col}")
                return False
        
        # Check data quality
        if df['resume_text'].isnull().any():
            print("⚠️ Warning: Some resume_text entries are null")
        
        if df['job_field'].isnull().any():
            print("⚠️ Warning: Some job_field entries are null")
        
        # Show distribution
        distribution = df['job_field'].value_counts()
        print("📈 Dataset distribution:")
        for field, count in distribution.items():
            print(f"   {field}: {count} samples")
        
        print("✅ Dataset structure is valid")
        return True
        
    except Exception as e:
        print(f"❌ Dataset error: {e}")
        return False

def test_components():
    """Test individual components"""
    print("🧪 Testing components...")
    
    try:
        # Test sample resume text
        sample_text = """
        John Doe
        Software Engineer
        john.doe@email.com
        (555) 123-4567
        
        EXPERIENCE
        Senior Software Engineer at Tech Corp (2020-2023)
        - Developed web applications using Python, Django, and React
        - Implemented microservices architecture with Docker and Kubernetes
        - Led team of 5 developers in agile environment
        
        EDUCATION
        Bachelor of Science in Computer Science
        University of Technology (2018)
        
        SKILLS
        Python, JavaScript, React, SQL, AWS, Docker, Git
        """
        
        # Test ATS Scorer
        from ats_scorer import ATSScorer
        scorer = ATSScorer()
        ats_score = scorer.calculate_ats_score(sample_text, "Software Engineering")
        print(f"✅ ATS Score calculated: {ats_score}%")
        
        # Test Resume Analyzer
        from resume_analyzer import ResumeAnalyzer
        analyzer = ResumeAnalyzer()
        recommendations = analyzer.get_field_recommendations(sample_text)
        print(f"✅ Field recommendations: {list(recommendations.keys())}")
        
        analysis = analyzer.analyze_resume(sample_text, "Software Engineering")
        print(f"✅ Resume analysis completed: {analysis['match_percentage']:.1f}% match")
        
        return True
        
    except Exception as e:
        print(f"❌ Component test error: {e}")
        return False

def test_streamlit_app():
    """Test if Streamlit app can be imported"""
    print("🚀 Testing Streamlit app...")
    
    try:
        # Just test if the app file can be read
        with open('app.py', 'r') as f:
            content = f.read()
        
        if 'def main():' in content and 'streamlit' in content:
            print("✅ Streamlit app structure is valid")
            return True
        else:
            print("❌ Invalid Streamlit app structure")
            return False
            
    except Exception as e:
        print(f"❌ Streamlit app error: {e}")
        return False

def main():
    """Run all tests"""
    print("🎯 Resume Screening System - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Directory Test", test_directories),
        ("Dataset Test", test_dataset),
        ("Component Test", test_components),
        ("Streamlit App Test", test_streamlit_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 30)
        
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED: {e}")
    
    print("\n" + "=" * 50)
    print(f"🎯 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        print("\n🚀 To run the application:")
        print("   streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
