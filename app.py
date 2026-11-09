import streamlit as st

from config.settings import settings
from frontend.playground import show_playground


st.set_page_config(
    page_title=settings.APP_NAME,
    page_icon="⚡",
    layout="wide"
)


def main():

    st.sidebar.title("⚡ CachePilot")

    st.sidebar.caption(
        "Intelligent LLM Cost Optimization Platform"
    )

    show_playground()


if __name__ == "__main__":
    main()