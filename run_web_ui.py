#!/usr/bin/env python3
"""
Launch script for the Configurable LangGraph Agents Web UI
"""
import subprocess
import sys
import os

def check_streamlit():
    """Check if Streamlit is available."""
    try:
        import streamlit
        return True
    except ImportError:
        return False

def activate_venv_and_run():
    """Activate virtual environment and run Streamlit."""
    venv_path = os.path.join(os.path.dirname(__file__), '.venv')
    if os.path.exists(venv_path):
        print("🔧 Activating virtual environment...")
        if sys.platform == "win32":
            # Windows
            activate_script = os.path.join(venv_path, 'Scripts', 'activate.bat')
            cmd = f'"{activate_script}" && python -m streamlit run web_ui.py'
            subprocess.run(cmd, shell=True)
        else:
            # Unix/Linux/macOS
            activate_script = os.path.join(venv_path, 'bin', 'activate')
            cmd = f'source "{activate_script}" && python -m streamlit run web_ui.py'
            subprocess.run(cmd, shell=True, executable='/bin/bash')
    else:
        print("❌ Virtual environment not found. Please run: python3 -m venv .venv")
        print("Then: source .venv/bin/activate && pip install -r requirements.txt")

def main():
    """Main function to launch the Web UI."""
    print("🚀 Launching Configurable LangGraph Agents Web UI...")
    
    # Check if Streamlit is available
    if check_streamlit():
        print("✅ Streamlit is available. Starting Web UI...")
        try:
            subprocess.run([sys.executable, "-m", "streamlit", "run", "web_ui.py"])
        except KeyboardInterrupt:
            print("\n👋 Web UI stopped by user.")
        except Exception as e:
            print(f"❌ Error starting Web UI: {e}")
    else:
        print("❌ Streamlit is not installed.")
        print("🔧 Attempting to use virtual environment...")
        activate_venv_and_run()

if __name__ == "__main__":
    main() 