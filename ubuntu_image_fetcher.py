#!/usr/bin/env python3
"""
Ubuntu-Inspired Image Fetcher
A tool for mindfully collecting and sharing images from the web community.
Embracing the principle: "I am because we are"
"""

import requests
import os
import hashlib
from urllib.parse import urlparse
from pathlib import Path

def get_filename_from_url(url, response):
    """
    Extracts a filename from the URL or the HTTP Content-Disposition header.
    Generates a fallback name if none is found.
    """
    # First, try to get the filename from the URL path
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    
    # If the URL doesn't contain a clear filename, check the Content-Disposition header
    if not filename or '.' not in filename:
        content_disp = response.headers.get('Content-Disposition', '')
        if 'filename=' in content_disp:
            filename = content_disp.split('filename=')[1].strip('"\'')
    
    # If still no valid filename, generate one based on the URL's MD5 hash
    if not filename or '.' not in filename:
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        # Try to determine the file extension from the Content-Type header
        content_type = response.headers.get('Content-Type', '')
        if 'image/' in content_type:
            ext = content_type.split('/')[1]
            # Handle common MIME type variations
            if ext == 'jpeg':
                ext = 'jpg'
            filename = f"downloaded_image_{url_hash}.{ext}"
        else:
            # Fallback if Content-Type is not helpful
            filename = f"downloaded_image_{url_hash}.bin"
            
    return filename

def is_duplicate_image(filepath, content):
    """
    Checks if an image with the same content already exists to prevent duplicates.
    Uses MD5 hash comparison for efficiency.
    """
    if not os.path.exists(filepath):
        return False
    
    # Calculate hash of the new content
    new_content_hash = hashlib.md5(content).hexdigest()
    
    # Calculate hash of the existing file
    try:
        with open(filepath, 'rb') as f:
            existing_content_hash = hashlib.md5(f.read()).hexdigest()
        return new_content_hash == existing_content_hash
    except IOError:
        return False

def download_image(url, download_dir="Fetched_Images"):
    """
    Downloads an image from a given URL and saves it to the specified directory.
    Returns a status message and success boolean.
    """
    try:
        # Create directory if it doesn't exist (with Ubuntu-inspired permissions)
        os.makedirs(download_dir, exist_ok=True)
        
        # Set a respectful user-agent header
        headers = {
            'User-Agent': 'UbuntuImageFetcher/1.0 (Community Education Tool)'
        }
        
        print(f"Connecting to the community at {urlparse(url).netloc}...")
        
        # Fetch the image with timeout and headers
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()  # Respect the server's response
        
        # Check if this is actually an image before proceeding
        content_type = response.headers.get('Content-Type', '')
        if not content_type.startswith('image/'):
            return (f"✗ Respectful warning: The URL does not point to an image (Content-Type: {content_type}).", False)
        
        # Check content length to avoid very large files
        content_length = response.headers.get('Content-Length')
        if content_length and int(content_length) > 10 * 1024 * 1024:  # 10MB limit
            return ("✗ Respectful warning: File size exceeds 10MB limit.", False)
        
        # Get appropriate filename
        filename = get_filename_from_url(url, response)
        filepath = os.path.join(download_dir, filename)
        
        # Check for duplicate content
        if is_duplicate_image(filepath, response.content):
            return (f"✓ Community resource preserved: '{filename}' already exists in our collection.", True)
        
        # Save the image with community appreciation
        with open(filepath, 'wb') as f:
            f.write(response.content)
            
        return (f"✓ Successfully fetched: {filename}\n✓ Image saved to {filepath}", True)
        
    except requests.exceptions.Timeout:
        return ("✗ Connection timeout: The community member took too long to respond.", False)
    except requests.exceptions.HTTPError as e:
        return (f"✗ HTTP error: The community server responded with {e.response.status_code}", False)
    except requests.exceptions.ConnectionError:
        return ("✗ Connection error: Could not reach the community member.", False)
    except requests.exceptions.RequestException as e:
        return (f"✗ Network error: {e}", False)
    except Exception as e:
        return (f"✗ An unexpected error occurred: {e}", False)

def main():
    """Main function that embodies the Ubuntu philosophy."""
    print("=" * 60)
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web")
    print("Embracing the principle: 'I am because we are'")
    print("=" * 60)
    
    # Get URL(s) from user
    url_input = input("\nPlease enter image URL(s), separated by commas if multiple: ").strip()
    
    if not url_input:
        print("✗ No URL provided. The community connection requires an address.")
        return
    
    urls = [url.strip() for url in url_input.split(',')]
    successful_downloads = 0
    
    for i, url in enumerate(urls, 1):
        if not url:
            continue
            
        print(f"\n--- Processing URL {i} of {len(urls)} ---")
        
        # Validate URL format
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.netloc:
            print(f"✗ Invalid URL: '{url}'. Please use full URLs (e.g., https://example.com/image.jpg)")
            continue
        
        # Download the image with Ubuntu principles
        message, success = download_image(url)
        print(message)
        
        if success:
            successful_downloads += 1
    
    # Ubuntu-inspired closing message
    print("\n" + "=" * 60)
    if successful_downloads > 0:
        print(f"✓ {successful_downloads} connection(s) strengthened. Community enriched.")
    else:
        print("ℹ No new connections made today, but the community remains.")
    print("=" * 60)

if __name__ == "__main__":
    main()
