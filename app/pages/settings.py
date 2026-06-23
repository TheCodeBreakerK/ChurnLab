import streamlit as st
from utils.i18n import _, set_language, SUPPORTED_LANGUAGES


def render_settings() -> None:
	"""Settings page: language selector and app preferences."""
	st.title(_('Settings'))
	st.caption(_('Configure your ChurnLab preferences.'))
	st.divider()

	st.subheader(_('Language'))

	current = st.session_state.get('language', 'en_US')
	codes = list(SUPPORTED_LANGUAGES.keys())
	labels = list(SUPPORTED_LANGUAGES.values())

	selected_label = st.radio(
		_('Select language'),
		options=labels,
		index=codes.index(current),
		horizontal=True,
		key='language_selector',
	)
	selected_code = codes[labels.index(selected_label)]

	if selected_code != current:
		set_language(selected_code)
		st.success(_('Language updated. Refreshing…'))
		st.rerun()
