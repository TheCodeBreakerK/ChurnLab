import streamlit as st

from services.constants import MODEL_PATHS
from utils.i18n import _


def render_model_selector(key: str = 'model') -> str | None:
	"""Render a model selectbox. Returns the selected model name or ``None`` if unavailable."""
	name = st.selectbox(
		_('Model'),
		options=list(MODEL_PATHS.keys()),
		key=key,
		help=_('Choose the ML model to use for prediction.'),
	)
	path = MODEL_PATHS[name]
	if not path.exists():
		st.warning(f'Model file not found: `{path}`')
		return None

	return name
