import importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location("processor",Path(__file__).parents[1]/"src"/"process_invoices.py")
mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

def valid_row():
    return {"invoice_id":"T100","vendor_name":"Demo Vendor","invoice_date":"2026-11-01","due_date":"2026-11-30","gst_number":"29ABCDE1234F1Z5","amount":"100.00","tax_amount":"18.00","currency":"INR","source_file":"demo.pdf"}
def test_valid_invoice(): assert mod.validate(valid_row(),set())==[]
def test_duplicate_invoice(): assert "DUPLICATE_INVOICE_ID" in mod.validate(valid_row(),{"T100"})
def test_bad_gst_and_zero_amount():
    row=valid_row(); row["gst_number"]="BAD"; row["amount"]="0"
    errors=mod.validate(row,set())
    assert "INVALID_GST_FORMAT" in errors and "NON_POSITIVE_AMOUNT" in errors
def test_missing_vendor():
    row=valid_row(); row["vendor_name"]=""
    assert "MISSING_VENDOR_NAME" in mod.validate(row,set())
def test_invalid_dates_and_due_before_invoice():
    row=valid_row(); row["invoice_date"]="not-a-date"
    assert "INVALID_INVOICE_DATE" in mod.validate(row,set())
    row=valid_row(); row["due_date"]="2026-10-01"
    assert "DUE_DATE_BEFORE_INVOICE_DATE" in mod.validate(row,set())
def test_invalid_currency_and_negative_tax():
    row=valid_row(); row["currency"]="US"; row["tax_amount"]="-1"
    errors=mod.validate(row,set())
    assert "INVALID_CURRENCY" in errors and "NEGATIVE_TAX" in errors
def test_process_demo_and_sqlite_idempotency(tmp_path):
    source=Path(__file__).parents[1]/"data"/"invoices_demo.csv"
    db=tmp_path/"invoices.db"; out=tmp_path/"out"
    first=mod.process_file(source,out,f"sqlite:///{db}")
    second=mod.process_file(source,out,f"sqlite:///{db}")
    assert first["total"]==10 and first["accepted"]+first["rejected"]==10
    assert second["total"]==10
    from sqlalchemy import create_engine,text
    engine=create_engine(f"sqlite:///{db}")
    with engine.connect() as conn:
        assert conn.execute(text("select count(*) from invoices")).scalar()==first["accepted"]
    engine.dispose()
    assert (out/"execution_logs.csv").exists()
