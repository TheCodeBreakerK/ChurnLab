import streamlit as st
import plotly.graph_objects as go

from utils.i18n import _


def _risk_badge(prob: float) -> tuple[str, str]:
	"""Return (risk_label, hex_color) based on churn probability thresholds."""
	if prob >= 0.70:
		return _('High Risk'), '#e85d5d'

	if prob >= 0.40:
		return _('Medium Risk'), '#ffa600'

	return _('Low Risk'), '#5cb87a'


def render_prediction_result(probability: float) -> None:
	"""Display the churn probability, risk badge, and gauge chart."""
	risk_label, risk_color = _risk_badge(probability)

	col1, col2 = st.columns([1, 2])
	with col1:
		st.metric(_('Churn Probability'), f'{probability * 100:.1f}%')
		st.markdown(
			f"<span style='font-size:1.4rem;font-weight:700;color:{risk_color}'>{risk_label}</span>",
			unsafe_allow_html=True,
		)
	with col2:
		fig = go.Figure(
			go.Indicator(
				mode='gauge+number',
				value=probability * 100,
				number={'suffix': '%'},
				gauge={
					'axis': {'range': [0, 100]},
					'bar': {'color': risk_color},
					'steps': [
						{'range': [0, 40], 'color': '#003d5c'},
						{'range': [40, 70], 'color': '#464c89'},
						{'range': [70, 100], 'color': '#954e9b'},
					],
					'threshold': {
						'line': {'color': '#dd4d88', 'width': 4},
						'value': 50,
					},
				},
			)
		)
		fig.update_layout(
			height=220,
			margin=dict(l=20, r=20, t=20, b=0),
			paper_bgcolor='rgba(0,0,0,0)',
		)
		st.plotly_chart(fig, width='stretch')
