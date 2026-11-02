from pathlib import Path
from datetime import date
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import zipfile

ROOT=Path("GRC-Analyst-Portfolio")
P1=ROOT/"01_Mini_Compliance_Program_ISO27001"; P2=ROOT/"02_Third_Party_Vendor_Risk_Assessment"
P1.mkdir(parents=True,exist_ok=True); P2.mkdir(parents=True,exist_ok=True)
PURPLE="5B2C83"; DARK="243247"; GREEN="D9EAD3"; YELLOW="FFF2CC"; RED="F4CCCC"
controls=[
("A.5.1","Information security policies","Governance","Policy approval and annual review","Partial","GRC Lead","SIM-ISO-01","Draft policy only; approval evidence missing","Obtain executive approval and publish policy","30 days","High"),
("A.5.2","Information security roles","Governance","Named security owners and responsibilities","Implemented","CISO","SIM-ISO-02","Sample RACI recorded","Review RACI after organization changes","90 days","Low"),
("A.5.9","Inventory of information and assets","Asset Management","Asset inventory, owners and classification","Partial","IT Operations","SIM-ISO-03","Laptop and SaaS inventory incomplete","Reconcile inventory and assign owners","45 days","High"),
("A.5.10","Acceptable use","Asset Management","Workforce acceptable-use acknowledgement","Planned","HR / IT","SIM-ISO-04","Acknowledgement register unavailable","Publish standard and collect acknowledgements","60 days","Medium"),
("A.5.15","Access control","Identity & Access","Documented access policy and approvals","Implemented","IAM Lead","SIM-ISO-05","Sample access workflow described","Test quarterly access reviews","60 days","Low"),
("A.5.16","Identity management","Identity & Access","Identity lifecycle and unique accounts","Partial","IAM Lead","SIM-ISO-06","MFA export and dormant-account review missing","Evidence MFA and review dormant accounts","30 days","High"),
("A.5.18","Access rights","Identity & Access","Periodic access review and removal","Planned","Application Owners","SIM-ISO-07","No completed review evidence","Run quarterly access review","45 days","High"),
("A.5.23","Cloud services security","Cloud Security","Cloud service governance and exit controls","Partial","Cloud Owner","SIM-ISO-08","Exit plan not evidenced","Document cloud risk and exit checklist","60 days","Medium"),
("A.5.24","Incident management preparation","Incident Response","Incident plan, roles and contacts","Implemented","SOC Lead","SIM-ISO-09","Sample IR plan described","Run tabletop exercise","90 days","Low"),
("A.5.25","Event assessment and decisions","Incident Response","Triage and severity criteria","Partial","SOC Lead","SIM-ISO-10","Severity matrix draft not tested","Approve and test severity matrix","45 days","Medium"),
("A.5.30","ICT readiness for continuity","Resilience","Recovery requirements and tests","Planned","IT Operations","SIM-ISO-11","No recovery test results supplied","Define RTO/RPO and test recovery","90 days","High"),
("A.5.31","Legal and contractual requirements","Compliance","Obligations register and owners","Partial","Compliance Lead","SIM-ISO-12","Review cadence unassigned","Validate obligations with Legal","60 days","Medium"),
("A.6.3","Awareness and training","People Security","Training completion tracking","Implemented","HR","SIM-ISO-13","Sample completion summary described","Track overdue staff","90 days","Low"),
("A.8.8","Technical vulnerability management","Technology","Vulnerability remediation and SLAs","Partial","IT Security","SIM-ISO-14","Remediation SLA evidence incomplete","Set severity SLAs and track exceptions","30 days","High"),
("A.8.15","Logging","Technology","Log sources and retention","Planned","SOC Lead","SIM-ISO-15","Central log coverage not demonstrated","Define sources and retention","75 days","High"),
("A.8.16","Monitoring activities","Technology","Monitoring and alert testing","Partial","SOC Lead","SIM-ISO-16","Alert test evidence missing","Test alert use cases","60 days","Medium"),
("A.8.24","Use of cryptography","Technology","Encryption and key management","Implemented","Platform Lead","SIM-ISO-17","Encryption standard described","Collect key rotation evidence","90 days","Low")]
questions=[
("Governance","Approved security policy reviewed annually?","Yes"),("Governance","Are security roles formally assigned?","Yes"),("Governance","Is a documented risk assessment process maintained?","Partial"),("Governance","Are independent security assessments performed periodically?","No"),("Governance","Are subcontractors and security obligations tracked?","Partial"),
("Access Control","Is MFA enforced for privileged and remote access?","Yes"),("Access Control","Are access rights reviewed quarterly?","Partial"),("Access Control","Are unique IDs and least privilege enforced?","Yes"),("Access Control","Are privileged accounts monitored?","Partial"),("Access Control","Are leaver accounts promptly disabled?","Yes"),
("Data Protection","Is customer data encrypted in transit?","Yes"),("Data Protection","Is customer data encrypted at rest?","Yes"),("Data Protection","Are keys protected and rotated?","Partial"),("Data Protection","Is customer data logically segregated?","Yes"),("Data Protection","Are retention and secure deletion documented?","Partial"),
("Incident Response","Is there a documented incident response plan?","Yes"),("Incident Response","Are customers notified within contract timelines?","Partial"),("Incident Response","Are annual incident exercises performed?","No"),("Incident Response","Are incidents logged and root-caused?","Yes"),("Incident Response","Is a 24/7 critical escalation path defined?","Partial"),
("Compliance","Is a current independent assurance report available?","No"),("Compliance","Are penetration tests performed annually?","Partial"),("Compliance","Are vulnerabilities remediated to defined SLAs?","Partial"),("Compliance","Are personnel checks and awareness training performed?","Yes"),("Compliance","Are privacy obligations and data requests handled?","Partial")]
def setup(ws,widths):
    ws.sheet_view.showGridLines=False; ws.freeze_panes="A2"
    for c,w in widths.items(): ws.column_dimensions[c].width=w
