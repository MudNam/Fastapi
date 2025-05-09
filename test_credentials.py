from google.cloud import storage
import os

def test_credentials():
    try:
        # Print the credentials path
        print(f"Looking for credentials at: {os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')}")
        
        # Try to create a storage client
        client = storage.Client()
        
        # Try to list buckets
        buckets = list(client.list_buckets())
        
        print("✅ Credentials are working!")
        print(f"Found {len(buckets)} buckets:")
        for bucket in buckets:
            print(f"- {bucket.name}")
            
    except Exception as e:
        print("❌ Error with credentials:")
        print(str(e))

if __name__ == "__main__":
    test_credentials() 