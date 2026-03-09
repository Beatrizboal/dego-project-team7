# dego-project-team7
DEGO Course Project — Team 7

# DEGO Project – Team 7

**Course:** Data Ecosystems and Governance in Organizations (DEGO 2606) — Nova SBE
**Project:** NovaCred Credit Application Audit
**Dataset:** 502 synthetic credit applications (`raw_credit_applications.json`)

---

## Team Members & Roles

| Name | Role | Primary Notebook |
|---|---|---|
| Beatriz Boal | Data Engineer | `01-data-quality.ipynb` |
| Miguel Rodrigues | Data Scientist | `02-bias-analysis.ipynb` |
| Martin Schmitz | Governance Officer | `03-privacy-demo.ipynb` |

---

## Project Description

This project analyzes a synthetic credit application dataset used by **NovaCred**, a fintech startup that applies machine learning models to approve or reject loan applications.

Following a regulatory inquiry regarding potential discrimination in lending practices, our team performed a **data governance audit** of the dataset. The audit evaluates:

- Data quality issues
- Algorithmic bias in credit decisions
- Privacy and governance risks
- Compliance with **GDPR** and the **EU AI Act**

The goal of the project is to demonstrate how **data governance controls can mitigate ethical, legal, and operational risks in AI-driven financial systems**.

---

## Repository Structure

```
dego-project-team7/
├── README.md                        # This document — executive summary
├── data/
│   ├── raw/
│   │   └── raw_credit_applications.json   # Original dataset (502 records)
│   └── processed/
│       └── clean_credit_applications.csv  # Cleaned output from 01-data-quality
├── notebooks/
│   ├── 01-data-quality.ipynb        # Data loading, cleaning, quality audit
│   ├── 02-bias-analysis.ipynb       # Bias detection, fairness metrics, DI ratio
│   └── 03-privacy-demo.ipynb        # PII identification, pseudonymisation, GDPR mapping, governance
├── src/
│   └── __init__.py
├── reports/                         # Visual outputs and analysis artifacts 
│   └── pii_risk_coverage.png        # PII field coverage visualisation
└── presentation/                    # Final project presentation
```

---

## Executive Summary

NovaCred is a fintech startup using machine learning to make credit decisions. Following a regulatory inquiry, our team was engaged as a Data Governance Task Force to audit the raw credit application dataset for data quality issues, algorithmic bias, and privacy and governance compliance gaps.

**The audit uncovered critical failures across all three dimensions:**

- **Data quality:** Multiple data quality issues identified including duplicates, type inconsistencies, missing values, and invalid entries across the 502-record dataset
- **Algorithmic bias:** A Disparate Impact ratio of **0.77** for gender (below the 0.80 four-fifths rule threshold), indicating statistically significant potential discrimination against female applicants
- **Privacy & governance:** 496 Social Security Numbers stored in plaintext, no consent documentation, no data retention policy, fully automated credit decisions with no human oversight — all constituting critical GDPR and EU AI Act violations

**The system cannot be legally deployed in the EU in its current state.** Immediate remediation is required before the next lending cycle.

---

## Key Metrics

| Metric | Result |
|------|------|
| Total credit applications | 500 |
| Dataset columns after processing | 34 |
| Plaintext SSNs detected | 496 |
| Disparate Impact ratio (gender) | 0.77 |
| Records overdue for deletion | 203 |

---

## 1. Data Quality Findings

> *Primary analysis: [`notebooks/01-data-quality.ipynb`](notebooks/01-data-quality.ipynb)*
> *Role: Beatriz Boal, Data Engineer*

The raw dataset contained **502 application records** in nested JSON format.  

**Issues identified across 5 quality dimensions:**

| Dimension | Issue |
|---|---|
| Completeness | Missing values across key fields |
| Consistency | Inconsistent gender encoding (e.g., "M" / "Male" and "F" / "Female"), different date formats and iconsistent schema (`financials.annual_income` and `financials.annual_salary`)
| Validity | Data type mismatches and invalid values (e.g., negative credit history months)
| Accuracy | Business rule validation required for financial attributes
| Uniqueness | Duplicate application records (app_001 and app_042)

**Data Engineering Pipeline:**

