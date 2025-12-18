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
/* ... copy toàn bộ CSS từ file gốc ... */
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
h1, h2 { text-align: center !important; }
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
