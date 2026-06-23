from pathlib import Path

import joblib
import streamlit as st


@st.cache_resource
def load_model(path: Path):
	"""Load a trained model from a `.joblib` file."""
	return joblib.load(path)


@st.cache_resource
def load_artifacts(path: Path):
	"""Load model artifacts (encoders, feature names, etc.) from a `.joblib` file."""
	return joblib.load(path)
