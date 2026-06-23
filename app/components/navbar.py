import streamlit as st

import pages as pg
from utils.i18n import _


def __get_navigation_pages() -> list[st.Page]:
	"""Build the list of Streamlit Page objects for the top navigation bar."""
	return [
		st.Page(
			pg.render_overview,
			title=_('Overview'),
			icon=':material/dashboard:',
			default=True,
		),
		st.Page(
			pg.render_prediction,
			title=_('Prediction'),
			icon=':material/psychology:',
		),
		st.Page(
			pg.render_benchmark,
			title=_('Benchmark'),
			icon=':material/bar_chart:',
		),
		st.Page(
			pg.render_settings,
			title=_('Settings'),
			icon=':material/settings:',
		),
		st.Page(
			pg.render_about,
			title=_('About'),
			icon=':material/info:',
		),
	]


def render_navbar() -> None:
	"""Render the top navigation bar and execute the selected page."""
	pages: list[st.Page] = __get_navigation_pages()
	nav = st.navigation(pages, position='top')
	nav.run()
