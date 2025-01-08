# Airflow Challenge: Orchestration with Airflow

This project is part of the "Orchestration with Airflow" track. The goal is to build and execute a Directed Acyclic Graph (DAG) to perform data extraction, transformation, and export tasks using Airflow.

## Challenge Overview

The DAG accomplishes the following tasks:

1. **Extract data from a SQLite database (`Order` table) and save it as a CSV file.**
2. **Perform a JOIN operation between the `OrderDetail` table and the previously extracted CSV, calculating the sum of `Quantity` for orders shipped to Rio de Janeiro. Save the result as `count.txt`.**
3. **Generate a final file `final_output.txt` as a placeholder for successful execution.**
4. **Include email notifications using Airflow variables.**

The tasks are orchestrated as:

```
extract_orders_task >> join_and_calculate_task >> export_final_output_task
```

---

## Prerequisites

- Python 3.8 or higher
- Linux, macOS, or Windows with WSL
- `git`

---

## Installation and Setup

Follow these steps to install and configure Airflow, and execute the project:

### Step 1: Clone the Repository

Clone the repository to your local machine:

```bash
git clone git@github.com:ThaisBarrosAlvim/AirflowChallenge.git
cd AirflowChallenge
```

### Step 2: Set Up the Environment

1. **Create a virtual environment:**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. **Run the install script:**

   ```bash
   bash install.sh
   ```

3. **Set the Airflow home directory:**

   ```bash
   export AIRFLOW_HOME=$(pwd)/airflow-data
   ```

4. **Initialize the Airflow database and start the standalone server:**

   ```bash
   airflow db reset
   airflow standalone
   ```

   After running this command, the Airflow standalone server will display a default username (`admin`) and a randomly generated password in the terminal output. **Copy this password**, as you will need it to log in to the Airflow web interface.

5. **Remove example DAGs:**

   To clean up the Airflow interface, disable the example DAGs:

   - Open the `airflow.cfg` file in the `airflow-data` directory.
   - Locate the line `load_examples = True` and change it to `load_examples = False`.
   - Restart the Airflow standalone server:

     ```bash
     airflow db reset
     airflow standalone
     ```

### Step 3: Prepare the DAGs Folder

Create the required folder structure:

```bash
mkdir -p airflow-data/dags
```

Copy the provided `elt_dag.py` file to the `dags` folder:

```bash
cp elt_dag.py airflow-data/dags/
```

### Step 4: Configure Airflow Variables

Add a variable for email notifications:

1. Open the Airflow webserver at [http://localhost:8080](http://localhost:8080).
2. Log in using the username `admin` and the password copied from the terminal output.
3. Navigate to **Admin > Variables**.
4. Create a variable with the following details:
   - **Key:** `my_email`
   - **Value:** `your_email@indicium.tech`

---

## Executing the DAG

1. **Activate the DAG:**
   In the Airflow UI, locate the DAG named `NorthwindELT` and toggle it to "On".

2. **Trigger the DAG:**
   Click the play button to trigger the DAG.

3. **Monitor Progress:**
   Use the **Graph View** or **Task Logs** to monitor the status of each task.

---

## Expected Output

- **`output_orders.csv`**: Extracted data from the `Order` table.
- **`count.txt`**: Total quantity of orders shipped to Rio de Janeiro.
- **`final_output.txt`**: Placeholder file for successful execution.

All files are saved in the `airflow-data` directory.
