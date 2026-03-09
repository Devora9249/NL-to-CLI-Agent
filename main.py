import gradio as gr
import os

import httpx
from groq import Groq
from dotenv import load_dotenv

# netfree
os.environ.pop('SSL_CERT_FILE', None)
unsafe_transport = httpx.HTTPTransport(verify=False)
unsafe_client = httpx.Client(transport=unsafe_transport)

# טעינת משתני סביבה (וודאי שיש לך קובץ .env עם GROQ_API_KEY)
load_dotenv()


# יצירת client של httpx עם ביטול אימות מוחלט
# verify=False כאן אומר לו להתעלם מתעודות SSL (הפתרון לנטפרי)
unsafe_http_client = httpx.Client(verify=False)

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
    http_client=unsafe_http_client  # הזרקה ישירה של הלקוח ה"לא מאובטח"
)


def load_prompt():
    """טוען את הפרומפט מקובץ חיצוני"""
    try:
        with open("prompt.md", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "You are a CLI assistant. Return only the command."

def translate_to_cli(user_input):
    """שולחת את הבקשה ל-Groq ומחזירה את הפקודה"""
    system_message = load_prompt()
    
    try:
        chat_completion = client.chat.completions.create(
            # מודל Llama 3 מהיר מאוד ומתאים למשימות כאלו
            model="llama-3.3-70b-versatile", 
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_input}
            ],
            temperature=0, 
            max_tokens=100,
        )
        
        # ניקוי רווחים מיותרים מהתשובה
        command = chat_completion.choices[0].message.content.strip()
        return command

    except Exception as e:
        import traceback
        traceback.print_exc() 
        return f"שגיאת חיבור מפורטת: {str(e)}"
        

def create_ui():
    with gr.Blocks(title="NL to CLI - Groq Edition") as demo:
        gr.Markdown("# ⚡ NL to CLI Agent (Powered by Groq)")
        gr.Markdown("הזינו הוראה בשפה חופשית וקבלו פקודה לטרמינל.")
        
        with gr.Row():
            with gr.Column():
                input_text = gr.Textbox(
                    label="הוראה למחשב", 
                    placeholder="'project' למשל: ליצור תיקייה חדשה בשם ",
                    lines=3
                )
                submit_btn = gr.Button("המיר לפקודה 🚀", variant="primary")
            
            with gr.Column():
                output_command = gr.Code(label="פקודת CLI מוצעת", language="shell")
        
        submit_btn.click(fn=translate_to_cli, inputs=input_text, outputs=output_command)
        
    return demo

if __name__ == "__main__":
    # וודאי שקובץ הפרומפט קיים לפני ההרצה
    if not os.path.exists("prompt.md"):
        print("Warning: prompt.md not found. Using default prompt.")
        
    app = create_ui()
    app.launch()