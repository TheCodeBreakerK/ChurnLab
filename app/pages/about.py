import streamlit as st

from utils.i18n import _


def render_about() -> None:
	"""About page: project description, tech stack, and links."""
	st.title(_('About ChurnLab'))
	st.caption(
		_(
			'End-to-end Machine Learning project for '
			'Telecom Customer Churn Prediction.'
		)
	)
	st.divider()

	st.subheader(_('Project Description'))
	st.markdown(
		_(
			'ChurnLab is a production-ready Machine Learning application '
			'that predicts telecom customer churn. Four models '
			'(Logistic Regression, Decision Tree, Random Forest, and XGBoost) '
			'were trained, tuned with Optuna, and evaluated on the '
			'IBM Telco Customer Churn dataset.'
		)
	)
	st.markdown(
		_(
			'The application provides an interactive prediction interface '
			'where users can select a model, input customer features, and '
			'receive a churn probability with risk classification. '
			'A benchmark dashboard compares model performance across '
			'ROC AUC, PR AUC, Accuracy, Precision, Recall, F1 Score, and '
			'Prediction Time.'
		)
	)

	st.divider()
	st.subheader(_('Technology Stack'))

	col1, col2 = st.columns(2)
	with col1:
		st.markdown(
			'- **Python**  \n'
			'- **Streamlit**  \n'
			'- **scikit-learn**  \n'
			'- **XGBoost**  \n'
			'- **Optuna**'
		)
	with col2:
		st.markdown('- **Pandas[parquet]**  \n- **Plotly**  \n- **Docker**')

	st.divider()
	st.subheader(_('Links'))

	link_col1, link_col2 = st.columns(2)
	with link_col1:
		st.markdown(
			'[![GitHub](https://skillicons.dev/icons?i=github)](https://github.com/TheCodeBreakerK)'
		)
	with link_col2:
		st.markdown(
			'[![LinkedIn](https://skillicons.dev/icons?i=linkedin)](https://www.linkedin.com/in/kelvin-moreira-santos-oliveira)'
		)
