# Airflow ETL Weather Project

This project aims to extract weather data using **Weather API** free services, transform the data into the desired format, and save it locally or in an online storage destination. It was created to help me learn and practice various technologies while implementing ETL (Extract, Transform, Load) procedures.

## Technologies Used

- **Apache Airflow**
- **Python**
- **Visual Studio Code (SSH Connection Extension)**
- **Amazon EC2 Virtual Machine**
- **Amazon S3 Storage**
- **Linux**
- **Git**

## Project Details

This project seamlessly integrates various technologies to execute the ETL process:

**Apache Airflow** serves as the core of the ETL workflow. It enables task scheduling and management and runs on an **Amazon EC2 Virtual Machine**, which hosts the Airflow instance. The EC2 VM runs **Linux** as Airflow cannot be set up on a Windows machine. **Python** is used for scripting the ETL workflow and creating the **Directed Acyclic Graph (DAG)**, defining the sequence of steps executed periodically (e.g., hourly, daily, weekly).

**Visual Studio Code**, equipped with the **SSH Connection Extension**, ensures smooth connectivity between the local Windows machine and the EC2 VM. This facilitates remote server interactions, a crucial aspect of this project, and allows the easy usage of version control with the goal of updating live the code of the project in GitHub.

**Amazon S3 Storage** serves as the designated destination for storing the processed weather data, ensuring data durability and accessibility. Processed data is transformed into the desired CSV format and saved to Amazon S3.

## DAG Setup

To set up the DAG of the project, we follow these steps:

1. Create a `weather_dag.py` file in the 'DAGS' directory.
2. Initialize a DAG Object.
3. Define the following components using the aforementioned Object:

   - **is_weather_api_ready**: Checks if the Weather API is online using an `HttpSensor`.
   - **extract_weather_data**: Retrieves weather data using a `SimpleHttpOperator`.
   - **transform_load_data**: Transforms the data into the desired CSV format and saves it to the Amazon S3 Storage.

Both the API and S3 Storage steps require **authentication** tokens to function correctly.

## Future extensions

Future enhancements for this project may include extending data extraction to encompass multiple greek regions and spanning across multiple days. This expanded dataset will enable us to derive valuable insights by utilizing powerful data visualization tools like Power BI and Tableau, thereby broadening the project's scope into the realm of data analysis.

Furthermore, with this enriched dataset, we can explore the exciting possibilities of applying machine learning algorithms. These algorithms can be leveraged to make predictions about future weather conditions, offering valuable forecasts. Additionally, we have the potential to fine-tune and train pre-existing deep learning models, unlocking their full capabilities for more advanced weather forecasting and analysis.
