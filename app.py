from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components


ROOT = Path(__file__).resolve().parent
html = (ROOT / "index.html").read_text(encoding="utf-8")

runtime_parent = "const parent = window.top;"
if html.count(runtime_parent) != 1:
    raise RuntimeError("Could not find GUST's proxy frame runtime")

html = html.replace(
    "<head>",
    "<head><script>window.__gustStreamlitRoot = window;</script>",
    1,
)
html = html.replace(
    runtime_parent,
    """const parent = (() => {
    let frame = window;
    try {
        while (frame !== frame.parent) {
            if (frame.__gustStreamlitRoot === frame) return frame;
            frame = frame.parent;
        }
    } catch (_) {}
    return window.top;
})();""",
    1,
)

resize_script = """
<script>
(() => {
    const fit = () => {
        try {
            if (window.frameElement) {
                window.frameElement.style.height = `${window.top.innerHeight}px`;
            }
        } catch (_) {}
    };
    fit();
    try {
        window.top.addEventListener("resize", fit);
    } catch (_) {}
})();
</script>
"""
html, closing_body, _ = html.rpartition("</body>")
if not closing_body:
    raise RuntimeError("Could not find the end of index.html")
html += resize_script + closing_body + "</body>"

st.set_page_config(page_title="GUST Browser", layout="wide")
st.markdown(
    """
    <style>
    [data-testid="stHeader"], [data-testid="stToolbar"], footer { display: none; }
    [data-testid="stAppViewContainer"] .main .block-container {
        max-width: 100%;
        padding: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)
components.html(html, height=900, scrolling=False)