The nested JSON dataset was processed through the following pipeline:
Key processing steps included:
- Standardizing missing values and categorical encodings  
- Consolidating duplicated schema fields  
- Converting variables to appropriate data types  
- Removing duplicate applications and correcting implausible values  
- Transforming nested spending data into tabular features  
- Exporting the cleaned dataset to the processed data directory

**Cleaned output:** `data/processed/clean_credit_applications.csv` — 500 records, 34 columns.

---

## 2. Bias Detection & Fairness

> *Primary analysis: [`notebooks/02-bias-analysis.ipynb`](notebooks/02-bias-analysis.ipynb)*
> *Role: Miguel Rodrigues, Data Scientist*

<!-- Data Scientist: please fill in full bias findings below -->

**Disparate Impact Ratio (Gender) — Four-Fifths Rule**

| Group | Approval Rate |
|---|---|
| Male (privileged) | **51%** |
| Female (unprivileged) | **66%** |
| **DI Ratio (Female / Male)** | **0.77** |

A DI ratio of **0.77 is below the 0.80 threshold**, indicating potential disparate impact against female applicants under the four-fifths rule. NovaCred's lending model may constitute unlawful discrimination under GDPR Article 22 and EU AI Act Article 10 requirements for unbiased training data.

**Additional bias patterns identified:**

- Proxy discrimination risk: `zip_code` is strongly associated with gender (χ² p < 0.001) but not with loan approval outcomes, indicating it is not currently acting as a proxy in decisions, though it should be monitored.

- Age-related patterns: approval rates increase with age, and younger applicants are approved less frequently. However, regression analysis suggests this pattern is largely explained by financial factors correlated with age (e.g., credit history and income).

- Interaction effects (age × gender): no statistically significant interaction was found, indicating that the gender approval gap is consistent across age groups.

---

## 3. Privacy Assessment

> *Primary analysis: [`notebooks/03-privacy-demo.ipynb`](notebooks/03-privacy-demo.ipynb)*
> *Role: Martin Schmitz, Governance Officer*

### 3.1 PII Identified

Ten fields were classified as personal data under GDPR Article 4(1), spanning three risk tiers:

| Tier | Fields | Risk |
|---|---|---|
| Direct Identifiers | `full_name`, `email`, `ssn`, `ip_address`, `date_of_birth` | Critical / High |
| Quasi-Identifiers | `zip_code`, `gender` | High |
| Sensitive Behavioral | `spend_gambling`, `spend_adult_entertainment`, `spend_alcohol` | High / Medium |

**Critical finding:** All 496 populated SSN records are stored in standard plaintext format (`XXX-XX-XXXX`) with no hashing, encryption, or tokenisation applied. This constitutes a high-severity breach risk requiring mandatory supervisory authority notification under GDPR Article 33 if exposed.

### 3.2 Pseudonymisation Demonstrated

Four privacy-preserving transformations were demonstrated in the notebook, distinguishing between pseudonymisation (still personal data under GDPR Recital 26) and anonymisation (outside GDPR scope):

| Field | Technique | Reversibility | GDPR Status |
|---|---|---|---|
| `ssn` | SHA-256 hashing | Irreversible without original | Pseudonymisation |
| `full_name` | Token lookup (`Applicant_001`) | Reversible via lookup table | Pseudonymisation |
| `date_of_birth` | Generalised to birth year | Not reversible to exact date | Approaches anonymisation |
| `zip_code` | Truncated to 3-digit prefix | Not reversible to exact code | Reduces re-identification risk |

**Utility preserved:** After pseudonymisation, the Disparate Impact ratio (0.77) is reproducible identically — bias analysis is fully functional on the safe dataset.

---

## 4. GDPR & AI Act Compliance Mapping

> *Full analysis: [Section 4 of `03-privacy-demo.ipynb`](notebooks/03-privacy-demo.ipynb)*

Findings were mapped to six GDPR articles and the EU AI Act. Every article examined revealed a compliance gap:

| Article | Requirement | Gap | Severity |
|---|---|---|---|
| Art. 5(1)(a) | Documented lawful basis | 0 consent or basis fields in dataset | High |
| Art. 5(1)(c) | Data minimisation | 6 excess fields incl. `spend_adult_entertainment` | High |
| Art. 5(1)(e) | Storage limitation | No retention metadata; PII retained indefinitely | High |
| Art. 22 | Human oversight of automated decisions | 500 decisions fully automated; 0 oversight fields | **Critical** |
| Art. 33 | Breach notification within 72 hours | 496 plaintext SSNs = immediate mandatory notification if breached | **Critical** |
| Art. 17 | Right to erasure | No DSR workflow or cross-system deletion mechanism | Medium |
| EU AI Act Annex III | High-risk AI conformity assessment | 16 compliance indicator fields missing; no conformity assessment | **Critical** |

