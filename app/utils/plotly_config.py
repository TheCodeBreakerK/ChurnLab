import plotly.graph_objects as go
from services.constants import COLORS


def apply_dark_layout(fig: go.Figure, **extra) -> go.Figure:
	"""Apply the app's dark theme to a Plotly figure."""
	font_color = 'rgba(255,255,255,0.87)'
	grid_color = COLORS['muted']

	extra.setdefault('plot_bgcolor', 'rgba(0,0,0,0)')
	extra.setdefault('paper_bgcolor', 'rgba(0,0,0,0)')
	extra.setdefault('margin', dict(l=0, r=0, t=24, b=0))

	fig.update_layout(
		xaxis=dict(showgrid=True, gridcolor=grid_color, gridwidth=0.5),
		yaxis=dict(showgrid=True, gridcolor=grid_color, gridwidth=0.5),
		font=dict(color=font_color),
		hoverlabel=dict(
			bgcolor='#222222',
			bordercolor='#464c89',
			font=dict(color='#FFFFFF'),
		),
		**extra,
	)

	return fig


def hide_xaxis_grid(fig: go.Figure) -> go.Figure:
	fig.update_xaxes(showgrid=False)

	return fig


def hide_color_scale(fig: go.Figure) -> go.Figure:
	fig.update_layout(coloraxis_showscale=False)

	return fig
