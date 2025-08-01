"""
Setup script for AI-Powered Influencer Research Tool
"""

import subprocess
import sys
import os
import toml

def install_requirements():
    """Install required Python packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Packages installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages. Please run manually: pip install -r requirements.txt")
        return False
    return True

def setup_secrets():
    """Help user set up API keys"""
    print("\n🔑 Setting up API keys...")
    
    if not os.path.exists("secrets.toml"):
        print("❌ secrets.toml file not found!")
        return False
    
    try:
        secrets = toml.load("secrets.toml")
        
        # Check if keys are still placeholder values
        qloo_key = secrets.get('default', {}).get('QLOO_API_KEY', '')
        perplexity_key = secrets.get('default', {}).get('PERPLEXITY_API_KEY', '')
        openai_key = secrets.get('default', {}).get('OPENAI_API_KEY', '')
        
        keys_needed = []
        if qloo_key == 'your_qloo_api_key_here':
            keys_needed.append('Qloo API Key')
        if perplexity_key == 'your_perplexity_api_key_here':
            keys_needed.append('Perplexity API Key')
        if openai_key == 'your_openai_api_key_here':
            keys_needed.append('OpenAI API Key')
        
        if keys_needed:
            print(f"⚠️  Please update the following API keys in secrets.toml:")
            for key in keys_needed:
                print(f"   - {key}")
            print("\n📝 Edit the secrets.toml file and replace placeholder values with your actual API keys.")
            return False
        else:
            print("✅ API keys appear to be configured!")
            return True
            
    except Exception as e:
        print(f"❌ Error reading secrets.toml: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 AI-Powered Influencer Research Tool Setup")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Setup secrets
    secrets_ok = setup_secrets()
    
    print("\n" + "=" * 50)
    print("🎯 Setup Summary:")
    print("✅ Requirements installed")
    if secrets_ok:
        print("✅ API keys configured")
        print("\n🚀 Ready to launch! Run:")
        print("   streamlit run influencer_research_app.py")
    else:
        print("⚠️  API keys need configuration")
        print("\n📝 Next steps:")
        print("   1. Edit secrets.toml with your actual API keys")
        print("   2. Run: streamlit run influencer_research_app.py")
    
    print("\n📚 For detailed instructions, see README.md")

if __name__ == "__main__":
    main()
