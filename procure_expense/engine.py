"""Automated 3-Way Purchase Matching (PO vs GRN vs Invoice) & Cash Flow Outflow Forecasting."""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field


@dataclass
class PurchaseOrderLine:
    item_code: str
    po_quantity: float
    po_rate: float


@dataclass
class GoodsReceiptLine:
    item_code: str
    received_quantity: float
    accepted_quantity: float
    rejected_quantity: float


@dataclass
class SupplierInvoiceLine:
    item_code: str
    billed_quantity: float
    billed_rate: float


@dataclass
class ThreeWayMatchAudit:
    po_number: str
    invoice_number: str
    is_quantity_matched: bool
    is_rate_matched: bool
    is_approved_for_payment: bool
    quantity_variance: float
    price_variance_inr: float
    status: str  # MATCHED_APPROVED, QUANTITY_OVERBILLED, PRICE_VARIANCE_BREACH


class PurchaseExpenseMatchingEngine:
    """Prevents fraudulent vendor overbilling via strict 3-way matching between PO, GRN, and Purchase Invoices."""

    PRICE_TOLERANCE_PCT = 1.0  # 1% allowable price variation

    def execute_3way_match(
        self,
        po_no: str,
        inv_no: str,
        po_lines: List[PurchaseOrderLine],
        grn_lines: List[GoodsReceiptLine],
        inv_lines: List[SupplierInvoiceLine]
    ) -> ThreeWayMatchAudit:
        grn_map = {g.item_code: g.accepted_quantity for g in grn_lines}
        po_rate_map = {p.item_code: p.po_rate for p in po_lines}

        qty_matched = True
        rate_matched = True
        total_qty_variance = 0.0
        total_price_variance = 0.0

        for inv in inv_lines:
            accepted_qty = grn_map.get(inv.item_code, 0.0)
            contracted_rate = po_rate_map.get(inv.item_code, 0.0)

            # Check quantity: Billed must not exceed physically accepted goods
            if inv.billed_quantity > accepted_qty:
                qty_matched = False
                total_qty_variance += (inv.billed_quantity - accepted_qty)

            # Check price: Rate must be within tolerance
            rate_diff = inv.billed_rate - contracted_rate
            if rate_diff > (contracted_rate * self.PRICE_TOLERANCE_PCT / 100.0):
                rate_matched = False
                total_price_variance += rate_diff * inv.billed_quantity

        approved = qty_matched and rate_matched
        if approved:
            status = "MATCHED_APPROVED"
        elif not qty_matched:
            status = "QUANTITY_OVERBILLED"
        else:
            status = "PRICE_VARIANCE_BREACH"

        return ThreeWayMatchAudit(
            po_number=po_no,
            invoice_number=inv_no,
            is_quantity_matched=qty_matched,
            is_rate_matched=rate_matched,
            is_approved_for_payment=approved,
            quantity_variance=round(total_qty_variance, 2),
            price_variance_inr=round(total_price_variance, 2),
            status=status
        )
