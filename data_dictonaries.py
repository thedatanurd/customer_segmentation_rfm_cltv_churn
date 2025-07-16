import json
import streamlit as st

def load_data_dictionary(json_path):
    with open(json_path, "r") as f:
        return json.load(f)

def render_data_dictionary_app(json_path):

    metrics = load_data_dictionary(json_path)

    # Detect whether to use "Metric Name" or "Segment Name"
    label_key = "Metric Name" if "Metric Name" in metrics[0] else "Segment Name"

    names = [m[label_key] for m in metrics]
    selected = st.selectbox(f"Data Dictionary: Select a {label_key} to view", names)

    selected_data = next(m for m in metrics if m[label_key] == selected)

    st.markdown(f"<h6 style='text-align: center;'>{label_key} Details:</h6>", unsafe_allow_html=True)
    for key, value in selected_data.items():
        st.markdown(
            f"""
            <div style="display: flex; gap: 10px; align-items: baseline; margin-bottom: 0.5rem;">
                <span style="font-size: 16px; font-weight: 600; min-width: 200px;">{key}:</span>
                <span style="font-size: 14px;">{value}</span>
            </div>
            """,
            unsafe_allow_html=True
        )
