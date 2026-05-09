import streamlit as st


def apply_global_theme():
    """Inject a premium futuristic dark glassmorphism theme."""
    st.set_page_config(layout="wide")

    css = """
    <style>
      :root{
        --bg0:#04070f;
        --bg1:#071428;
        --glass: rgba(10, 20, 40, .55);
        --glass2: rgba(20, 40, 70, .35);
        --stroke: rgba(120, 255, 255, .18);
        --text:#d7f7ff;
        --muted:#8db7c7;
        --cyan:#39e6ff;
        --teal:#00ffc2;
        --green:#35ff7a;
        --amber:#ffd166;
        --red:#ff4d6d;
        --shadow: 0 20px 60px rgba(0,0,0,.55);
      }

      html, body { background: radial-gradient(1200px 700px at 20% 10%, rgba(57,230,255,.15), transparent 60%),
                                   radial-gradient(900px 600px at 70% 20%, rgba(0,255,194,.12), transparent 55%),
                                   linear-gradient(180deg, var(--bg0), var(--bg1)); color: var(--text); }

      .vv-glass{
        background: linear-gradient(135deg, rgba(20,60,120,.25), rgba(10,20,40,.55));
        border: 1px solid rgba(120,255,255,.18);
        border-radius: 18px;
        box-shadow: var(--shadow);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
      }

      .vv-ai-hero{position:relative; overflow:hidden; padding: 34px 22px; border-radius: 24px; border:1px solid rgba(120,255,255,.18); box-shadow: var(--shadow); background: rgba(10,20,40,.35);}
      .vv-ai-hero__bg{position:absolute; inset:-80px; background: conic-gradient(from 200deg, rgba(57,230,255,.22), rgba(0,255,194,.18), rgba(53,255,122,.12), rgba(57,230,255,.22)); filter: blur(24px); animation: spin 10s linear infinite;}
      @keyframes spin{from{transform:rotate(0deg);}to{transform:rotate(360deg);}}
      .vv-ai-hero__content{position:relative; z-index:2; display:flex; flex-direction:column; gap:10px;}
      .vv-badge{display:inline-flex; align-items:center; gap:10px; padding:8px 14px; border-radius: 999px; font-weight:700; letter-spacing:.2px; border:1px solid rgba(57,230,255,.25); background: rgba(0,0,0,.25);}
      .vv-badge--neon{color: var(--cyan); box-shadow: 0 0 18px rgba(57,230,255,.35);}
      .vv-hero-title{font-size: 42px; margin: 0; line-height:1.05; letter-spacing:-.6px;}
      .vv-hero-subtitle{max-width: 920px; color: var(--muted); font-size: 16px; margin-top:0;}
      .vv-hero-actions{display:flex; align-items:center; gap:16px; margin-top: 6px;}
      .vv-cta{display:inline-flex; align-items:center; justify-content:center; padding: 12px 18px; border-radius: 12px; border:1px solid rgba(0,255,194,.35); background: linear-gradient(135deg, rgba(0,255,194,.18), rgba(57,230,255,.12)); color: var(--text); text-decoration:none; font-weight:800; box-shadow: 0 0 22px rgba(0,255,194,.18); transition: transform .2s ease, box-shadow .2s ease;}
      .vv-cta:hover{transform: translateY(-2px); box-shadow: 0 0 30px rgba(0,255,194,.28);}
      .vv-hero-glow-dot{width: 12px; height: 12px; border-radius: 50%; background: var(--teal); box-shadow: 0 0 26px rgba(0,255,194,.6); animation: pulse 1.8s ease-in-out infinite;}
      @keyframes pulse{0%,100%{transform:scale(1); opacity:.7;}50%{transform:scale(1.7); opacity:1;}}

      .vv-section-spacer{height: 18px;}
      .vv-footer{display:flex; justify-content:space-between; gap:12px; align-items:center; padding: 14px 16px; border-radius: 16px; border:1px solid rgba(120,255,255,.18); background: rgba(10,20,40,.30);}
      .vv-footer__brand{font-weight:900; letter-spacing:.3px;}
      .vv-footer__meta{color: var(--muted); font-size: 13px;}
      .vv-footer-spacer{height: 28px;}

      .vv-marquee{display:flex; gap: 14px; white-space: nowrap; overflow:hidden; animation: marquee 28s linear infinite;}
      .vv-marquee__item{display:inline-flex; padding: 10px 14px; border-radius: 999px; border:1px solid rgba(120,255,255,.18); background: rgba(0,0,0,.18); font-weight:700;}
      .vv-marquee__item--warn{color: var(--amber); box-shadow: 0 0 14px rgba(255,209,102,.16);}
      .vv-marquee__item--risk{color: var(--teal); box-shadow: 0 0 14px rgba(0,255,194,.14);}
      .vv-marquee__item--bad{color: var(--red); box-shadow: 0 0 14px rgba(255,77,109,.14);}
      @keyframes marquee{from{transform: translateX(0);}to{transform: translateX(-35%);}}

      .vv-feature-card{padding: 14px 14px; border-radius: 16px; border:1px solid rgba(120,255,255,.18); background: rgba(0,0,0,.18); transition: transform .2s ease;}
      .vv-feature-card:hover{transform: translateY(-2px);}
      .vv-feature-card__title{color: var(--muted); font-size: 13px; font-weight:700;}
      .vv-feature-card__value{font-size: 22px; font-weight:950; margin-top:6px; color: var(--cyan);}
      .vv-feature-card__desc{color: var(--muted); font-size: 13px; margin-top:4px;}

      .vv-health-summary{display:flex; justify-content:space-between; gap: 14px; align-items:center;}
      .vv-health-summary__kicker{color: var(--muted); font-weight:800; letter-spacing:.3px;}
      .vv-health-summary__headline{font-size: 28px; font-weight:1000; margin-top: 6px;}
      .vv-health-summary__text{color: var(--muted); max-width: 640px; margin-top: 8px;}
      .vv-health-pills{display:flex; gap: 10px; flex-wrap:wrap; justify-content:flex-end;}
      .vv-pill{padding:10px 12px; border-radius: 999px; font-weight:900; border:1px solid rgba(120,255,255,.18); background: rgba(0,0,0,.18);}
      .vv-pill--ok{color: var(--green); box-shadow: 0 0 20px rgba(53,255,122,.16);}
      .vv-pill--risk{color: var(--teal); box-shadow: 0 0 20px rgba(0,255,194,.14);}
      .vv-pill--caution{color: var(--amber); box-shadow: 0 0 20px rgba(255,209,102,.14);}
      .vv-health-score{margin-top: 12px; text-align:right; color: var(--muted); font-weight:800;}
      .vv-health-score span{color: var(--cyan); font-size: 26px; font-weight:1100;}

      /* Streamlit container tuning */
      .stApp [data-testid="stVerticalBlock"]{gap: 14px;}
    </style>
    """

    st.markdown(css, unsafe_allow_html=True)

