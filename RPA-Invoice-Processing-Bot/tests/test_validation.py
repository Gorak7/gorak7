import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location("processor",Path(__file__).parents[1]/"src"/"process_invoices.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

def valid_row():
    return {"invoice_id":"T100","vendor_name":"Demo Vendor","invoice_date":"2026-11-01",
    "due_date":"2026-11-30","gst_number":"29ABCDE1234F1Z5","amount":"100.00",
    "tax_amount":"18.00","currency":"INR","source_file":"demo.pdf"}

def test_valid_invoice():
    assert mod.validate(valid_row(),set())==[]

def test_duplicate_invoice():
    seen={"T100"}
    assert "DUPLICATE_INVOICE_ID" in mod.validate(valid_row(),seen)

def test_bad_gst_and_zero_amount():
    row=valid_row(); row["gst_number"]="BAD"; row["amount"]="0"
    errors=mod.validate(row,set())
    assert "INVALID_GST_FORMAT" in errors
    assert "NON_POSITIVE_AMOUNT" in errors

def test_missing_vendor():
    row=valid_row(); row["vendor_name"]=""
    assert "MISSING_VENDOR_NAME" in mod.validate(row,set())
