from pathlib import Path

import pandas as pd

import importlib.util

MODULE_PATH = Path(__file__).parents[1] / "src" / "invoice_pipeline.py"
SPEC = importlib.util.spec_from_file_location("invoice_pipeline", MODULE_PATH)
invoice_pipeline = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(invoice_pipeline)
process_records = invoice_pipeline.process_records
read_manifest = invoice_pipeline.read_manifest
parse_pdf = invoice_pipeline.parse_pdf


def _row(invoice_id, source_file):
    return {
        "invoice_id": invoice_id,
        "vendor_name": "Acme Supplies",
        "invoice_date": "2026-11-01",
        "due_date": "2026-11-30",
        "gst_number": "29ABCDE1234F1Z5",
        "amount": "1000.00",
        "tax_amount": "180.00",
        "currency": "INR",
        "source_file": str(source_file),
    }


def test_csv_manifest_reading(tmp_path):
    file = tmp_path / "manifest.csv"
    pd.DataFrame([{"invoice_id": "INV-1", "source_file": "one.pdf"}]).to_csv(file, index=False)
    assert read_manifest(file)[0]["invoice_id"] == "INV-1"


def test_approved_invoice_and_reports(tmp_path):
    root = tmp_path / "workspace"
    inbox = root / "Input"
    inbox.mkdir(parents=True)
    source = inbox / "invoice-1.txt"
    source.write_text("synthetic invoice file", encoding="utf-8")
    suppliers = tmp_path / "suppliers.csv"
    pd.DataFrame([{"vendor_name": "Acme Supplies"}]).to_csv(suppliers, index=False)

    result = process_records(root, [_row("INV-001", source)], suppliers)
    assert result["summary"]["approved"] == 1
    assert (root / "Approved" / source.name).exists()
    assert Path(result["csv"]).exists()
    assert Path(result["xlsx"]).exists()
    assert Path(result["pdf"]).exists()


def test_duplicate_invoice_is_rejected_across_runs(tmp_path):
    root = tmp_path / "workspace"
    inbox = root / "Input"
    inbox.mkdir(parents=True)
    suppliers = tmp_path / "suppliers.csv"
    pd.DataFrame([{"vendor_name": "Acme Supplies"}]).to_csv(suppliers, index=False)

    first = inbox / "first.txt"
    first.write_text("first invoice", encoding="utf-8")
    second = inbox / "second.txt"
    second.write_text("second invoice", encoding="utf-8")

    process_records(root, [_row("INV-DUP", first)], suppliers)
    result = process_records(root, [_row("INV-DUP", second)], suppliers)
    assert result["summary"]["rejected"] == 1
    details = pd.read_csv(result["csv"])
    assert "DUPLICATE_ACROSS_RUNS" in details.iloc[0]["decision_reason"]


def test_unknown_supplier_goes_to_review(tmp_path):
    root = tmp_path / "workspace"
    inbox = root / "Input"
    inbox.mkdir(parents=True)
    source = inbox / "invoice.txt"
    source.write_text("synthetic invoice", encoding="utf-8")
    suppliers = tmp_path / "suppliers.csv"
    pd.DataFrame([{"vendor_name": "Different Supplier"}]).to_csv(suppliers, index=False)

    result = process_records(root, [_row("INV-UNKNOWN", source)], suppliers)
    assert result["summary"]["review"] == 1
    assert (root / "Review" / source.name).exists()


def test_missing_file_is_rejected(tmp_path):
    root = tmp_path / "workspace"
    result = process_records(root, [_row("INV-MISSING", root / "Input" / "missing.pdf")])
    assert result["summary"]["rejected"] == 1


def test_pdf_text_field_extraction(tmp_path):
    from reportlab.pdfgen import canvas

    pdf = tmp_path / "invoice.pdf"
    document = canvas.Canvas(str(pdf))
    lines = [
        "Invoice Number: INV-PDF-001",
        "Supplier: Acme Supplies",
        "Invoice Date: 2026-11-01",
        "GSTIN: 29ABCDE1234F1Z5",
        "Tax Amount: 180.00",
        "Grand Total: 1180.00",
    ]
    for index, line in enumerate(lines):
        document.drawString(50, 780 - index * 24, line)
    document.save()

    extracted, method = parse_pdf(pdf)
    assert method == "pdf_text"
    assert extracted["invoice_id"] == "INV-PDF-001"
    assert extracted["vendor_name"] == "Acme Supplies"
    assert extracted["gst_number"] == "29ABCDE1234F1Z5"
    assert extracted["amount"] == "1180.00"
