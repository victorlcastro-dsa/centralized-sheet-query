# sharepoint-sheet-merger

`Under Development`

```bash
# TODO: Implement delta queries to fetch only new files
# TODO: Implement a strategy to process different file types
# TODO: Implement a strategy to process different file formats
# TODO: Create an executable script to run the application
# TODO: Implement automated tests for the application
# TODO: Implement a strategy to handle errors and exceptions
```

## Overview

The sharepoint-sheet-merger project is designed to fetch and process files from SharePoint and generate a centralized spreadsheet. The application uses various services to interact with SharePoint, authenticate using Microsoft Graph API, and manipulate Excel files.

## Project Structure

```
sharepoint-sheet-merger/
├── .env
├── .gitignore
├── README.md
├── requirements.txt
├── app/
│   ├── __init__.py
│   ├── app.py
├── auth/
│   ├── __init__.py
│   ├── authentication.py
├── config/
│   ├── __init__.py
│   ├── logger_config.py
│   ├── settings.py
├── main.py
├── services/
│   ├── __init__.py
│   ├── base/
│   │   ├── __init__.py
│   │   ├── base_service.py
│   ├── factory/
│   │   ├── __init__.py
│   │   ├── service_factory.py
│   ├── file_processing/
│   │   ├── __init__.py
│   │   ├── file_processor.py
│   │   ├── strategies/
│   │       ├── __init__.py
│   │       ├── base_file_processing_strategy.py
│   │       ├── excel_processing_strategy.py
│   │       ├── file_processing_strategy.py
│   ├── sharepoint/
│   │   ├── __init__.py
│   │   ├── sharepoint_service.py
│   ├── spreadsheet/
│       ├── __init__.py
│       ├── spreadsheet_service.py
```

## Installation

Clone the repository:

```sh
git clone https://github.com/victorlcastro-dsa/sharepoint-sheet-merger.git
cd sharepoint-sheet-merger
```

Create a virtual environment and activate it:

```sh
python -m venv venv
source venv/bin/activate
```

Install the required dependencies:

```sh
pip install -r requirements.txt
```

Create a `.env` file in the root directory with the following content:

```plaintext
client_id = "<your_client_id>"
client_secret = "<your_client_secret>"
tenant_id = "<your_tenant_id>"
sharepoint_host = "<your_sharepoint_host>"
sharepoint_site = "<your_sharepoint_site>"
sharepoint_path = "<your_sharepoint_path>"
columns = "<your_columns>"
output_filename = "<your_output_filename>.xlsx"
origin_column_name = "<your_origin_column_name>"
log_level = "<your_log_level>"
```

## Usage

Run the application:

```sh
python main.py
```

## Configuration

### Environment Variables

The application uses environment variables to configure the SharePoint and authentication settings. These variables are loaded from the `.env` file.

### Logger Configuration

The logger configuration is set up in the `logger_config.py` file. It sets up the logging level and format.

## Code Overview

### Main Application

- `app/app.py`: Contains the `App` class that orchestrates the process of fetching and processing files from SharePoint and generating a centralized spreadsheet.

### Authentication

- `auth/authentication.py`: Contains the `AuthenticationService` class that handles authentication with Microsoft Graph API.

### Configuration

- `config/logger_config.py`: Contains the `LoggerConfig` class that sets up and obtains loggers.
- `config/settings.py`: Contains the `Settings` class that loads and stores application configuration from environment variables.

### Services

- `services/base/base_service.py`: Contains the `BaseService` abstract class for services that make HTTP requests.
- `services/factory/service_factory.py`: Contains the `ServiceFactory` class that creates and manages service instances.
- `services/file_processing/file_processor.py`: Contains the `FileProcessor` class responsible for processing files using a specified strategy.
- `services/file_processing/strategies/base_file_processing_strategy.py`: Contains the `BaseFileProcessingStrategy` abstract class for file processing strategies.
- `services/file_processing/strategies/excel_processing_strategy.py`: Contains the `ExcelProcessingStrategy` class for processing Excel files.
- `services/file_processing/strategies/file_processing_strategy.py`: Contains the `FileProcessingStrategy` abstract class for file processing strategies.
- `services/sharepoint/sharepoint_service.py`: Contains the `SharePointFolderService` class for interacting with SharePoint folders.
- `services/spreadsheet/spreadsheet_service.py`: Contains the `SpreadsheetService` class for manipulating spreadsheets.

### Entry Point

- `main.py`: The main entry point of the application. Initializes settings, logger, service factory, and the main application class, then runs the application.

## Dependencies

The project dependencies are listed in the `requirements.txt` file:

- `aiohttp==3.11.12`: Asynchronous HTTP client/server framework
- `msal==1.31.1`: Microsoft Authentication Library for Python
- `openpyxl==3.1.5`: Library to read/write Excel 2010 xlsx/xlsm/xltx/xltm files
- `pandas==2.2.3`: Data analysis and manipulation library
- `python-dotenv==1.0.1`: Reads key-value pairs from a `.env` file and can set them as environment variables
