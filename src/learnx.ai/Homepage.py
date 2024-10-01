import streamlit as st

st.set_page_config(
    page_title="learnX.ai (study support)",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("<h3 style='text-align: center;'>🌟 <span style='color: #9932CC;'>LearnX.ai</span> 🌈</h3>", unsafe_allow_html=True)

st.sidebar.success("Navigate using the options above")
with st.sidebar:
    st.write("The project is available at the GitHub Repository [here](https://github.com/a-b365/learnx.ai)")

st.markdown("<h3 style='text-align: center;'>An AI-powered study support platform 🤖</h3>", unsafe_allow_html=True)

st.divider()

st.markdown("""
<div style='text-align: center;'>
    <p style='color: gray;'> This platform helps create questions in various formats, reducing the time spent on manual processing.</p>
    <p style='color: green;'>The question formats include multiple types listed on the sidebar.</p>
    <p style='color: orange;'>Powered by <strong>Streamlit</strong>, an open-source framework designed specifically for Machine Learning and Data Science applications.</p>
</div>
""", unsafe_allow_html=True)
