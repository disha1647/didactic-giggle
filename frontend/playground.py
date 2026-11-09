import streamlit as st

from core.request_manager import RequestManager
from providers.litellm_provider import LiteLLMProvider


def show_playground():

    st.title("CachePilot AI Playground")

    st.caption(
        "Test LLM requests and monitor token usage and response latency."
    )

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "metrics" not in st.session_state:
        st.session_state.metrics = []

    # Display previous conversation
    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    prompt = st.chat_input("Ask CachePilot something...")

    if prompt:

        try:
            clean_prompt = RequestManager.validate_prompt(prompt)

            # Display user message
            st.session_state.messages.append({
                "role": "user",
                "content": clean_prompt
            })

            with st.chat_message("user"):
                st.markdown(clean_prompt)

            # Generate LLM response
            with st.chat_message("assistant"):

                with st.spinner("Generating response..."):

                    provider = LiteLLMProvider()
                    result = provider.generate_response(clean_prompt)

                st.markdown(result["response"])

                # Display request metrics
                st.divider()

                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "Input Tokens",
                    result["input_tokens"]
                )

                col2.metric(
                    "Output Tokens",
                    result["output_tokens"]
                )

                col3.metric(
                    "Latency",
                    f'{result["latency"]} sec'
                )

            # Save assistant response
            st.session_state.messages.append({
                "role": "assistant",
                "content": result["response"]
            })

            # Save metrics for dashboard development
            st.session_state.metrics.append({
                "model": result["model"],
                "input_tokens": result["input_tokens"],
                "output_tokens": result["output_tokens"],
                "total_tokens": result["total_tokens"],
                "latency": result["latency"]
            })

        except Exception as error:
            st.error(str(error))

    # Sidebar metrics
    st.sidebar.subheader("Session Statistics")

    total_requests = len(st.session_state.metrics)

    total_tokens = sum(
        item["total_tokens"]
        for item in st.session_state.metrics
    )

    average_latency = (
        sum(item["latency"] for item in st.session_state.metrics)
        / total_requests
        if total_requests else 0
    )

    st.sidebar.metric("Total Requests", total_requests)
    st.sidebar.metric("Total Tokens", total_tokens)
    st.sidebar.metric(
        "Average Latency",
        f"{average_latency:.3f} sec"
    )

    if st.sidebar.button("Clear Conversation"):
        st.session_state.messages = []
        st.session_state.metrics = []
        st.rerun()