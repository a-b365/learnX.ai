import streamlit as st

st.set_page_config(
    page_title="learnX.ai (study support)",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:

    st.sidebar.success("See the above options")
    st.divider()
    st.write("The project is available at the GitHub Repository [here](https://github.com/fuseai-fellowship/learnX.ai/) .")


st.markdown("<h3 style='text-align: center;'>🌟 <span style='color: #6A5ACD;'>LearnX.ai</span> 🌈</h3>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center;'>An AI-powered study support platform 🤖</h3>", unsafe_allow_html=True)

st.divider()

st.markdown("""
<div style='text-align: center;'>
    <p style='color: #228B22 '> This platform helps create questions in various formats, reducing the time spent on manual processing.</p>
    <p style='color: #008080'>The question formats include multiple types listed on the sidebar.</p>
    <p style='color: #FF6347'>Powered by <strong>Streamlit</strong>, an open-source framework designed specifically for Machine Learning and Data Science applications.</p>
</div>
""", unsafe_allow_html=True)