def head(ws,row,n):
    for cells in ws.iter_rows(min_row=row,max_row=row,min_col=1,max_col=n):
        for c in cells:
            c.font=Font(bold=True,color="FFFFFF"); c.fill=PatternFill("solid",fgColor=DARK); c.alignment=Alignment(wrap_text=True,vertical="center")
def table(ws,ref,name):
    t=Table(displayName=name,ref=ref); t.tableStyleInfo=TableStyleInfo(name="TableStyleMedium4",showRowStripes=True,showColumnStripes=False); ws.add_table(t)
def title(ws,ref,text):
    ws.merge_cells(ref); c=ws[ref.split(":")[0]]; c.value=text; c.font=Font(size=16,bold=True,color="FFFFFF"); c.fill=PatternFill("solid",fgColor=PURPLE); ws.row_dimensions[c.row].height=30

# ISO workbook
w=Workbook(); d=w.active; d.title="Dashboard"; setup(d,{"A":38,"B":28,"C":20})
title(d,"A1:C1","MINI ISO/IEC 27001:2022 COMPLIANCE PROGRAM")
for r,(a,b) in enumerate([("Organization","NovaCloud AI Solutions (fictional)"),("Scope","Laptops, identity, SaaS, cloud workloads and security operations"),("Assessment basis","Simulated portfolio exercise; evidence IDs are synthetic"),("Assessment date",date(2026,11,2))],3): d.cell(r,1,a); d.cell(r,2,b); d.cell(r,1).font=Font(bold=True,color=PURPLE)
d.append([]); d.append(["Metric","Result"]); head(d,8,2)
for r,(label,formula) in enumerate([("Controls assessed","=COUNTA('Control Register'!A2:A18)"),("Implemented",'=COUNTIF(\'Control Register\'!E2:E18,"Implemented")'),("Partial",'=COUNTIF(\'Control Register\'!E2:E18,"Partial")'),("Planned",'=COUNTIF(\'Control Register\'!E2:E18,"Planned")'),("Indicative coverage","=IFERROR((B10+0.5*B11)/B9,0)"),("High-priority actions",'=COUNTIF(\'Control Register\'!K2:K18,"High")')],9):
    d.cell(r,1,label); d.cell(r,2,formula)
