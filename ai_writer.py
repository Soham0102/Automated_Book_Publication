
import os

use_openai = False
try:
    from openai import OpenAI
    from dotenv import load_dotenv
    load_dotenv()  
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    use_openai = True
    print("Using OpenAI GPT-4o.")
except Exception as e:
    print(f"OpenAI not available ({e}). Falling back to HuggingFace.")

def rewrite_with_openai(text):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are an expert book editor who rewrites content clearly and concisely."},
                {"role": "user", "content": f"Rewrite the following text:\n\n{text}"}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI failed: {e}")
        return None

def rewrite_with_huggingface(text):
    from transformers import pipeline
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    results = []
    for c in chunks:
        try:
            summary = summarizer(c, max_length=120, min_length=40, do_sample=False)
            results.append(summary[0]['summary_text'])
        except Exception as e:
            print(f"HuggingFace failed on chunk: {e}")
            results.append(c)
    return "\n\n".join(results)

def rewrite_text(text):
    if use_openai:
        rewritten = rewrite_with_openai(text)
        if rewritten:
            return rewritten
    return rewrite_with_huggingface(text)

if __name__ == "__main__":
    with open("data/content.txt", "r", encoding="utf-8") as f:
        content = f.read()
    rewritten = rewrite_text(content)
    with open("data/rewritten.txt", "w", encoding="utf-8") as f:
        f.write(rewritten)
    print("Rewritten content saved in data/rewritten.txt")
