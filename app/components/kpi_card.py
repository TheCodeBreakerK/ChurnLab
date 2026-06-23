def render_kpi_card(
	col,
	label: str,
	value: str,
	delta: str | None = None,
	delta_color: str = 'normal',
) -> None:
	"""Render a KPI metric card inside a Streamlit column."""
	col.metric(
		label=label,
		value=value,
		delta=delta if delta else None,
		delta_color=delta_color,
	)