d["B13"].number_format="0.0%"; d["A17"]="Coverage is a simple planning indicator, not an ISO maturity or certification score."
d.merge_cells("A17:C18"); d["A17"].alignment=Alignment(wrap_text=True)
d["A20"]="Fictional training simulation only. No real company evidence was accessed or audited."; d.merge_cells("A20:C21"); d["A20"].alignment=Alignment(wrap_text=True)
s=w.create_sheet("Control Register"); s.append(["Control ID","Control name","Theme","Assessment requirement","Current status","Owner","Evidence reference","Observation / evidence note","Gap / action","Target","Priority"])
for x in controls:s.append(x)
setup(s,{"A":13,"B":38,"C":19,"D":40,"E":18,"F":20,"G":17,"H":42,"I":43,"J":15,"K":14}); head(s,1,11); table(s,"A1:K18","ISOControls")
for r in range(2,19):
    s.row_dimensions[r].height=48
    for c in s[r]:c.alignment=Alignment(wrap_text=True,vertical="top")
dv=DataValidation(type="list",formula1='"Implemented,Partial,Planned,Not Applicable"');s.add_data_validation(dv);dv.add("E2:E18")
dv=DataValidation(type="list",formula1='"Low,Medium,High,Critical"');s.add_data_validation(dv);dv.add("K2:K18")
for status,color in [("Implemented",GREEN),("Partial",YELLOW),("Planned",RED)]:
    s.conditional_formatting.add("E2:E18",FormulaRule(formula=[f'E2="{status}"'],fill=PatternFill("solid",fgColor=color)))
a=w.create_sheet("Improvement Plan");a.append(["Action ID","Control ID","Action","Owner","Priority","Target","Status","Closure evidence"])
for i,x in enumerate(controls,1):
    if x[4]!="Implemented":a.append([f"ACT-{i:02} ",x[0],x[8],x[5],x[10],x[9],"Open","Attach genuine evidence after remediation"])
setup(a,{"A":14,"B":14,"C":54,"D":20,"E":15,"F":15,"G":18,"H":42});head(a,1,8);table(a,f"A1:H{a.max_row}","ISOActions")
dv=DataValidation(type="list",formula1='"Open,In Progress,Closed,Accepted Risk"');a.add_data_validation(dv);dv.add(f"G2:G{a.max_row}")
g=w.create_sheet("Read Me");g.append(["GUIDE"]); 
for x in ["Update status, owner, evidence, priority and dates in Control Register.","Replace SIM-ISO references with genuine dated artifacts before real-world use.","Track remediation and closure evidence in Improvement Plan.","Dashboard coverage: Implemented=1, Partial=0.5, Planned=0. This is not an ISO rating.","All scenario data is synthetic. Confirm applicability and the Statement of Applicability with qualified stakeholders."]:g.append([x])
setup(g,{"A":120});title(g,"A1:A1","WORKBOOK GUIDE")
w.calculation.fullCalcOnLoad=True;w.calculation.forceFullCalc=True;w.calculation.calcMode="auto"
w.save(P1/"ISO27001_Mini_Compliance_Program.xlsx")

# ISO report
doc=Document(); sec=doc.sections[0];sec.top_margin=Inches(.65);sec.bottom_margin=Inches(.65)
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;r=p.add_run("ISO/IEC 27001:2022 MINI COMPLIANCE PROGRAM");r.bold=True;r.font.size=Pt(18);r.font.color.rgb=RGBColor(91,44,131)
doc.add_paragraph("Portfolio simulation • 02 November 2026",style="Subtitle")
doc.add_heading("Executive summary",1);doc.add_paragraph("Fictional baseline exercise for NovaCloud AI Solutions covering laptops, identity, SaaS, cloud workloads and security operations. The register contains 17 selected controls: 4 Implemented, 8 Partial and 5 Planned. Indicative planning coverage is 47.1% (Implemented=1, Partial=0.5, Planned=0). This is not an ISO maturity score, audit opinion or certification result.")
doc.add_heading("Scope and method",1);doc.add_paragraph("Selected representative ISO/IEC 27001:2022 Annex A controls, assigned owners, recorded synthetic evidence references and observations, identified gaps, prioritized remediation and created an improvement plan.")
doc.add_heading("Priority recommendations",1)
for x in ["Approve and publish the information security policy.","Reconcile asset and SaaS inventories; assign accountable owners.","Validate MFA coverage and conduct periodic access reviews.","Define vulnerability remediation SLAs and track exceptions.","Approve incident severity criteria and test response procedures.","Define RTO/RPO and execute recovery tests."]:doc.add_paragraph(x,style="List Number")
doc.add_heading("Evidence limitations",1);doc.add_paragraph("All SIM-ISO references and observations are fictional training inputs. No actual documents, logs, configurations, interviews or system exports were inspected. Replace all simulated references with genuine evidence before presenting this as a real assessment.")
doc.add_heading("Disclaimer",1);doc.add_paragraph("Training portfolio simulation only; not client work, an external audit, legal advice or ISO certification.")
doc.save(P1/"Management_Compliance_Summary.docx")

