import os
from google_auth_oauthlib.flow import InstalledAppFlow

# The scopes needed for the fetcher
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

def generate_refresh_token():
    """
    To use this script:
    1. Go to Google Cloud Console (console.cloud.google.com)
    2. Create a project and enable the Gmail API
    3. Create OAuth 2.0 Client IDs (Type: Desktop App)
    4. Download the JSON and save it as 'credentials.json' in this folder
    5. Run this script. It will open a browser to authenticate.
    """
    if not os.path.exists("credentials.json"):
        print("Error: 'credentials.json' not found in the current directory.")
        print("Please download it from Google Cloud Console and try again.")
        return

    print("Starting OAuth flow. Check your browser to authenticate...")
    flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
    
    # run_local_server will attempt to open the browser automatically
    creds = flow.run_local_server(port=0)
    
    print("\n" + "="*50)
    print("SUCCESS! Replace the token in your .env with this:")
    print("GOOGLE_REFRESH_TOKEN=" + str(creds.refresh_token))
    print("="*50 + "\n")

if __name__ == "__main__":
    generate_refresh_token()
