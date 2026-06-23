from pathlib import Path
import streamlit as st

import components as cmp

import utils as utl

ICON = Path(__file__).parent / 'assets' / 'churnlab-favicon.jpeg'

st.set_page_config(
	page_title='ChurnLab',
    page_icon=str(ICON),
	layout='wide',
)

utl.init_i18n()

cmp.render_navbar()
