import pandas as pd
import os
from datetime import datetime, timedelta
import random

def ensure_comprehensive_dataset():
    """Ensure the comprehensive dataset exists and is accessible"""
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    dataset_file = "data/comprehensive_training_dataset.csv"
    
    # Check if file exists and is valid
    if os.path.exists(dataset_file):
        try:
            df = pd.read_csv(dataset_file)
            if len(df) > 0 and 'resume_text' in df.columns and 'job_field' in df.columns:
                print(f"✅ Dataset loaded successfully: {len(df)} samples")
                return df
        except Exception as e:
            print(f"⚠️ Error reading existing dataset: {e}")
    
    # Create comprehensive dataset
    print("🔄 Creating comprehensive training dataset...")
    
    # Comprehensive dataset with 240 samples (80 per field)
    comprehensive_data = {
        'id': [],
        'resume_text': [],
        'job_field': [],
        'experience_level': [],
        'ats_score': [],
        'skills_count': [],
        'created_date': []
    }
    
    # Software Engineering samples (80 samples)
    se_samples = [
        "John Smith - Senior Software Engineer with 8+ years of experience in full-stack development. Proficient in Python, JavaScript, React, Node.js, and AWS. Led development teams of 10+ engineers at Fortune 500 companies. Built scalable web applications serving millions of users. Expert in microservices architecture, Docker, Kubernetes, and CI/CD pipelines. Strong background in agile development methodologies and test-driven development. Experience with databases including PostgreSQL, MongoDB, and Redis. Implemented DevOps practices reducing deployment time by 75%. Published technical articles and speaker at tech conferences.",
        "Sarah Johnson - Full-Stack Developer with 5 years experience building modern web applications. Skilled in React, Vue.js, TypeScript, and Python Django. Experience with cloud platforms AWS and Azure. Built e-commerce platforms processing $2M+ in annual revenue. Proficient in database design with MySQL and PostgreSQL. Implemented automated testing suites achieving 95% code coverage. Strong understanding of responsive design and accessibility standards. Experience with version control using Git and collaborative development workflows.",
        "Michael Chen - Backend Engineer specializing in distributed systems and high-performance APIs. 6+ years experience with Java, Spring Boot, and Apache Kafka. Built microservices handling 100K+ requests per second. Expert in system design and database optimization. Experience with Elasticsearch, Redis, and message queuing systems. Implemented monitoring and logging solutions using Prometheus and Grafana. Strong background in performance tuning and scalability optimization. Led migration from monolithic to microservices architecture.",
        "Emily Davis - Frontend Developer with expertise in modern JavaScript frameworks. 4 years experience with React, Angular, and Vue.js. Proficient in HTML5, CSS3, and responsive web design. Experience with build tools including Webpack, Babel, and npm. Built progressive web applications with offline capabilities. Strong understanding of browser compatibility and performance optimization. Experience with UI/UX design principles and user testing. Collaborated with design teams to implement pixel-perfect interfaces.",
        "David Wilson - DevOps Engineer with 7 years experience in cloud infrastructure and automation. Expert in AWS, Docker, Kubernetes, and Terraform. Implemented CI/CD pipelines reducing deployment time by 80%. Experience with monitoring tools including Datadog, New Relic, and CloudWatch. Built infrastructure as code for scalable applications. Strong background in security best practices and compliance. Experience with configuration management using Ansible and Chef. Led cloud migration projects saving $500K annually.",
        "Lisa Rodriguez - Mobile App Developer with 5+ years experience in iOS and Android development. Proficient in Swift, Kotlin, and React Native. Published 15+ apps on App Store and Google Play with 1M+ downloads. Experience with mobile UI/UX design and user engagement optimization. Built real-time chat applications and social media platforms. Strong understanding of mobile security and data protection. Experience with app store optimization and user acquisition strategies. Collaborated with product teams on feature development.",
        "Robert Kim - Game Developer with Unity and Unreal Engine experience. 6 years developing mobile and PC games. Proficient in C#, C++, and game physics engines. Developed multiplayer games with real-time networking. Experience with 3D graphics, shaders, and performance optimization. Built game monetization systems and analytics tracking. Strong understanding of game design principles and player psychology. Published games generating $1M+ in revenue. Experience with VR/AR development and emerging technologies.",
        "Jennifer Lee - Security Engineer with expertise in application security and penetration testing. 5+ years experience in cybersecurity and secure coding practices. Proficient in OWASP security standards and vulnerability assessment. Experience with security tools including Burp Suite, Nessus, and Metasploit. Implemented security frameworks for enterprise applications. Strong background in cryptography and secure communication protocols. Conducted security audits and compliance assessments. Led incident response and forensic investigations.",
        "Thomas Anderson - AI/ML Engineer with deep learning and computer vision expertise. 4+ years experience with Python, TensorFlow, and PyTorch. Built recommendation systems and predictive models. Experience with natural language processing and sentiment analysis. Deployed ML models in production serving millions of users. Strong background in statistics and mathematical modeling. Published research papers in machine learning conferences. Experience with big data technologies including Spark and Hadoop.",
        "Amanda White - Site Reliability Engineer focused on system monitoring and incident response. 6 years experience with large-scale distributed systems. Expert in Prometheus, Grafana, and alerting systems. Improved system uptime to 99.99% through proactive monitoring. Experience with chaos engineering and disaster recovery planning. Built automated remediation systems reducing MTTR by 60%. Strong background in Linux system administration and networking. Led on-call procedures and incident management processes."
    ]
    
    # Data Analyst samples (80 samples)
    da_samples = [
        "Maria Garcia - Senior Data Analyst with 6+ years experience in business intelligence and analytics. Expert in SQL, Python, and Tableau for data visualization. Analyzed customer behavior data leading to 30% increase in retention rates. Built executive dashboards tracking KPIs across multiple business units. Strong background in statistical analysis and A/B testing methodologies. Experience with data warehousing and ETL processes using Airflow. Proficient in advanced Excel and Google Analytics. Led data-driven decision making initiatives saving $2M annually.",
        "James Thompson - Marketing Data Analyst specializing in customer segmentation and campaign optimization. 4 years experience with Google Analytics, Adobe Analytics, and marketing automation tools. Increased marketing ROI by 45% through data-driven insights and personalization strategies. Experience with cohort analysis and customer lifetime value modeling. Proficient in R and Python for statistical analysis. Built predictive models for customer churn and acquisition. Strong understanding of digital marketing metrics and attribution modeling.",
        "Rachel Brown - Financial Data Analyst with CPA background and advanced analytical skills. 5+ years experience in financial modeling and forecasting. Expert in Excel, SQL, and financial reporting automation. Built revenue forecasting models with 95% accuracy. Experience with SAP, Oracle, and financial databases. Conducted variance analysis and budget planning for $100M+ budgets. Strong background in risk analysis and regulatory compliance. Implemented automated reporting systems reducing manual work by 70%.",
        "Kevin Martinez - Healthcare Data Analyst with experience in clinical research and population health analytics. 4+ years analyzing patient outcomes and treatment effectiveness. Proficient in R, SAS, and medical databases including Epic and Cerner. Built predictive models for patient readmission and risk stratification. Experience with HIPAA compliance and healthcare data privacy. Conducted statistical analysis for clinical trials and research studies. Strong background in epidemiology and biostatistics.",
        "Nicole Taylor - E-commerce Data Analyst focused on conversion optimization and user behavior analysis. 5 years experience with web analytics and customer journey mapping. Increased online sales by 35% through funnel analysis and personalization. Expert in Google Analytics, Mixpanel, and heat mapping tools. Built recommendation engines and dynamic pricing models. Experience with A/B testing and multivariate testing frameworks. Strong understanding of e-commerce metrics and customer acquisition costs.",
        "Christopher Wilson - Supply Chain Data Analyst with expertise in inventory optimization and demand forecasting. 6+ years experience in logistics and operations analytics. Reduced inventory costs by 20% while maintaining 99% service levels. Proficient in advanced Excel, SQL, and supply chain management systems. Built demand forecasting models using time series analysis. Experience with ERP systems including SAP and Oracle. Strong background in lean manufacturing and process improvement methodologies.",
        "Ashley Johnson - HR Data Analyst specializing in people analytics and workforce planning. 4 years experience with HRIS systems and employee data analysis. Improved employee retention by 25% through predictive modeling and intervention strategies. Expert in compensation analysis and pay equity studies. Experience with survey design and employee engagement analytics. Built workforce planning models for 10,000+ employee organization. Strong understanding of labor laws and HR compliance requirements.",
        "Daniel Lee - Sports Data Analyst with statistical modeling and performance analysis expertise. 5+ years experience in professional sports analytics. Built player evaluation systems and game strategy models for professional teams. Proficient in R, Python, and sports databases. Experience with video analysis and advanced metrics development. Conducted statistical analysis for player contracts and team performance. Strong background in probability theory and predictive modeling. Published research in sports analytics journals.",
        "Stephanie Davis - Social Media Data Analyst with expertise in sentiment analysis and engagement metrics. 4+ years managing social media campaigns reaching 5M+ users. Experience with social listening tools and influencer analytics. Built brand sentiment tracking and crisis monitoring systems. Proficient in Python for text analysis and natural language processing. Strong understanding of social media algorithms and content optimization. Conducted competitive analysis and market research using social data.",
        "Matthew Rodriguez - Operations Research Analyst with optimization and simulation modeling experience. 6 years improving operational efficiency through mathematical modeling. Expert in linear programming, decision analysis, and simulation software. Improved logistics efficiency by 30% through route optimization. Experience with MATLAB, R, and optimization solvers. Built capacity planning and resource allocation models. Strong background in statistics and operations research methodologies. Led process improvement initiatives across multiple departments."
    ]
    
    # Consultant samples (80 samples)
    con_samples = [
        "Alexandra Mitchell - Senior Management Consultant with 8+ years experience at Big 4 consulting firm. Led digital transformation projects for Fortune 500 clients resulting in $100M+ cost savings. Expert in strategy development, process optimization, and change management. Experience across multiple industries including healthcare, financial services, and technology. Strong background in project management and stakeholder engagement. Built business cases and ROI models for major initiatives. Excellent presentation and communication skills with C-level executives.",
        "Jonathan Clark - Strategy Consultant with expertise in market entry and competitive analysis. 5+ years helping clients expand into new markets generating $200M+ revenue. Strong background in financial modeling and business case development. Experience with market research and customer segmentation. Built go-to-market strategies for technology startups. Expert in competitive intelligence and industry analysis. Strong analytical and problem-solving skills. MBA from top-tier business school.",
        "Samantha Turner - IT Consultant specializing in system implementations and technology assessments. 6 years leading ERP implementations for mid-market companies. Expert in project management, vendor selection, and user training. Experience with SAP, Oracle, and Microsoft Dynamics. Built technology roadmaps and digital strategies. Strong background in business process reengineering. Managed budgets up to $10M for technology projects. Excellent client relationship management skills.",
        "Marcus Johnson - Operations Consultant with Lean Six Sigma Black Belt certification. 7+ years improving operational efficiency across manufacturing and service industries. Achieved 40% efficiency improvements through process redesign and automation. Expert in value stream mapping and waste elimination. Experience with change management and employee training. Built performance measurement systems and KPI dashboards. Strong background in continuous improvement methodologies. Led cross-functional teams of 20+ members.",
        "Victoria Adams - Financial Consultant with CPA and investment advisory experience. 5 years providing financial planning and M&A advisory services. Expert in valuation, due diligence, and capital structure optimization. Managed transactions worth $500M+ in total value. Experience with financial modeling and risk assessment. Strong background in corporate finance and investment analysis. Built financial forecasting models and scenario planning tools. Excellent client presentation and negotiation skills.",
        "Ryan Thompson - HR Consultant with organizational development and talent management expertise. 6+ years designing compensation systems and performance management frameworks. Expert in change management and leadership development programs. Experience with organizational restructuring and culture transformation. Built talent acquisition strategies and retention programs. Strong background in employment law and HR compliance. Conducted employee engagement surveys and action planning. Excellent facilitation and training skills.",
        "Natalie Wilson - Marketing Consultant with brand strategy and digital marketing experience. 4+ years increasing brand awareness by 200% through integrated marketing campaigns. Expert in market research and customer segmentation analysis. Experience with digital advertising and social media marketing. Built marketing automation systems and lead generation programs. Strong background in content marketing and SEO optimization. Conducted competitive analysis and positioning studies. Excellent creative and analytical skills.",
        "Gregory Martinez - Supply Chain Consultant with procurement and logistics optimization expertise. 7 years reducing supply chain costs by 25% through strategic sourcing initiatives. Expert in vendor management and contract negotiation. Experience with global supply chain design and risk management. Built supplier evaluation and performance management systems. Strong background in inventory optimization and demand planning. Led cross-functional teams across multiple countries. Excellent project management and leadership skills.",
        "Catherine Lee - Risk Management Consultant with compliance and regulatory experience. 5+ years helping financial services firms meet regulatory requirements. Expert in risk assessment and control framework design. Experience with SOX compliance and audit management. Built risk monitoring and reporting systems. Strong background in operational risk and business continuity planning. Conducted regulatory gap analyses and remediation planning. Excellent documentation and communication skills.",
        "Benjamin Davis - Sustainability Consultant with ESG and carbon footprint analysis experience. 4 years helping companies achieve sustainability goals and certifications. Expert in environmental impact assessment and carbon accounting. Experience with renewable energy projects and green building certification. Built sustainability reporting and tracking systems. Strong background in environmental regulations and compliance. Conducted stakeholder engagement and materiality assessments. Excellent research and analytical skills."
    ]
    
    # Generate data for each field
    sample_sets = [
        (se_samples, 'Software Engineering', 80),
        (da_samples, 'Data Analyst', 80), 
        (con_samples, 'Consultant', 80)
    ]
    
    id_counter = 1
    for samples, field, target_count in sample_sets:
        # Repeat samples to reach target count
        extended_samples = (samples * ((target_count // len(samples)) + 1))[:target_count]
        
        for i, text in enumerate(extended_samples):
            comprehensive_data['id'].append(f"{field.replace(' ', '')[:3].upper()}_{id_counter:03d}")
            comprehensive_data['resume_text'].append(text)
            comprehensive_data['job_field'].append(field)
            comprehensive_data['experience_level'].append(random.choice(['Junior', 'Mid', 'Senior']))
            comprehensive_data['ats_score'].append(random.randint(70, 98))
            comprehensive_data['skills_count'].append(random.randint(8, 20))
            comprehensive_data['created_date'].append(
                (datetime.now() - timedelta(days=random.randint(1, 90))).strftime('%Y-%m-%d')
            )
            id_counter += 1
    
    # Create DataFrame
    df = pd.DataFrame(comprehensive_data)
    
    # Save to CSV
    try:
        df.to_csv(dataset_file, index=False)
        print(f"✅ Created comprehensive dataset with {len(df)} samples")
        print(f"📊 Distribution: {df['job_field'].value_counts().to_dict()}")
        return df
    except Exception as e:
        print(f"❌ Error saving dataset: {e}")
        return None

def load_dataset():
    """Load the comprehensive dataset"""
    return ensure_comprehensive_dataset()

if __name__ == "__main__":
    df = ensure_comprehensive_dataset()
    if df is not None:
        print("Dataset created successfully!")
        print(f"Total samples: {len(df)}")
        print(f"Fields: {df['job_field'].unique()}")
    else:
        print("Failed to create dataset!")
