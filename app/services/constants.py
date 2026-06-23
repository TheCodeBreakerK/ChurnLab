from pathlib import Path


BASE = Path('models')

MODEL_PATHS: dict[str, Path] = {
	'Logistic Regression': (
		BASE / 'logistic_regression' / 'logistic_regression_best_model.joblib'
	),
	'Decision Tree': (
		BASE / 'decision_tree' / 'decision_tree_best_model.joblib'
	),
	'Random Forest': (
		BASE / 'random_forest' / 'random_forest_best_model.joblib'
	),
	'XGBoost': (BASE / 'xgboost' / 'xgboost_best_model.joblib'),
}

ARTIFACT_PATHS: dict[str, Path] = {
	name: path.parent / path.name.replace('best_model', 'artifacts')
	for name, path in MODEL_PATHS.items()
}

COLORS = {
	'muted': 'rgba(255,255,255,0.10)',
	'model_sequence': [
		'#003d5c',
		'#464c89',
		'#954e9b',
		'#dd4d88',
		'#ff6b59',
		'#ffa600',
	],
}
