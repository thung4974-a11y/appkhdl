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

[data-testid="stSidebar"] > div:first-child {
    padding: 10px;
    border-radius: 20px;
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
    font-weight: 500 !important;
    font-family: "Segoe UI", sans-serif;
}

div[role="radiogroup"] > label {
    background: rgba(255, 255, 255, 0.06);
    padding: 10px 14px;
    border-radius: 12px;
    margin-bottom: 6px;
    transition: 0.25s ease;
    border: 1px solid rgba(255,255,255,0.08);
}

div[role="radiogroup"] > label:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: translateX(4px);
}

div[role="radiogroup"] > label[data-testid="stRadioOption"]:has(input:checked) {
    background: rgba(0, 168, 255, 0.25) !important;
    border: 1px solid rgba(0,168,255,0.6) !important;
    box-shadow: 0 0 10px rgba(0,168,255,0.6);
    transform: translateX(6px);
}

button[kind="primary"] {
    background: linear-gradient(135deg, #0abde3, #0984e3) !important;
    padding: 10px 20px !important;
    border-radius: 12px !important;
    border: none !important;
    transition: 0.25s ease;
}

button[kind="primary"]:hover {
    transform: scale(1.04);
    box-shadow: 0 4px 20px rgba(0,150,255,0.45);
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
h1, h2 {
    text-align: center !important;
}
input[type="text"], input[type="password"] {
    background-color: white !important;
    color: black !important;
    border-radius: 8px;
    border: 1px solid #cccccc !important;
}
button[kind="primary"] {
    background-color: white !important;
    color: black !important;
    border-radius: 8px !important;
    border: none !important;
    font-weight: bold !important;
}
button[kind="primary"]:hover {
    background-color: #e6e6e6 !important;
    color: black !important;
}
</style>
"""
