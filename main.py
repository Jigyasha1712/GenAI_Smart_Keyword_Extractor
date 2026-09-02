import google.generativeai as genai

# ----------------- CONFIG -----------------
API_KEY = "YOUR_GEMINI_API_KEY"  # 👉 Add your key here
genai.configure(api_key=API_KEY)

# ----------------- GEMINI MODEL -----------------
model = genai.GenerativeModel("gemini-1.5-flash")

# ----------------- FUNCTION: Extract Keywords -----------------
def extract_keywords(text):
    prompt = f"""
    Extract 10 important keywords from the text below.
    Only return keywords (one per line), no numbering.

    Text:
    {text}
    """

    response = model.generate_content(prompt)

    keywords = response.text.strip().split("\n")
    keywords = [k.strip().replace("-", "") for k in keywords if k.strip()]
    return keywords


# ----------------- FUNCTION: Create Social Media Links -----------------
def generate_social_media_links(keyword):
    query = keyword.replace(" ", "+")  # URL safe

    return {
        "keyword": keyword,
        "google_search": f"https://www.google.com/search?q={query}",
        "youtube_search": f"https://www.youtube.com/results?search_query={query}",
        "instagram_hashtag": f"https://www.instagram.com/explore/tags/{keyword.replace(' ', '')}/",
        "twitter_search": f"https://x.com/search?q={query}"
    }


# ----------------- MAIN PROGRAM -----------------
if __name__ == "__main__":
    text = input("Enter text to extract keywords: ")

    print("\n🔍 Extracting keywords using Gemini...\n")
    keywords = extract_keywords(text)

    print("✅ Keywords Found:")
    for k in keywords:
        print("-", k)

    print("\n🔗 Social Media Links:\n")
    for kw in keywords:
        links = generate_social_media_links(kw)
        print(f"🔹 {kw}")
        print("  Google:", links["google_search"])
        print("  YouTube:", links["youtube_search"])
        print("  Instagram:", links["instagram_hashtag"])
        print("  Twitter:", links["twitter_search"])
        print()
