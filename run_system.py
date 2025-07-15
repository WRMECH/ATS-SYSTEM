#!/usr/bin/env python3
"""
Enhanced startup script for the Resume Screening System
"""

import os
import sys
import subprocess
import time
import platform

def print_banner():
    """Print startup banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                                                              ║
    ║        🚀 AI RESUME SCREENING SYSTEM 🎯                     ║
    ║                                                              ║
    ║        ⚡ POWERED BY TECHY GANG ⚡            ║
    ║                                                              ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)
    print("🔧 Starting system setup and initialization...")
    print("=" * 60)

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please upgrade Python and try again")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def check_requirements():
    """Check if required packages are installed"""
    print("📦 Checking required packages...")
    
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'scikit-learn',
        'nltk', 'PyPDF2', 'python-docx', 'plotly'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'python-docx':
                __import__('docx')
            elif package == 'PyPDF2':
                __import__('PyPDF2')
            elif package == 'scikit-learn':
                __import__('sklearn')
            else:
                __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package} - Missing")
    
    if missing_packages:
        print(f"\n📥 Installing missing packages: {', '.join(missing_packages)}")
        
        try:
            subprocess.check_call([
                sys.executable, '-m', 'pip', 'install', '--upgrade'
            ] + missing_packages)
            print("✅ All packages installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install packages: {e}")
            print("💡 Try running: pip install -r requirements.txt")
            return False
    else:
        print("✅ All required packages are installed")
    
    return True

def setup_environment():
    """Setup the environment"""
    print("⚙️ Setting up environment...")
    
    # Create directories
    directories = ['data', 'models', 'temp', 'logs']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   📂 Created directory: {directory}")
        else:
            print(f"   ✅ Directory exists: {directory}")
    
    # Check for dataset files
    dataset_files = [
        "data/comprehensive_training_dataset.csv",
        "data/training_dataset_200.csv"
    ]
    
    dataset_found = False
    for dataset_file in dataset_files:
        if os.path.exists(dataset_file):
            print(f"✅ Dataset found: {dataset_file}")
            dataset_found = True
            break
    
    if not dataset_found:
        print("⚠️ No training dataset found!")
        print("💡 Please ensure you have one of these files:")
        for file in dataset_files:
            print(f"   - {file}")
        print("📝 The comprehensive dataset should be included with the system files")
    
    # Download NLTK data
    try:
        import nltk
        print("📚 Downloading NLTK data...")
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        print("✅ NLTK data downloaded")
    except Exception as e:
        print(f"⚠️ NLTK download warning: {e}")
    
    print("✅ Environment setup complete")
    return True

def run_tests():
    """Run system tests"""
    print("🧪 Running system tests...")
    
    try:
        # Import test module
        from test_system import main as run_tests_main
        
        # Run tests
        success = run_tests_main()
        
        if success:
            print("✅ All tests passed!")
            return True
        else:
            print("⚠️ Some tests failed, but continuing...")
            return True  # Continue even if some tests fail
            
    except Exception as e:
        print(f"⚠️ Test execution warning: {e}")
        return True  # Continue even if tests can't run

def get_system_info():
    """Get system information"""
    print("💻 System Information:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Python: {sys.version.split()[0]}")
    print(f"   Architecture: {platform.machine()}")
    
    # Check available memory (if psutil is available)
    try:
        import psutil
        memory = psutil.virtual_memory()
        print(f"   RAM: {memory.total // (1024**3)} GB total, {memory.available // (1024**3)} GB available")
    except ImportError:
        print("   RAM: Unable to detect (psutil not installed)")

def start_streamlit():
    """Start the Streamlit application"""
    print("🚀 Starting Resume Screening System...")
    print("📱 The application will open in your default web browser")
    print("🔗 URL: http://localhost:8501")
    print("\n" + "="*60)
    print("🎯 RESUME SCREENING SYSTEM IS STARTING...")
    print("="*60)
    print("\n💡 Tips:")
    print("   • Upload PDF, DOCX, or TXT resume files")
    print("   • Try different job fields for analysis")
    print("   • Check the Analytics Dashboard for insights")
    print("   • Use Ctrl+C to stop the application")
    print("\n" + "="*60)
    
    try:
        # Start Streamlit with optimized settings
        cmd = [
            sys.executable, '-m', 'streamlit', 'run', 'app.py',
            '--server.port', '8501',
            '--server.address', 'localhost',
            '--server.headless', 'false',
            '--browser.gatherUsageStats', 'false'
        ]
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
        print("✅ Shutdown complete")
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Check if port 8501 is available")
        print("   2. Try: streamlit run app.py --server.port 8502")
        print("   3. Ensure all dependencies are installed")

def main():
    """Main startup function"""
    print_banner()
    
    # Step 1: Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        return False
    
    # Step 2: Get system info
    get_system_info()
    print()
    
    # Step 3: Check requirements
    if not check_requirements():
        print("❌ Requirements check failed")
        input("Press Enter to exit...")
        return False
    
    # Step 4: Setup environment
    if not setup_environment():
        print("❌ Environment setup failed")
        input("Press Enter to exit...")
        return False
    
    # Step 5: Ask about tests
    print("\n🧪 Would you like to run system tests? (recommended for first run)")
    print("   y/yes - Run tests")
    print("   n/no  - Skip tests")
    print("   Enter - Skip tests")
    
    choice = input("Choice: ").lower().strip()
    
    if choice in ['y', 'yes']:
        run_tests()
        print()
    
    # Step 6: Final confirmation
    print("🎯 Ready to start the Resume Screening System!")
    print("   The application will start in a few seconds...")
    
    # Small delay for user to read
    time.sleep(3)
    
    # Step 7: Start application
    start_streamlit()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if not success:
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Startup cancelled by user")
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        print("\n🔧 Please check the README.md for manual setup instructions")
        input("Press Enter to exit...")
        sys.exit(1)
