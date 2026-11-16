# Frappe 3-Way Purchase Matching & Expense Tracking Engine

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Procurement](https://img.shields.io/badge/Purchase-3--Way%20PO%20Matching-darkgreen.svg)](https://frappe.io)

Stops procurement leakage by enforcing strict 3-way matching between Purchase Orders, warehouse Goods Receipt Notes (GRN), and vendor Purchase Invoices before payment approval.

## Features
- **3-Way Discrepancy Gate:** Blocks supplier invoice payment approval if billed quantities exceed physically accepted stock.
- **Contract Rate Variance Tolerance:** Catches vendor price escalations violating original purchase orders.
- **Cash Flow Outflow Forecasting:** Projects supplier disbursement liabilities across 15, 30, and 60-day aging buckets.

## Tests
```bash
python3 -m unittest discover tests
```
