import openai
import os

# Set this via environment variable or replace below
openai.api_key = os.getenv("OPENAI_API_KEY") or "your-api-key-here"

def ask_gpt_about_code(code_snippet):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You're an expert code reviewer. Judge if the given Python code is likely AI-generated or written by a human, and explain why."},
                {"role": "user", "content": code_snippet}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error during detection: {e}"

def detect_ai_in_cells(code_cell_groups):
    results = []
    for group in code_cell_groups:
        code = "\n".join(group)
        judgment = ask_gpt_about_code(code)
        results.append(judgment)
    return results
