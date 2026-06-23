import pandas as pd
import streamlit as st


REPORT_PATH = 'reports/model_comparison.csv'

HIGHER_IS_BETTER = [
	'ROC AUC',
	'PR AUC',
	'Accuracy',
	'Precision',
	'Recall',
	'F1 Score',
]
LOWER_IS_BETTER = ['Predict Time']


@st.cache_data
def load_report() -> pd.DataFrame:
	"""Load and normalise the CSV benchmark report."""
	df = pd.read_csv(REPORT_PATH)
	df.columns = (
		df.columns.str.replace('F1-Score', 'F1 Score')
		.str.replace('Predict Time (ms)', 'Predict Time')
		.str.strip()
	)

	return df


def get_ranking(df: pd.DataFrame, metric: str) -> pd.DataFrame:
	"""Sort the report by *metric* (lower-is-better aware)."""
	ascending = metric in LOWER_IS_BETTER

	return df.sort_values(metric, ascending=ascending).reset_index(drop=True)


def get_best_model(
	df: pd.DataFrame, metric: str = 'ROC AUC'
) -> tuple[str, float]:
	"""Return (model_name, best_score) for the given metric (lower-is-better aware)."""
	idx = (
		df[metric].idxmin()
		if metric in LOWER_IS_BETTER
		else df[metric].idxmax()
	)

	return str(df.iloc[idx, 0]), df.iloc[idx][metric]


def highlight_best(df: pd.DataFrame) -> pd.DataFrame.style:
	"""Return a styled DataFrame highlighting best scores per column."""
	styled = df.style
	for col in df.select_dtypes('number').columns:
		if col in LOWER_IS_BETTER:
			styled = styled.highlight_min(subset=[col], color='#8B5CF633')

		if col not in LOWER_IS_BETTER:
			styled = styled.highlight_max(subset=[col], color='#8B5CF633')

	styled = styled.format(
		{c: '{:.4f}' for c in df.select_dtypes('number').columns}
	)

	return styled