# Vendor workbook
v=Workbook();d=v.active;d.title="Vendor Scorecard";setup(d,{"A":38,"B":30})
title(d,"A1:C1","THIRD-PARTY VENDOR SECURITY ASSESSMENT")
for r,(a,b) in enumerate([("Vendor","Northstar Cloud Services (fictional)"),("Service","Hypothetical SaaS handling business contact and operational data"),("Assessment date",date(2026,11,2)),("Basis","Simulated questionnaire and evidence references")],3):d.cell(r,1,a);d.cell(r,2,b);d.cell(r,1).font=Font(bold=True,color=PURPLE)
d.append([]);d.append(["Metric","Result"]);head(d,8,2)
for r,(lab,formula) in enumerate([("Questions assessed","=COUNTA(Questionnaire!A2:A26)"),("Yes","=COUNTIF(Questionnaire!C2:C26,\"Yes\")"),("Partial","=COUNTIF(Questionnaire!C2:C26,\"Partial\")"),("No","=COUNTIF(Questionnaire!C2:C26,\"No\")"),("Weighted score","=IFERROR(SUM(Questionnaire!D2:D26)/(2*B9),0)"),("Risk tier",'=IF(B13>=0.85,"Low",IF(B13>=0.65,"Moderate",IF(B13>=0.45,"High","Critical")))')],9):d.cell(r,1,lab);d.cell(r,2,formula)
d["B13"].number_format="0.0%";d["A17"]="Scoring: Yes=2, Partial=1, No=0. Risk: Low ≥85%, Moderate ≥65%, High ≥45%, Critical <45%.";d.merge_cells("A17:C18");d["A17"].alignment=Alignment(wrap_text=True)
d["A20"]="Simulation only. Do not approve a real supplier based on this score; validate primary evidence and contracts.";d.merge_cells("A20:C21");d["A20"].alignment=Alignment(wrap_text=True)
q=v.create_sheet("Questionnaire");q.append(["Domain","Question","Response","Score","Evidence ref","Evidence note","Follow-up"])
for i,(domain,question,response) in enumerate(questions,1):q.append([domain,question,response,f'=IF(C{i+1}="Yes",2,IF(C{i+1}="Partial",1,0))',f"SIM-VEN-{i:02}", "Simulated vendor response; primary evidence not inspected","Request dated primary evidence"])
setup(q,{"A":19,"B":60,"C":16,"D":12,"E":16,"F":43,"G":40});head(q,1,7);table(q,"A1:G26","VendorQuestions")
for r in range(2,27):q.row_dimensions[r].height=42
dv=DataValidation(type="list",formula1='"Yes,Partial,No,Not Applicable"');q.add_data_validation(dv);dv.add("C2:C26")
for status,color in [("Yes",GREEN),("Partial",YELLOW),("No",RED)]:q.conditional_formatting.add("C2:C26",FormulaRule(formula=[f'C2="{status}"'],fill=PatternFill("solid",fgColor=color)))
f=v.create_sheet("Findings & Actions");f.append(["ID","Domain","Finding / evidence gap","Risk","Recommended action","Owner","Target","Status"])
findings=[
("VR-01","Governance","No independent security report supplied","High","Obtain current SOC 2 Type II or ISO certificate; validate scope and exceptions","Vendor Security","30 days","Open"),
("VR-02","Governance","Subprocessor oversight evidence incomplete","Medium","Obtain current subprocessor list and contractual flow-down clauses","Legal / Procurement","45 days","Open"),
("VR-03","Access","Access review and privileged monitoring evidence incomplete","High","Obtain signed access review and privileged activity samples","Vendor IAM","30 days","Open"),
("VR-04","Data Protection","Key rotation and secure deletion evidence incomplete","High","Review rotation records and deletion certificate sample","Vendor DPO","30 days","Open"),
("VR-05","Incident Response","No annual incident exercise report supplied","Medium","Request exercise report and validate notification commitments","Vendor CISO","45 days","Open"),
("VR-06","Compliance","No current independent assurance report supplied","High","Request current assurance report and bridge letter if applicable","Vendor Compliance","30 days","Open"),
("VR-07","Compliance","Pen-test summary and remediation metrics missing","High","Obtain recent test scope, summary and remediation proof","Vendor Security","30 days","Open")]
for x in findings:f.append(x)
setup(f,{"A":12,"B":20,"C":48,"D":15,"E":52,"F":20,"G":15,"H":16});head(f,1,8);table(f,"A1:H8","VendorFindings")
dv=DataValidation(type="list",formula1='"Open,In Progress,Closed,Accepted Risk"');f.add_data_validation(dv);dv.add("H2:H8")
g=v.create_sheet("Read Me");g.append(["GUIDE"])
for x in ["Change Questionnaire responses using dropdowns; scores and tier recalculate.","Yes=2, Partial=1, No=0. Score=earned points/(2×25).","Replace SIM-VEN references with real dated documents, exports, reports or contract clauses.","Update Findings & Actions with owners, due dates, status and closure evidence.","All vendor responses and evidence are synthetic; no actual vendor material was reviewed. Not a real supplier rating or approval."]:g.append([x])
setup(g,{"A":120});title(g,"A1:A1","WORKBOOK GUIDE")
v.calculation.fullCalcOnLoad=True;v.calculation.forceFullCalc=True;v.calculation.calcMode="auto"
v.save(P2/"Third_Party_Vendor_Risk_Assessment.xlsx")

