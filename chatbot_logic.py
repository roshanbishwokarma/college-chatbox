from google import genai
import sqlite3
client = genai.Client(api_key="AIzaSyDr8yRI2lSFhgQ_WsoUVjFM_jP4XcfFmYU")


# ================= COLLEGE CALENDAR EVENTS =================
# Add this import at the top of chatbot_logic.py
from datetime import datetime


# Replace your existing get_college_event_response() function with this one.
# Replace your current get_college_event_response() function with this improved version.

def get_college_event_response(user_input):
    user_input = user_input.lower()

    event_dates = {
        "semester start": ("2026-02-23", "The 4th semester starts on 23 February 2026."),
        "commencement": ("2026-02-23", "The 4th semester commences on 23 February 2026."),
        "mega health camp": ("2026-02-27", "The Mega Health Camp (Blood Donation Camp) is on 27 February 2026."),
        "blood donation camp": ("2026-02-27", "The Mega Health Camp (Blood Donation Camp) is on 27 February 2026."),
        "kalatarranga": ("2026-03-06", "KalataRRanga 2K26 will be held on 6 and 7 March 2026."),
        "women's day": ("2026-03-09", "International Women's Day celebration is on 9 March 2026."),
        "workshop": ("2026-03-11", "The two-day workshop is scheduled for 11 and 12 March 2026."),
        "sdp": ("2026-03-26", "The Skill Development Program (SDP) is on 26 March 2026."),
        "industrial visit": ("2026-04-11", "The Industrial Visit is scheduled on 11 April 2026."),
        "ia1": ("2026-04-23", "The 1st Internal Assessment (IA-1) will be conducted from 23 to 25 April 2026."),
        "internal assessment 1": ("2026-04-23", "The 1st Internal Assessment (IA-1) will be conducted from 23 to 25 April 2026."),
        "first internal": ("2026-04-23", "The 1st Internal Assessment (IA-1) will be conducted from 23 to 25 April 2026."),
        "graduation day": ("2026-04-30", "Graduation Day is on 30 April 2026."),
        "guest lecture": ("2026-05-07", "Guest Lectures are scheduled on 7 and 8 May 2026."),
        "technical seminar": ("2026-05-22", "The Technical Seminar is scheduled for 22 May 2026."),
        "ia2": ("2026-06-08", "The 2nd Internal Assessment (IA-2) will be conducted from 8 to 10 June 2026."),
        "internal assessment 2": ("2026-06-08", "The 2nd Internal Assessment (IA-2) will be conducted from 8 to 10 June 2026."),
        "second internal": ("2026-06-08", "The 2nd Internal Assessment (IA-2) will be conducted from 8 to 10 June 2026."),
        "last working day": ("2026-06-15", "The last working day of the semester is 15 June 2026."),
    }

    today = datetime.today().date()

    for keyword, (date_str, response_text) in event_dates.items():
        if keyword in user_input:
            event_date = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Event already completed
            if event_date < today:
                past_response = response_text

                # Convert future tense to past tense
                past_response = past_response.replace("will be conducted", "was conducted")
                past_response = past_response.replace("will be held", "was held")
                past_response = past_response.replace("is scheduled for", "was held on")
                past_response = past_response.replace("is scheduled on", "was conducted on")
                past_response = past_response.replace("is on", "was held on")
                past_response = past_response.replace("starts on", "started on")
                past_response = past_response.replace("commences on", "commenced on")
                past_response = past_response.replace("are scheduled on", "were conducted on")

                return past_response + " It has already been completed."

            # Event is today
            elif event_date == today:
                return response_text + " It is happening today."

            # Upcoming event
            else:
                return response_text

    return None


# ================= DB RESPONSE =================
def get_db_response(user_input):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    cursor.execute("SELECT keyword, response FROM responses")
    data = cursor.fetchall()

    conn.close()

    user_input = user_input.lower()

    for keyword, response in data:
        if keyword.lower() in user_input:
            return response

    return None


# ================= SAVE CHAT =================
def save_chat(user_message, bot_response):
    conn = sqlite3.connect("chatbot.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO chat_history (user_message, bot_response)
        VALUES (?, ?)
    """, (user_message, bot_response))

    conn.commit()
    conn.close()


# ================= AI RESPONSE =================
# Replace only the get_ai_response() function with this version.

# Replace only your get_ai_response() function with this version.

def get_ai_response(user_input):
    try:
        prompt = f"""
Answer the following question in a short and simple way.
Use plain text only.
Do not use markdown symbols like *, #, -, or bullet points.
Keep the answer under 4 sentences.

Question: {user_input}
"""

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        return response.text.strip()

    except Exception as e:
        print("AI Error:", e)
        return "Sorry, I'm having trouble right now."

# ================= MAIN FUNCTION =================
def get_response(user_input):
    user_input = user_input.strip()

    # Greeting responses
    if user_input.lower() in ["hi", "hello", "hey"]:
        response = "Hello! How can I help you?"
        save_chat(user_input, response)
        return response

    # 1. Check college calendar events first
    college_response = get_college_event_response(user_input)
    if college_response:
        save_chat(user_input, college_response)
        return college_response

    # 2. Check database responses
    db_response = get_db_response(user_input)
    if db_response:
        save_chat(user_input, db_response)
        return db_response

    # 3. Use AI response
    ai_response = get_ai_response(user_input)
    save_chat(user_input, ai_response)
    return ai_response