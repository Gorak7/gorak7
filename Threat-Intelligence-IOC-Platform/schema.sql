CREATE TABLE IF NOT EXISTS iocs (
  id BIGSERIAL PRIMARY KEY,
  value VARCHAR(500) NOT NULL,
  type TEXT NOT NULL CHECK (type IN ('ip','domain','url','hash')),
  severity TEXT NOT NULL CHECK (severity IN ('low','medium','high','critical')),
  confidence SMALLINT NOT NULL CHECK (confidence BETWEEN 0 AND 100),
  status TEXT NOT NULL DEFAULT 'new' CHECK (status IN ('new','investigating','confirmed','false_positive')),
  source TEXT NOT NULL DEFAULT 'analyst',
  notes TEXT NOT NULL DEFAULT '',
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  UNIQUE(value,type)
);
CREATE INDEX IF NOT EXISTS iocs_type_idx ON iocs(type);
CREATE INDEX IF NOT EXISTS iocs_severity_idx ON iocs(severity);
CREATE INDEX IF NOT EXISTS iocs_status_idx ON iocs(status);
