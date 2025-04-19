
# 🍎 Azure Blob-Triggered Fruit Classification System

This project is an automated image classification system that uses Azure Functions and Custom Vision AI to classify fruit images uploaded to Azure Blob Storage. The system updates the count of each classified fruit in an Azure SQL Database and deletes the image afterward to maintain cleanliness.

---

## 📦 Project Structure

```
FruitClassifier/
│
├── Azure                        # All screenshots from Azure Portal
├── Azure Diagram                # It have the solution diagram picture
├── function_app.py              # Main function logic
├── requirements.txt             # Python dependencies
├── host.json                    # Azure Functions host configuration
├── local.settings.json          # Local environment settings
└── .vscode/                     # VS Code debug configs (optional)
```

---

## ⚙️ How It Works

1. **Trigger**: Uploading a fruit image to Blob Storage (`input/` container) triggers the Azure Function.
2. **Prediction**: The image is sent to a Custom Vision API for classification.
3. **Database Update**: The predicted fruit type count is incremented in Azure SQL Database.
4. **Cleanup**: The blob is deleted after processing.

---

## 🚀 Tech Stack

- **Azure Blob Storage** - Image trigger and storage
- **Azure Functions** - Serverless logic
- **Azure Custom Vision** - Image classification
- **Azure SQL Database** - Data storage
- **Python** (3.11) - Function runtime
- **pyodbc** - Database driver

---

## 🧪 Local Development Setup

### 1. Prerequisites

- [Azure CLI](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli)
- [Azure Functions Core Tools](https://learn.microsoft.com/en-us/azure/azure-functions/functions-run-local?wt.mc_id=studentamb_299177)
- Python 3.11
- [ODBC Driver 18 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16?wt.mc_id=studentamb_299177)
- `pyodbc` installed:  
  ```bash
  pip install pyodbc
  ```

### 2. Clone and Setup

```bash
git clone https://github.com/your-username/fruit-classifier.git
cd FruitClassifier
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Local Configuration

Edit your `local.settings.json`:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "<your_blob_storage_connection_string>",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "PREDICTION_KEY": "<your_prediction_key>",
    "PREDICTION_URL": "<your_custom_vision_prediction_url>",
    "SQL_CONNECTION_STRING": "Driver={ODBC Driver 18 for SQL Server};Server=tcp:<your_server>.database.windows.net,1433;Database=<your_db>;Uid=<your_user>;Pwd=<your_password>;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
  }
}
```

---

## ☁️ Deploy to Azure

### 1. Create a Function App

```bash
az functionapp create   --resource-group <your-resource-group>   --consumption-plan-location <location>   --runtime python   --functions-version 4   --name <your-functionapp-name>   --storage-account <your-storage-account-name>
```

### 2. Publish the Function

```bash
func azure functionapp publish <your-functionapp-name>
```

---

## 🧾 Example Output

When a blob is uploaded:

```
Processing blob: input/apple.jpg
Classified as: Apple
Updated 'Apple' count in database.
Deleted blob after processing.
```

---

## 🔐 Notes

- Ensure you have the **ODBC Driver 18** installed for SQL Server.
- Secure your credentials using [Azure Key Vault](https://learn.microsoft.com/en-us/azure/key-vault/general/basic-concepts?wt.mc_id=studentamb_299177).
