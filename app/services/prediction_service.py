import pandas as pd


def build_input_dataframe(
	gender: str,
	senior_citizen: str,
	partner: str,
	dependents: str,
	tenure: int,
	phone_service: str,
	multiple_lines: str,
	internet_service: str,
	online_security: str,
	online_backup: str,
	device_protection: str,
	tech_support: str,
	streaming_tv: str,
	streaming_movies: str,
	contract: str,
	paperless_billing: str,
	payment_method: str,
	monthly_charges: float,
) -> pd.DataFrame:
	"""Build a single-row DataFrame from user inputs for model inference."""
	return pd.DataFrame(
		[
			{
				'Gender': gender,
				'SeniorCitizen': senior_citizen,
				'Partner': partner,
				'Dependents': dependents,
				'Tenure': tenure,
				'PhoneService': phone_service,
				'MultipleLines': multiple_lines,
				'InternetService': internet_service,
				'OnlineSecurity': online_security,
				'OnlineBackup': online_backup,
				'DeviceProtection': device_protection,
				'TechSupport': tech_support,
				'StreamingTV': streaming_tv,
				'StreamingMovies': streaming_movies,
				'Contract': contract,
				'PaperlessBilling': paperless_billing,
				'PaymentMethod': payment_method,
				'MonthlyCharges': monthly_charges,
			}
		]
	)


def align_features(
	input_df: pd.DataFrame, feature_cols: list[str]
) -> pd.DataFrame:
	"""Ensure *input_df* contains every column in *feature_cols*, filling missing ones with ``'No'``."""
	for col in feature_cols:
		if col not in input_df.columns:
			input_df[col] = 'No'

	return input_df[feature_cols]


def predict_proba(model, input_df: pd.DataFrame) -> float:
	"""Return churn probability from *model*."""
	return float(model.predict_proba(input_df)[0][1])


def extract_feature_importance(
	artifacts: dict, feature_cols: list[str]
) -> pd.Series | None:
	"""Extract top 10 feature importances, or ``None`` if not available."""
	fi = artifacts.get('feature_importances') or artifacts.get(
		'feature_importance'
	)
	if fi is not None and feature_cols and len(fi) == len(feature_cols):
		return (
			pd.Series(fi, index=feature_cols)
			.sort_values(ascending=True)
			.tail(10)
		)

	return None
