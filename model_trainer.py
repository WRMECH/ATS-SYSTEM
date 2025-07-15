import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, classification_report
import pickle
import os
import json
from datetime import datetime

class ModelTrainer:
    def __init__(self):
        self.models = {
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
            'SVM': SVC(probability=True, random_state=42)
        }
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.best_model = None
        self.best_score = 0
        self.best_model_name = None
    
    def preprocess_text(self, text):
        """Clean and preprocess text for training"""
        import re
        text = str(text).lower()
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text
    
    def prepare_data(self, df):
        """Prepare training data"""
        required_columns = ['resume_text', 'job_field']
        for col in required_columns:
            if col not in df.columns:
                raise ValueError(f"Missing required column: {col}")
        df['cleaned_text'] = df['resume_text'].apply(self.preprocess_text)
        df = df[df['cleaned_text'].str.len() > 0]
        return df
    
    def load_training_data(self):
        """Load training data from the dataset loader"""
        try:
            from dataset_loader import load_dataset
            df = load_dataset()
    
            if df is not None and len(df) > 0:
                print(f"✅ Loaded comprehensive dataset: {len(df)} samples")
                return df
            else:
                print("❌ Failed to load dataset from dataset_loader")
                return None
            
        except ImportError:
            print("⚠️ Dataset loader not available, using fallback method")
            # Fallback to original method
            dataset_files = [
                "data/comprehensive_training_dataset.csv",
                "data/training_dataset_200.csv"
            ]
    
            for dataset_file in dataset_files:
                if os.path.exists(dataset_file):
                    try:
                        df = pd.read_csv(dataset_file)
                        print(f"✅ Loaded dataset: {dataset_file} ({len(df)} samples)")
                        return df
                    except Exception as e:
                        print(f"⚠️ Error loading {dataset_file}: {e}")
                        continue
    
            print("❌ No dataset files found")
            return None

        except Exception as e:
            print(f"❌ Error in load_training_data: {e}")
            return None

    def train_models(self, df=None):
        """Train multiple models and select the best one"""
        try:
            if df is None:
                df = self.load_training_data()
        
            if df is None or len(df) == 0:
                return {
                    'training_completed': False,
                    'error': 'No training data available'
                }
        
            df = self.prepare_data(df)
            X = df['cleaned_text']
            y = df['job_field']
        
            X_vectorized = self.vectorizer.fit_transform(X)
        
            try:
                X_train, X_test, y_train, y_test = train_test_split(
                    X_vectorized, y, test_size=0.2, random_state=42, stratify=y
                )
            except ValueError:
                X_train, X_test, y_train, y_test = train_test_split(
                    X_vectorized, y, test_size=0.2, random_state=42
                )
        
            results = {}
        
            for model_name, model in self.models.items():
                print(f"Training {model_name}...")
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
                recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
                results[model_name] = {
                    'accuracy': accuracy,
                    'precision': precision,
                    'recall': recall,
                    'model': model
                }
                if accuracy > self.best_score:
                    self.best_score = accuracy
                    self.best_model = model
                    self.best_model_name = model_name
        
            self.save_models_and_results(results)
        
            return {
                'training_completed': True,
                'best_model': self.best_model_name,
                'best_accuracy': self.best_score,
                'all_results': {k: {
                    'accuracy': v['accuracy'],
                    'precision': v['precision'],
                    'recall': v['recall']
                } for k, v in results.items()}
            }
        
        except Exception as e:
            return {
                'training_completed': False,
                'error': str(e)
            }
    
    def save_models_and_results(self, results):
        """Save trained models and performance metrics"""
        os.makedirs('models', exist_ok=True)
        
        if self.best_model is not None:
            with open('models/field_classifier.pkl', 'wb') as f:
                pickle.dump(self.best_model, f)
        
        with open('models/vectorizer.pkl', 'wb') as f:
            pickle.dump(self.vectorizer, f)
        
        metrics = {k: {
            'accuracy': v['accuracy'],
            'precision': v['precision'],
            'recall': v['recall']
        } for k, v in results.items()}
        
        with open('models/performance_metrics.json', 'w') as f:
            json.dump(metrics, f, indent=2)
        
        metadata = {
            'training_date': datetime.now().isoformat(),
            'best_model': self.best_model_name,
            'best_accuracy': self.best_score,
            'models_trained': list(self.models.keys())
        }
        
        with open('models/training_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def load_model(self):
        """Load trained model"""
        try:
            with open('models/field_classifier.pkl', 'rb') as f:
                model = pickle.load(f)
            with open('models/vectorizer.pkl', 'rb') as f:
                vectorizer = pickle.load(f)
            return model, vectorizer
        except FileNotFoundError:
            return None, None
    
    def predict_field(self, resume_text):
        """Predict job field for a resume"""
        model, vectorizer = self.load_model()
        if model is None or vectorizer is None:
            return None
        cleaned_text = self.preprocess_text(resume_text)
        text_vector = vectorizer.transform([cleaned_text])
        prediction = model.predict(text_vector)[0]
        probabilities = model.predict_proba(text_vector)[0]
        classes = model.classes_
        prob_dict = dict(zip(classes, probabilities))
        return {
            'predicted_field': prediction,
            'confidence': max(probabilities),
            'all_probabilities': prob_dict
        }
