# config/styles.py

PREMIUM_SIDEBAR = """
<style>
[data-testid="stSidebar"] {
    background: rgba(15, 32, 65, 0.65) !important;
    backdrop-filter: blur(18px) !important;
    -webkit-backdrop-filter: blur(18px) !important;
    border-right: 1px solid rgba(255,255,255,0.12);
    box-shadow: 4px 0 25px rgba(0,0,0,0.55);
    padding-top: 20px !important;
}
</style>
"""

LOGIN_PAGE_BG = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://sf-static.upanhlaylink.com/img/image_2025120700f9fd552eecbc6c73df72a9cb906ab6.jpg");
    background-size: cover;
    background-repeat: no-repeat;
    background-position: center;
}
[data-testid="stHeader"], [data-testid="stFooter"] {
    background: rgba(0,0,0,0);
}
</style>
"""

LOGIN_FORM_CSS = """
<style>

/* Center title */
h1, h2 {
    text-align: center !important;
}

/* Input fields */
div[data-testid="stTextInput"] input,
div[data-testid="stPassword"] input {
    background-color: white !important;
    color: black !important;
    border-radius: 8px !important;
    border: 1px solid #cccccc !important;
}

/* Buttons */
div[data-testid="stButton"] > button {
    background-color: white !important;
    color: black !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: bold !important;
    transition: all 0.25s ease-in-out;
}

/* Hover effect */
div[data-testid="stButton"] > button:hover {
    background-color: #e6e6e6 !important;
    transform: translateY(-2px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.25);
}

</style>
"""


