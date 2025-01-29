import streamlit as st


st.title("Steam Video Games: A Comprehensive Analysis")
st.title("Introduction")


st.markdown("---")

st.markdown("""
    <style>
        div.custom-text {
            font-size: 28px; /* Size for general text */
        }

        div.custom-text ul {
            font-size: 36px; /* Bullet point size */
            margin-left: 0px; /* Optional: Adjust the left margin for bullet points */
            margin-top: 40px; /* Adds space between the text and the bullet list */
        }

        div.custom-text li {
            font-size: 30px; /* Size for individual bullet points */
            line-height: 2.2; /* Optional: Add spacing between bullet points */
        }
    </style>
    <div class="custom-text">
        This project explores the dynamic world of video games through data collected from Steam, one of the largest digital distribution platforms. By analyzing key features such as the number of games, platforms, genres, and total playtime it uncovers meaningful trends and patterns. This data-driven story aims to answer key questions:
        <ul>
            <li>What number of games are created in different genres and for different platforms?</li>
            <li>What types of games captivate us the most?</li>
            <li>Which genres do we spend the most playtime on?</li>
            <li>Which platforms are preferred by players?</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

