import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components.kpi_card import render_kpi_card
from services.constants import COLORS
from services.benchmark_service import (
	HIGHER_IS_BETTER,
	get_best_model,
	get_ranking,
	highlight_best,
	load_report,
)
from utils.i18n import _
from utils.plotly_config import (
	apply_dark_layout,
	hide_color_scale,
	hide_xaxis_grid,
)


def render_benchmark() -> None:
	"""Benchmark page: model performance comparison tables and charts."""
	st.title(_('Models Benchmark'))
	st.caption(
		_('Compare trained model performance across key evaluation metrics.')
	)
	st.divider()

	try:
		df = load_report()
	except Exception as e:
		st.error(
			f'Could not load report: `reports/model_comparison.csv` — {e}'
		)
		return

	model_col = df.columns[0]

	if 'ROC AUC' in df.columns:
		best_name, best_roc = get_best_model(df, 'ROC AUC')
		avg_roc = df['ROC AUC'].mean()
		avg_f1 = df['F1 Score'].mean() if 'F1 Score' in df.columns else 0.0

		k1, k2, k3, k4 = st.columns(4)
		render_kpi_card(k1, _('Best Model'), best_name)
		render_kpi_card(k2, _('Best ROC AUC'), f'{best_roc:.4f}')
		render_kpi_card(k3, _('Avg ROC AUC'), f'{avg_roc:.4f}')
		render_kpi_card(k4, _('Avg F1 Score'), f'{avg_f1:.4f}')
		st.divider()

	metric_cols = [c for c in HIGHER_IS_BETTER if c in df.columns]

	st.subheader(_('Full Comparison Table'))
	sort_col = st.selectbox(
		_('Sort by'),
		options=[c for c in df.columns if c != model_col],
		index=0,
	)
	df_sorted = get_ranking(df, sort_col)
	st.dataframe(
		highlight_best(df_sorted),
		width='stretch',
		hide_index=True,
	)

	if metric_cols:
		st.divider()
		st.subheader(_('Metric Comparison'))
		melted = df_sorted.melt(
			id_vars=model_col,
			value_vars=metric_cols,
			var_name='Metric',
			value_name='Score',
		)
		fig = px.bar(
			melted,
			x='Metric',
			y='Score',
			color=model_col,
			barmode='group',
			color_discrete_sequence=COLORS['model_sequence'][1:5],
			text=melted['Score'].apply(lambda v: f'{v:.3f}'),
			labels={'Metric': _('Metric'), 'Score': _('Score')},
		)
		fig = apply_dark_layout(fig, legend_title_text=_('Model'))
		fig = hide_xaxis_grid(fig)
		fig.update_yaxes(range=[0, 1.05])
		fig.update_traces(textposition='outside', textfont_size=10)
		st.plotly_chart(fig, width='stretch')

	if len(metric_cols) >= 3:
		st.subheader(_('Radar Chart'))
		fig_radar = go.Figure()
		model_colors = COLORS['model_sequence'][1:5]
		for idx, row in df_sorted.iterrows():
			fig_radar.add_trace(
				go.Scatterpolar(
					r=[row[m] for m in metric_cols] + [row[metric_cols[0]]],
					theta=metric_cols + [metric_cols[0]],
					fill='toself',
					name=str(row[model_col]),
					opacity=0.7,
					line=dict(
						color=model_colors[idx % len(model_colors)], width=1.5
					),
				)
			)
		grid = COLORS['muted']
		fig_radar = apply_dark_layout(
			fig_radar,
			plot_bgcolor='#121212',
			polar=dict(
				bgcolor='#121212',
				radialaxis=dict(
					visible=True,
					range=[0, 1],
					gridcolor=grid,
					gridwidth=0.5,
				),
				angularaxis=dict(gridcolor=grid, gridwidth=0.5),
			),
			margin=dict(l=40, r=40, t=24, b=40),
		)
		st.plotly_chart(fig_radar, width='stretch')

	if 'Predict Time' in df.columns:
		st.subheader(_('Prediction Speed'))
		fig_time = px.bar(
			df_sorted,
			x=model_col,
			y='Predict Time',
			color='Predict Time',
			color_continuous_scale=['#464c89', '#ff6b59'],
			text=df_sorted['Predict Time'].apply(lambda v: f'{v:.4f}s'),
			labels={
				'Predict Time': _('Predict Time (s)'),
				'Model': _('Model'),
			},
		)
		fig_time = apply_dark_layout(fig_time)
		fig_time = hide_color_scale(fig_time)
		fig_time = hide_xaxis_grid(fig_time)
		fig_time.update_traces(textposition='outside')
		st.plotly_chart(fig_time, width='stretch')