**EU AI Act classification:** NovaCred's credit scoring system is **High-Risk AI** under Annex III Category 5(b). Deployment without a completed conformity assessment (Art. 43) and human oversight (Art. 14) is a regulatory violation.

---

## 5. Governance Recommendations

> *Full implementation: [Section 5 of `03-privacy-demo.ipynb`](notebooks/03-privacy-demo.ipynb)*

Five controls were implemented with working code, each directly addressing a gap from Section 4:

### 5.1 Safe Analytical Dataset (Critical — implement immediately)
Apply the Section 5.2 pipeline before distributing any data to analysts. The pipeline pseudonymises SSNs and names, generalises quasi-identifiers, and drops 7 excess fields — reducing plaintext PII field-records from **2,480 to 0**.

### 5.2 Consent Tracking (Critical)
Add four fields to every application record: `consent_timestamp`, `lawful_basis_credit`, `lawful_basis_fraud`, `consent_behavioral`. Records without behavioral consent (~15% in simulation) must have spending sub-categories nullified. Implement a withdrawal endpoint.

### 5.3 Data Retention Policy (High)
Add `application_date` and `retention_until` to the schema. Apply the following schedule:

| Category | Retention | Trigger |
|---|---|---|
| Rejected application PII | 30 days | Rejection notification sent |
| Approved application PII | Loan term + 5 years | Loan fully repaid |
| Behavioral spending data | Decision date only | Decision logged |
| Audit logs | 7 years | EU AI Act Art. 12 |

Based on the simulated dataset, **203 records are already overdue for deletion.**

### 5.4 Decision Audit Trail (Critical)
Implement an append-only audit log capturing four event types per application: `APPLICATION_RECEIVED`, `MODEL_SCORED`, `HUMAN_REVIEWED` (where applicable), `DECISION_ISSUED`. Each event records `event_id`, `event_timestamp`, `model_version`, `model_score`, `human_reviewed`, `reviewer_id`, and `final_outcome`. Retain for 7 years per EU AI Act Art. 12.

### 5.5 Human Oversight Framework (Critical)
Deploy a tiered review model based on model score:

| Score | Tier | Decision Path |
|---|---|---|
| ≥ 0.70 | Low risk | Auto-approve; 5% sampled audit review |
| 0.40 – 0.69 | Medium risk | **Mandatory human review before decision** |
| < 0.40 | High risk | Auto-decline with explanation; review on request |

Under this model, **252 of 500 applications (50.4%) require human review** — ensuring Art. 22 compliance for the highest-risk decisions.

### 5.6 Governance Scorecard (Ongoing)
A 10-control scorecard was implemented to track compliance against the accountability principle (Art. 5(2)). NovaCred's current overall compliance score is **6%**. Monthly DPO review is recommended, with a quarterly report to senior management.

---

## How to Run

```bash
# Clone the repository
git clone https://github.com/your-org/dego-project-team7.git
cd dego-project-team7

# Install dependencies
pip install pandas numpy matplotlib seaborn

# Run notebooks in order
jupyter notebook notebooks/01-data-quality.ipynb
jupyter notebook notebooks/02-bias-analysis.ipynb
jupyter notebook notebooks/03-privacy-demo.ipynb
```

All notebooks load data from `data/processed/clean_credit_applications.csv`. Run `01-data-quality.ipynb` first to generate this file from the raw JSON.

---

## Video Presentation

<!-- Add YouTube unlisted link or Google Drive link here before submission -->

---

## Individual Contributions

| Name | Contributions |
|---|---|
| Beatriz Boal | Data pipeline, cleaning logic, quality audit (`01-data-quality.ipynb`), repository structure |
| Miguel Rodrigues | Bias analysis, DI ratio calculation, fairness metrics, proxy discrimination analysis (`02-bias-analysis.ipynb`) |
| Martin Schmitz | PII identification, pseudonymisation demonstration, GDPR compliance mapping, governance recommendations (`03-privacy-demo.ipynb`), README |