# Vendor report
doc=Document();sec=doc.sections[0];sec.top_margin=Inches(.65);sec.bottom_margin=Inches(.65)
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;r=p.add_run("THIRD-PARTY VENDOR RISK ASSESSMENT");r.bold=True;r.font.size=Pt(18);r.font.color.rgb=RGBColor(91,44,131)
doc.add_paragraph("Portfolio simulation • 02 November 2026",style="Subtitle")
doc.add_heading("Executive summary",1);doc.add_paragraph("Fictional desk-based assessment of Northstar Cloud Services across Governance, Access Control, Data Protection, Incident Response and Compliance. Sample responses: 11 Yes, 11 Partial and 3 No; score 33/50 (66.0%), corresponding to the illustrative Moderate tier. This is not a verified supplier rating or approval.")
doc.add_heading("Scoring",1);doc.add_paragraph("Yes=2, Partial=1, No=0. Weighted score=earned points divided by 50. Low ≥85%, Moderate ≥65%, High ≥45%, Critical <45%.")
doc.add_heading("Key findings",1)
for x in findings:doc.add_paragraph(f"{x[0]} — {x[2]} Risk: {x[3]}. Action: {x[4]}")
doc.add_heading("Due diligence before onboarding",1)
for x in ["Request a current SOC 2 Type II report or ISO certificate and validate scope, validity and exceptions.","Obtain penetration-test scope, executive summary and remediation evidence.","Review executed DPA, breach notification terms, data residency and subprocessors.","Validate MFA, privileged access, access reviews, encryption, key management and deletion.","Review incident exercises, business continuity and recovery test results.","Obtain documented risk-owner approval from Procurement, Legal, Privacy, IT Security and the business."]:doc.add_paragraph(x,style="List Number")
doc.add_heading("Evidence limitations and disclaimer",1);doc.add_paragraph("All responses and SIM-VEN evidence references are fictional. No actual vendor portal, policy, SOC report, certificate, penetration test, contract or configuration was accessed or verified. Training simulation only; not an actual vendor assessment, client engagement, procurement approval or legal advice.")
doc.save(P2/"Vendor_Assessment_Report.docx")

# Package validation
for p in [P1/"ISO27001_Mini_Compliance_Program.xlsx",P2/"Third_Party_Vendor_Risk_Assessment.xlsx",P1/"Management_Compliance_Summary.docx",P2/"Vendor_Assessment_Report.docx"]:
    with zipfile.ZipFile(p) as z: assert z.testzip() is None
load_workbook(P1/"ISO27001_Mini_Compliance_Program.xlsx")
load_workbook(P2/"Third_Party_Vendor_Risk_Assessment.xlsx")
Document(P1/"Management_Compliance_Summary.docx");Document(P2/"Vendor_Assessment_Report.docx")
print("Generated and package-validated all four GRC deliverables.")
