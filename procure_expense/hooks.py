# Copyright (c) 2026, Shyamkumar Pandey and contributors
# For license information, please see license.txt

app_name = "procure_expense"
app_title = "Frappe Automated Purchase Expense Tracker"
app_publisher = "Shyamkumar Pandey"
app_description = "Frappe Automated Purchase Expense Tracker - Enterprise Multi-DocType Solution for Frappe & ERPNext"
app_email = "shyampandey1104@gmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------
app_include_css = "/assets/procure_expense/css/procure_expense.bundle.css"
app_include_js = "/assets/procure_expense/js/procure_expense.bundle.js"

# Document Events
# ---------------
doc_events = {
    "Frappe Automated Purchase Expense Tracker Entry": {
        "validate": "procure_expense.services.validator.EnterpriseValidationEngine.validate_compliance_rules",
        "on_submit": "procure_expense.services.integration_service.EnterpriseIntegrationService.verify_remote_status"
    }
}

# Scheduled Background Tasks
# --------------------------
scheduler_events = {
    "hourly": [
        "procure_expense.tasks.hourly_sync"
    ],
    "daily": [
        "procure_expense.tasks.daily_reconciliation"
    ],
    "weekly": [
        "procure_expense.tasks.weekly_digest"
    ]
}
