import streamlit as st

import components as cmp

import utils as utl

st.set_page_config(
	page_title='ChurnLab',
	layout='wide',
)

utl.init_i18n()

cmp.render_navbar()
