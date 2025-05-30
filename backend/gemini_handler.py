import os
# import google.generativeai as genai
from google import genai


class GeminiHandler:
    def __init__(self):
        """Initialize with Gemini API key."""
        global client
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key not found in environment variables.")
        # genai.configure(api_key=self.api_key)
        client = genai.Client(api_key=self.api_key)

    def get_medical_consultation(self, prompt):
        """Get AI medical consultation based on melanoma probability."""
        try:
            # model = genai.GenerativeModel('gemini-1.0-pro')
            # model = client.models.get(model="gemini-2.0-flash")

            # prompt = prompt
            
            response = client.models.generate_content(
                model='gemini-2.0-flash', 
                contents=prompt
            )

            # ✅ Handle API response correctly
            if response.text:
               formatted_response = response.text.strip()
               formatted_response = formatted_response.replace('\n\n', '</br></br>')
               formatted_response = formatted_response.replace('\n', '</br>')
               return formatted_response
            else:
                return "AI consultation is currently unavailable. Please consult a dermatologist."

        except Exception as e:
            print(f"Gemini API Error: {str(e)}")
            print(genai.ListModels())
            return "AI consultation is currently unavailable. Please consult a dermatologist."
