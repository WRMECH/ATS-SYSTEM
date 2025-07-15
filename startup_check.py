import os
import sys

def ensure_system_ready():
    """Ensure the system is ready with all required components"""
    
    print("🔧 Checking system components...")
    
    # Check if data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
        print("📂 Created data directory")
    
    # Ensure dataset is available
    try:
        from dataset_loader import ensure_comprehensive_dataset
        df = ensure_comprehensive_dataset()
        
        if df is not None:
            print(f"✅ Dataset ready: {len(df)} samples")
            return True
        else:
            print("❌ Dataset creation failed")
            return False
            
    except Exception as e:
        print(f"❌ System check failed: {e}")
        return False

if __name__ == "__main__":
    if ensure_system_ready():
        print("🚀 System ready!")
    else:
        print("❌ System not ready!")
        sys.exit(1)
