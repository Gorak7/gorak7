CREATE DATABASE IF NOT EXISTS rpa_ops;
USE rpa_ops;
CREATE TABLE IF NOT EXISTS invoices (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  invoice_id VARCHAR(64) NOT NULL UNIQUE,
  vendor_name VARCHAR(255) NOT NULL,
  invoice_date DATE,
  due_date DATE,
  gst_number VARCHAR(32),
  amount DECIMAL(14,2) NOT NULL,
  tax_amount DECIMAL(14,2) DEFAULT 0,
  currency CHAR(3) DEFAULT 'INR',
  source_file VARCHAR(255),
  run_id VARCHAR(64),
  processed_at DATETIME
);
CREATE TABLE IF NOT EXISTS invoice_exceptions (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  invoice_id VARCHAR(64),
  vendor_name VARCHAR(255),
  error_codes TEXT,
  run_id VARCHAR(64),
  processed_at DATETIME
);
CREATE TABLE IF NOT EXISTS bot_execution_logs (
  id BIGINT AUTO_INCREMENT PRIMARY KEY,
  run_id VARCHAR(64) NOT NULL,
  invoice_id VARCHAR(64),
  status VARCHAR(20) NOT NULL,
  error_category VARCHAR(40),
  error_message TEXT,
  started_at DATETIME,
  completed_at DATETIME
);
