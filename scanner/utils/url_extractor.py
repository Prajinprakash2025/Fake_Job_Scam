import requests
from bs4 import BeautifulSoup

def extract_text_from_url(url, timeout=10):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # remove unwanted tags
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()

        text = soup.get_text(separator=" ")
        text = " ".join(text.split())

        if len(text) < 100:
            return None  # too little text → useless

        return text[:15000]

    except Exception as e:
        print("URL extraction error:", e)
        return None
