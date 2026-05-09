import streamlit as st


def glass_container(title: str):
    """Context manager-like helper for glass panels."""
    return _GlassContainer(title)


class _GlassContainer:
    def __init__(self, title: str):
        self.title = title

    def __enter__(self):
        st.markdown(
            f"""
            <div class='vv-glass' style='padding:16px 16px;'>
              <div style='display:flex; justify-content:space-between; align-items:center; gap:12px;'>
                <div style='font-weight:1000; letter-spacing:.2px;'>{self.title}</div>
              </div>
            """,
            unsafe_allow_html=True,
        )
        return self

    def __exit__(self, exc_type, exc, tb):
        st.markdown("</div>", unsafe_allow_html=True)


def neon_title(text: str):
    st.markdown(
        f"""
        <div style='font-size:26px; font-weight:1100; color:#39e6ff; text-shadow: 0 0 18px rgba(57,230,255,.35);'>
          {text}
        </div>
        """,
        unsafe_allow_html=True,
    )


def animated_metric(title: str, value: str, delta: float):
    sign = "+" if delta >= 0 else ""
    st.markdown(
        f"""
        <div class='vv-glass' style='padding:14px; height: 120px;'>
          <div style='color:#8db7c7; font-weight:900; font-size:13px;'>{title}</div>
          <div style='margin-top:10px; font-size:28px; font-weight:1100; color:#39e6ff;'>{value}</div>
          <div style='margin-top:6px; color:#8db7c7; font-weight:900;'>
            <span style='color:#00ffc2;'>{sign}{delta:.1f}%</span> vs last window
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

