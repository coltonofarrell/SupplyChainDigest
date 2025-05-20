import requests
import os
from datetime import datetime
from config import NEWS_API_KEY
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_article(text):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You summarize supply chain news articles briefly and clearly."},
                {"role": "user", "content": f"Summarize this in 1-2 sentences:\n\n{text}"}
            ],
            temperature=0.7
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"❌ GPT error: {e}")
        return "_Summary unavailable._"

def get_supply_chain_news():
    if not NEWS_API_KEY:
        print("❌ Missing NewsAPI key.")
        return

    url = "https://newsapi.org/v2/everything"
    query = "supply chain OR global trade OR logistics OR shipping OR ports OR freight"
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "apiKey": NEWS_API_KEY
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"❌ API Error: {response.status_code} - {response.text}")
        return

    articles = response.json().get("articles", [])
    if not articles:
        print("⚠️ No articles found.")
        return

    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"supply_chain_digest_{today}.md"

    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"# 📰 Supply Chain Digest – {today}\n\n")

        for article in articles:
            title = article["title"]
            url = article["url"]
            content = article.get("description") or article.get("content") or ""

            print(f"📌 {title}")
            print(f"🔗 {url}\n")

            summary = summarize_article(content)

            file.write(f"## 📌 {title}\n")
            file.write(f"[Read more]({url})\n\n")
            file.write(f"**🧠 Summary:** {summary}\n\n")

    print(f"✅ Saved digest to `{filename}`.")

if __name__ == "__main__":
    get_supply_chain_news()