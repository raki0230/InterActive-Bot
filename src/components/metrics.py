import streamlit as st


def render_metrics(response):

    c1, c2 = st.columns(2)

    with c1:

        st.metric(
            "Confidence",
            response.confidence.upper(),
        )

    with c2:

        st.metric(
            "Sources Needed",
            str(response.sources_needed),
        )