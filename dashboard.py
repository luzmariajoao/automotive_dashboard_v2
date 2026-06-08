import streamlit as st
from anthropic import Anthropic

st.set_page_config(page_title="EU Automotive", layout="wide")

st.title("🚗 EU Automotive Market Intelligence")

st.write("✅ App is running!")

# Simple chat
st.subheader("Chat")
query = st.text_input("Ask something:")

if query:
    try:
        api_key = st.secrets.get("ANTHROPIC_API_KEY")
        if api_key:
            client = Anthropic(api_key=api_key)
            response = client.messages.create(
                model="claude-opus-4-1-20250805",
                max_tokens=200,
                messages=[{"role": "user", "content": query}]
            )
            st.success(response.content[0].text)
        else:
            st.warning("API key not configured")
    except Exception as e:
        st.error(f"Error: {str(e)}")

st.write("---")
st.write("Ready to go! 🚀")
