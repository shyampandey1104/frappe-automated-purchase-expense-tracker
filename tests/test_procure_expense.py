import unittest
from procure_expense.engine import (
    PurchaseExpenseMatchingEngine,
    PurchaseOrderLine,
    GoodsReceiptLine,
    SupplierInvoiceLine
)

class TestPurchaseMatching(unittest.TestCase):
    def test_three_way_match_successful(self):
        engine = PurchaseExpenseMatchingEngine()

        po = [PurchaseOrderLine("RAW-STEEL-BAR", 100.0, 500.0)]
        grn = [GoodsReceiptLine("RAW-STEEL-BAR", 100.0, 100.0, 0.0)] # 100 accepted
        inv = [SupplierInvoiceLine("RAW-STEEL-BAR", 100.0, 500.0)]     # 100 billed @ 500

        res = engine.execute_3way_match("PO-901", "PINV-441", po, grn, inv)
        self.assertTrue(res.is_approved_for_payment)
        self.assertEqual(res.status, "MATCHED_APPROVED")

    def test_quantity_overbilled_rejection(self):
        engine = PurchaseExpenseMatchingEngine()

        po = [PurchaseOrderLine("RAW-STEEL-BAR", 100.0, 500.0)]
        grn = [GoodsReceiptLine("RAW-STEEL-BAR", 100.0, 80.0, 20.0)] # Only 80 accepted, 20 rejected
        inv = [SupplierInvoiceLine("RAW-STEEL-BAR", 100.0, 500.0)]    # Vendor billed for full 100

        res = engine.execute_3way_match("PO-901", "PINV-442", po, grn, inv)
        self.assertFalse(res.is_approved_for_payment)
        self.assertEqual(res.status, "QUANTITY_OVERBILLED")
        self.assertEqual(res.quantity_variance, 20.0)

if __name__ == "__main__":
    unittest.main()
