from google import genai

client = genai.Client(api_key="AIzaSyDr8yRI2lSFhgQ_WsoUVjFM_jP4XcfFmYU")

for m in client.models.list():
    print(m.name)