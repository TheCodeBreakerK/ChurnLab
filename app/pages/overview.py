import pandas as pd
import plotly.express as px
import streamlit as st

from components.kpi_card import render_kpi_card
from utils.i18n import _
from utils.plotly_config import apply_dark_layout, hide_xaxis_grid


@st.cache_data
def _load_data() -> pd.DataFrame:
	"""Load the clean Telco Churn parquet dataset."""
	return pd.read_parquet('data/processed/telco_churn_clean.parquet')


def render_overview() -> None:
	"""Dashboard overview page: dataset stats, churn distribution, and scatter plots."""
	st.title(_('ChurnLab — Customer Churn Prediction System'))
	st.caption(
		_(
			'Explore dataset statistics, understand churn patterns, '
			'and review model performance.'
		)
	)
	st.divider()

	try:
		df = _load_data()
	except Exception as e:
		st.error(f'Could not load dataset: {e}')
		return

	churn_col = 'Churn' if 'Churn' in df.columns else df.columns[-1]
	total = len(df)
	churned = (
		int(df[churn_col].sum())
		if df[churn_col].dtype in ['int64', 'float64']
		else int((df[churn_col] == 'Yes').sum())
	)
	churn_rate = churned / total * 100
	avg_tenure = df['Tenure'].mean() if 'Tenure' in df.columns else 0
	avg_monthly = (
		df['MonthlyCharges'].mean() if 'MonthlyCharges' in df.columns else 0
	)

	k1, k2, k3, k4 = st.columns(4)
	render_kpi_card(k1, _('Total Customers'), f'{total:,}')
	render_kpi_card(
		k2,
		_('Churned'),
		f'{churned:,}',
		delta=f'{churn_rate:.1f}%',
		delta_color='inverse',
	)
	render_kpi_card(k3, _('Avg. Tenure (mo)'), f'{avg_tenure:.1f}')
	render_kpi_card(k4, _('Avg. Monthly ($)'), f'{avg_monthly:.2f}')

	st.divider()

	col_left, col_right = st.columns(2)

	with col_left:
		st.subheader(_('Churn Distribution'))
		counts = df[churn_col].value_counts().reset_index()
		counts.columns = ['Status', 'Count']
		fig = px.bar(
			counts,
			x='Status',
			y='Count',
			color='Status',
			color_discrete_sequence=['#dd4d88', '#464c89'],
			text='Count',
			labels={'Status': _('Status'), 'Count': _('Count')},
		)
		fig.update_traces(textposition='outside')
		fig = apply_dark_layout(fig, showlegend=False)
		fig = hide_xaxis_grid(fig)
		st.plotly_chart(fig, width='stretch')

	with col_right:
		st.subheader(_('Churn by Contract Type'))
		if 'Contract' in df.columns:
			ct = (
				df.groupby('Contract')[churn_col]
				.apply(
					lambda x: (
						(x.sum() / len(x) * 100)
						if x.dtype in ['int64', 'float64']
						else ((x == 'Yes').sum() / len(x) * 100)
					)
				)
				.reset_index()
			)
			ct.columns = ['Contract', 'ChurnRate']
			fig2 = px.bar(
				ct,
				x='Contract',
				y='ChurnRate',
				color='ChurnRate',
				color_continuous_scale=['#464c89', '#dd4d88'],
				text=ct['ChurnRate'].apply(lambda v: f'{v:.1f}%'),
				labels={
					'Contract': _('Contract'),
					'ChurnRate': _('Churn Rate (%)'),
				},
			)
			fig2.update_traces(textposition='outside')
			fig2 = apply_dark_layout(
				fig2, showlegend=False, coloraxis_showscale=False
			)
			fig2 = hide_xaxis_grid(fig2)
			st.plotly_chart(fig2, width='stretch')

	if 'Tenure' in df.columns and 'MonthlyCharges' in df.columns:
		st.subheader(_('Tenure vs Monthly Charges'))
		sample = df.sample(min(1000, len(df)), random_state=42)
		label_col = sample[churn_col].astype(str)
		fig3 = px.scatter(
			sample,
			x='Tenure',
			y='MonthlyCharges',
			color=label_col,
			color_discrete_map={
				'1': '#dd4d88',
				'0': '#464c89',
				'Yes': '#dd4d88',
				'No': '#464c89',
			},
			opacity=0.6,
			labels={
				'Tenure': _('Tenure (months)'),
				'MonthlyCharges': _('Monthly Charges ($)'),
			},
		)
		fig3 = apply_dark_layout(fig3, legend_title_text=_('Churn'))
		st.plotly_chart(fig3, width='stretch')
