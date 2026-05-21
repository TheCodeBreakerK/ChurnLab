#!/bin/bash
set -euo pipefail

BASE_PATH="$(pwd)"
DATA_DIR="${BASE_PATH}/data/raw"
ZIP_FILE="${DATA_DIR}/telco-customer-churn.zip"

mkdir -p "${DATA_DIR}"

echo "Downloading Telco Customer Churn dataset..."

curl -L -o "${ZIP_FILE}" \
    "https://www.kaggle.com/api/v1/datasets/download/blastchar/telco-customer-churn"

unzip -o "${ZIP_FILE}" -d "${DATA_DIR}"
rm "${ZIP_FILE}"

echo "✅ Dataset downloaded → ${DATA_DIR}"
