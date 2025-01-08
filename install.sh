# Airflow needs a home. `~/airflow` is the default, but you can put it
# somewhere else if you prefer (optional)
# Gets where this script (install.sh) is located.
SOURCE_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)
export AIRFLOW_HOME=${SOURCE_DIR}/airflow-data

# Install Airflow using the constraints file
AIRFLOW_VERSION=2.6.0
PYTHON_VERSION="$(python --version | cut -d " " -f 2 | cut -d "." -f 1-2)"
# For example: 3.6
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

# For example: https://raw.githubusercontent.com/apache/airflow/constraints-2.2.3/constraints-3.6.txt
pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"

# Install others dependencies
pip install -r requirements.txt