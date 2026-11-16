# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "procure_expense"
app_title = "Frappe Automated Purchase Expense Tracker"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Automated Purchase Expense Tracker for Frappe and ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/procure_expense/css/procure_expense.bundle.css"
app_include_js = "/assets/procure_expense/js/procure_expense.bundle.js"

# Document Events
# ---------------
doc_events = {
    "DocType Event": {
        "on_submit": "procure_expense.engine.on_document_submit",
        "on_cancel": "procure_expense.engine.on_document_cancel"
    }
}

# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily": [
        "procure_expense.engine.daily_scheduled_sync"
    ]
}
