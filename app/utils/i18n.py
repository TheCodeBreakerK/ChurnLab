import os
from gettext import translation, NullTranslations
import streamlit as st


SUPPORTED_LANGUAGES: dict[str, str] = {
	'en_US': 'English',
	'pt_BR': 'Português',
}

_DEFAULT_LANGUAGE = 'en_US'

_LOCALE_DIR = os.path.join(
	os.path.dirname(os.path.abspath(__file__)), '..', 'locales'
)


def _build_translator(lang: str) -> NullTranslations:
	return translation(
		domain='messages',
		localedir=_LOCALE_DIR,
		languages=[lang],
		fallback=True,
	)


def init_i18n() -> None:
	"""Detect browser locale and initialise translator in session state."""
	if 'language' not in st.session_state:
		locale = st.context.locale or ''
		st.session_state.language = (
			'pt_BR' if locale.lower().startswith('pt') else _DEFAULT_LANGUAGE
		)

	st.session_state._translator = _build_translator(st.session_state.language)


def set_language(lang: str) -> None:
	"""Switch the active language and rebuild the translator."""
	if lang in SUPPORTED_LANGUAGES:
		st.session_state.language = lang
		st.session_state._translator = _build_translator(lang)


def _(text: str) -> str:
	"""Translate *text* using the current session translator."""
	translator: NullTranslations | None = st.session_state.get('_translator')
	if translator is None:
		return text

	return translator.gettext(text)
