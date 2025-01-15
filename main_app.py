import streamlit as st
import plotly.io as pio
import plotly.graph_objects as go
import warnings
warnings.filterwarnings("ignore")


st.set_page_config(page_title="Streamlit App", layout="wide")

custom_template = {
    "layout": {
        "font": {
            "family": "Poppins, sans-serif",
            "size": 28,
            "color": "#E8E8E8",
        },
        "paper_bgcolor": "rgba(30, 30, 47, 1)",
        "plot_bgcolor": "rgba(30, 30, 47, 1)",
        
        "title": {  
            "font": { 
                "size": 32,
                "color": "#32CD32",
            },
            "x": 0.5,
            "xanchor": "center",
        },
        
        "xaxis": {
            "title": {
                "font": { 
                    "size": 26,
                    "color": "#FFFFFF",
                },
            },
            "tickfont": {
                "size": 22,  
                "color": "#FFFFFF",
            },
            "gridcolor": "rgba(255, 255, 255, 0.1)",
            "zerolinecolor": "rgba(255, 255, 255, 0.2)",
            "color": "#FFFFFF",
        },

        "yaxis": {
            "title": {
                "font": { 
                    "size": 26,
                    "color": "#FFFFFF",
                },
            },
            "tickfont": {
                "size": 22,  
                "color": "#FFFFFF",
            },
            "gridcolor": "rgba(255, 255, 255, 0.1)",
            "zerolinecolor": "rgba(255, 255, 255, 0.2)",
            "color": "#FFFFFF",
        },
        
        "legend": {
            "font": {"size": 22, "color": "#E8E8E8"},
            "bgcolor": "rgba(70, 70, 100, 0.4)",
        },
    }
}

pio.templates["custom"] = custom_template
pio.templates.default = "custom"





st.markdown("""
    <style>
        /* General App Styling */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
        html, body, [class*="css"]  {
            font-family: 'Poppins', sans-serif;
            color: #FFFFFF;  /* Light gray text */
            background: linear-gradient(135deg, #1E1E2F, #23233D);
            margin: 0;
            padding: 0;
        }

        /* App Background */
        .stApp {
            background-image: url("https://i.postimg.cc/fLHFdTNy/white-background-7425604-1280.webp");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }

        /* Header Styles */
        h1 , h2, h3, h4, h5, h6 {
            font-family: 'Poppins', sans-serif;
            color: #D4B483;  /* Beige */
            text-shadow: 2px 2px 4px rgba(212, 180, 131, 0.5); /* Subtle glow */
            text-transform: uppercase; /* All caps for a bold look */
            font-weight: 800; /* Medium-bold headers */
            margin-bottom: 15px;
        }

        /* Sidebar */
        [data-testid="stSidebar"] {
            background: linear-gradient(135deg, #D4B483,  #1E1E2F ); /* Beige gradient for sidebar */
            border-right: 3px solid #D4B483; /* Beige border */
            color: #1E1E2F; /* Light gray text for better contrast */
        }
        [data-testid="stSidebar"] h1, h2, h3, h4, h5, h6 {
            color: #D4B483; /* Beige for sidebar headers */
            text-shadow: none; /* No glow for sidebar */
        }

        /* Streamlit Title Bar (Top Bar) */
        header[data-testid="stHeader"] {
            background: linear-gradient(135deg, #1E1E2F, #2A2A3D); /* Match sidebar color */
            border-bottom: 3px solid #D4B483; /* Beige bottom border */
        }
        header[data-testid="stHeader"] .stAppViewContainer > div:first-child {
            color: #D4B483; /* Light gray text for title */
            text-align: center;
            text-shadow: 1px 1px 4px rgba(212, 180, 131, 0.7); /* Beige glow */
        }

        /* Tabs Styling (st.tabs) */
        div[data-testid="stHorizontalBlock"] > div:first-child {
            display: flex;
            justify-content: flex-start;
            gap: 10px; /* Space between tabs */
        }
        div[data-testid="stHorizontalBlock"] > div:first-child > div {
            color: white; /* Default text color for tabs */
            font-family: 'Poppins', sans-serif;
            font-weight: bold;
            padding: 10px 20px;
            border-radius: 8px; /* Rounded corners for tabs */
            background: transparent; /* No background by default */
            cursor: pointer; /* Pointer cursor for clarity */
            transition: all 0.3s ease-in-out;
        }
        div[data-testid="stHorizontalBlock"] > div:first-child > div[aria-selected="true"] {
            color: white; /* White text for active tab */
            background: linear-gradient(135deg, #D4B483, #C9A067); /* Beige background for active tab */
            box-shadow: 0 4px 10px rgba(212, 180, 131, 0.5); /* Glow for active tab */
        }
        div[data-testid="stHorizontalBlock"] > div:first-child > div:hover {
            background: rgba(255, 255, 255, 0.1); /* Light background on hover */
        }

        /* Vertical Tabs Styling (if used) */
        div[data-testid="stVerticalTab"] button {
            color: white; /* White text for all tabs */
            font-weight: bold;
            font-family: 'Poppins', sans-serif;
            border: none; /* Remove default borders */
            background: transparent; /* Transparent background for a clean look */
        }
        div[data-testid="stVerticalTab"] button[data-selected="true"] {
            color: white; /* White text for active tab */
            background: linear-gradient(135deg, #D4B483, #C9A067); /* Highlighted background for active tab */
            border-radius: 8px; /* Rounded corners */
        }
        div[data-testid="stVerticalTab"] button:hover {
            color: #E8E8E8; /* Light gray text on hover */
            cursor: pointer; /* Change cursor to pointer for clarity */
        }

        /* Card-Like Appearance for Widgets */
        [data-testid="stBlock"] {
            background: rgba(255, 255, 255, 0.05); /* Transparent white */
            border-radius: 15px;  /* Rounded corners */
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3); /* Shadow for depth */
            padding: 20px;
            margin-bottom: 20px;
        }

        /* Buttons */
        button {
            background: linear-gradient(135deg, #D4B483, #C9A067); /* Beige */
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 16px;
            box-shadow: 0 4px 10px rgba(212, 180, 131, 0.5);
            cursor: pointer;
            transition: all 0.3s ease-in-out;
        }
        button:hover {
            transform: scale(1.05); /* Slight zoom on hover */
            background: linear-gradient(135deg, #C9A067, #B78F5A); /* Darker beige on hover */
        }

        /* Inputs */
        input, textarea, select {
            background: rgba(255, 255, 255, 0.1);
            color: white;
            border: 1px solid #D4B483; /* Beige */
            border-radius: 8px;
            padding: 10px;
        }
    </style>
    """, unsafe_allow_html=True)






app = st.navigation([
    st.Page("pages/intro.py", title="Introduction"),
    st.Page("pages/financial.py", title="Numbers and Revenue"),
    st.Page("pages/platform.py", title ="Platform, Ratings and Top Games"),
    st.Page("pages/genres.py", title ="Genres, Categories and Playtime"),
    st.Page("pages/conclusion.py", title="Conclusion"),
    st.Page("pages/references.py", title=" References")
])

app.run()
