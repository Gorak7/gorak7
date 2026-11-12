# Lovable dashboard build brief

Paste this complete brief into the FlowOps Operations Console project in Lovable when workspace credits are available.

Build a polished responsive enterprise operations dashboard called **FlowOps — RPA Operations Console** for two integrated demonstration projects: Automation Anywhere A360 Invoice Processing Bot and Python Bot Monitoring & Failure Alert Tool.

Persistent banner: **DEMO DATA — synthetic sample records only; no live A360 Control Room connection or real email delivery is configured.**

Pages: Overview, Invoice Processing, Exceptions, Bot Monitoring, Incidents, Reports & Evidence, Integration Guide.

Use React, TypeScript, Tailwind, shadcn/ui, Lucide icons and Recharts. Professional navy sidebar, light content area, teal/blue accent, responsive layouts.

Seed a consistent data model: 10 invoice rows (7 valid, 3 invalid), 10 execution runs (6 successful, 3 failed, 1 timeout), and 4-6 synthetic incidents. Derive all KPIs/charts from data. Do not hard-code totals separately. Include invoice search/status/source filters; execution search/status filters; failure category chart; execution status pie; invoice trend chart; incident queue with editable local status; report cards and CSV download actions; evidence checklist with local state; CSV upload with required-header validation and session-only data replacement. Include integration documentation describing the A360 CSV export contract and local Python scripts. No Supabase or secrets are required for this demo. All controls must work; no fake buttons.

Dashboard data must clearly be synthetic and should never be presented as actual A360 execution evidence. Include a note that PDF OCR and real A360 Control Room integration require local A360 configuration and testing.
