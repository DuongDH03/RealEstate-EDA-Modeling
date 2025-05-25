import os
import streamlit as st
import webbrowser
import time
import subprocess
import signal
import sys

def run_streamlit_app():
    """Run the Streamlit app and open it in a browser."""
    print("Starting Real Estate Price Predictor app...")
    
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Change to the application directory if needed
    os.chdir(current_dir)
    
    # Check if model files exist, if not, print a warning
    if not os.path.exists('xgboost_model.joblib'):
        print("Warning: XGBoost model file not found. App will fall back to KNN if available.")
    
    if not os.path.exists('model_features.pkl'):
        print("Warning: Model features file not found. App will use default features.")
    
    # Start Streamlit in a subprocess
    cmd = "streamlit run app.py --server.port=8501 --server.headless=true"
    process = subprocess.Popen(cmd, shell=True)
    
    # Wait a moment for the server to start
    time.sleep(3)
    
    # Open the browser using the system's default browser
    url = "http://localhost:8501"
    print(f"Opening {url} in your browser...")
    
    # Use the $BROWSER environment variable if running in a container
    if 'BROWSER' in os.environ:
        browser_cmd = f"{os.environ['BROWSER']} {url}"
        subprocess.Popen(browser_cmd, shell=True)
    else:
        # Default browser opening mechanism
        webbrowser.open(url)
    
    print("\nStreamlit app is running! Press Ctrl+C to stop.")
    
    try:
        # Keep the script running until keyboard interrupt
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping the Streamlit app...")
        # Kill the process gracefully
        process.send_signal(signal.SIGTERM)
        process.wait()
        print("App stopped successfully!")

if __name__ == "__main__":
    run_streamlit_app()
