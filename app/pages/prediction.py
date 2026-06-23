import plotly.express as px
import streamlit as st

from components.model_selector import render_model_selector
from components.prediction_result import render_prediction_result
from services.constants import ARTIFACT_PATHS, MODEL_PATHS
from services.model_loader import load_artifacts, load_model
from services.prediction_service import (
	align_features,
	build_input_dataframe,
	extract_feature_importance,
	predict_proba,
)
from utils.i18n import _
from utils.plotly_config import (
	apply_dark_layout,
	hide_color_scale,
	hide_xaxis_grid,
)


def render_prediction() -> None:
	"""Prediction page: model selection, customer form, and churn result."""
	st.title(_('Churn Prediction'))
	st.caption(
		_(
			'Select a model and fill in customer details to predict '
			'churn probability.'
		)
	)
	st.divider()

	model_name = render_model_selector()
	if model_name is None:
		return

	model_path = MODEL_PATHS[model_name]
	artifact_path = ARTIFACT_PATHS[model_name]

	if not model_path.exists():
		st.warning(_('Model file not found at: ') + str(model_path))
		return

	model = load_model(model_path)
	artifacts = (
		load_artifacts(artifact_path)
		if artifact_path and artifact_path.exists()
		else {}
	)
	feature_cols: list[str] = artifacts.get('feature_names', [])

	st.divider()
	st.subheader(_('Customer Information'))

	with st.form('prediction_form'):
		col1, col2, col3 = st.columns(3)

		with col1:
			st.markdown(f'**{_("Profile")}**')
			gender = st.selectbox(_('Gender'), ['Male', 'Female'])
			senior_citizen = st.selectbox(_('Senior Citizen'), ['No', 'Yes'])
			senior_citizen = 1 if senior_citizen == 'Yes' else 0
			partner = st.selectbox(_('Partner'), ['Yes', 'No'])
			dependents = st.selectbox(_('Dependents'), ['Yes', 'No'])
			tenure = st.slider(_('Tenure (months)'), 0, 72, 12)
			phone_service = st.selectbox(_('Phone Service'), ['Yes', 'No'])

		with col2:
			st.markdown(f'**{_("Services")}**')
			multiple_lines = st.selectbox(
				_('Multiple Lines'), ['Yes', 'No', 'No phone service']
			)
			internet_service = st.selectbox(
				_('Internet Service'), ['Fiber optic', 'DSL', 'No']
			)
			online_security = st.selectbox(
				_('Online Security'),
				['Yes', 'No', 'No internet service'],
			)
			online_backup = st.selectbox(
				_('Online Backup'), ['Yes', 'No', 'No internet service']
			)
			device_protection = st.selectbox(
				_('Device Protection'),
				['Yes', 'No', 'No internet service'],
			)
			tech_support = st.selectbox(
				_('Tech Support'), ['Yes', 'No', 'No internet service']
			)
			streaming_tv = st.selectbox(
				_('Streaming TV'), ['Yes', 'No', 'No internet service']
			)
			streaming_movies = st.selectbox(
				_('Streaming Movies'),
				['Yes', 'No', 'No internet service'],
			)

		with col3:
			st.markdown(f'**{_("Billing")}**')
			contract = st.selectbox(
				_('Contract'),
				['Month-to-month', 'One year', 'Two year'],
			)
			paperless_billing = st.selectbox(
				_('Paperless Billing'), ['Yes', 'No']
			)
			payment_method = st.selectbox(
				_('Payment Method'),
				[
					'Electronic check',
					'Mailed check',
					'Bank transfer (automatic)',
					'Credit card (automatic)',
				],
			)
			monthly_charges = st.number_input(
				_('Monthly Charges ($)'), 0.0, 200.0, 65.0, step=1.0
			)

		st.divider()
		submitted = st.form_submit_button(
			_('Predict'), type='primary', width='stretch'
		)

	if submitted:
		input_df = build_input_dataframe(
			gender,
			senior_citizen,
			partner,
			dependents,
			tenure,
			phone_service,
			multiple_lines,
			internet_service,
			online_security,
			online_backup,
			device_protection,
			tech_support,
			streaming_tv,
			streaming_movies,
			contract,
			paperless_billing,
			payment_method,
			monthly_charges,
		)

		if feature_cols:
			input_df = align_features(input_df, feature_cols)

		try:
			prob = predict_proba(model, input_df)
		except Exception:
			try:
				prob = float(model.predict(input_df)[0])
			except Exception as e:
				st.error(f'Prediction failed: {e}')
				return

		st.divider()
		render_prediction_result(prob)

		fi_series = extract_feature_importance(artifacts, feature_cols)
		if fi_series is not None:
			st.subheader(_('Feature Importance'))
			fig_fi = px.bar(
				fi_series.reset_index(),
				x=fi_series.values,
				y=fi_series.index,
				orientation='h',
				color=fi_series.values,
				color_continuous_scale=['#464c89', '#dd4d88'],
				labels={'x': _('Importance'), 'index': _('Feature')},
			)
			fig_fi = apply_dark_layout(fig_fi)
			fig_fi = hide_color_scale(fig_fi)
			fig_fi = hide_xaxis_grid(fig_fi)
			st.plotly_chart(fig_fi, width='stretch')
