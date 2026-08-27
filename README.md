# Software Engineering Lab 1 – Requirements Engineering & UML Use-Case Modelling

## Scenario #53 – Freelance Content Creator Escrow Platform

This repository contains the completed deliverables for **Software Engineering Lab 1** based on Problem Statement #53.

### Scenario Overview

The system is a freelance contract management and escrow platform that allows content creators and sponsors to define deliverable milestones, submit and review watermarked draft media assets, and release secure milestone payments after sponsor approval.

### Actors

- **Content Creator** – Submits deliverables and receives milestone payments.
- **Client Sponsor** – Reviews submitted deliverables and approves or rejects milestones.
- **Escrow / Payment Service** – Handles the release of locked milestone payments after valid approval.

## Deliverables

### 1. Requirements Table

**File:** `SE_Lab1_Scenario53_Requirements_Table.xlsx`

Contains exactly:

- 5 Functional Requirements: FR-001 to FR-005
- 2 Non-Functional Requirements: NFR-001 to NFR-002
- Requirement ID
- Requirement Type
- Description
- Priority
- Acceptance Criteria
- Rationale

The requirements focus on deliverable submission, watermarking, client review, milestone approval/rejection, and secure payment release.

### 2. UML Use-Case Diagram

**File:** `SE_Lab1_Scenario53_UML_Use_Case_Diagram.pdf`

The diagram contains:

- All identified actors
- Primary system use cases
- System boundary
- Actor associations
- `«include»` relationship
- `«extend»` relationship

Key relationships include:

- **Submit Deliverable** `«include»` **Apply Watermark**
- **Request Revision** `«extend»` **Review Deliverable**

### 3. Use-Case Flow Specification

**File:** `SE_Lab1_Scenario53_Use_Case_Flow.pdf`

The selected core use case is:

**Approve Milestone and Release Payment**

The document includes:

- Actors
- Preconditions
- Main Success Scenario
- Postconditions
- Alternate Flow for deliverable rejection and revision

## Repository Structure

```text
SE-Lab-1/
│
├── README.md
├── SE_Lab1_Scenario53_Requirements_Table.xlsx
├── SE_Lab1_Scenario53_UML_Use_Case_Diagram.pdf
└── SE_Lab1_Scenario53_Use_Case_Flow.pdf
```

## Submission

All three deliverables should be pushed to the **Lab-1 GitHub repository** as required by the Software Engineering Lab handout.

## Tools Used

- Microsoft Excel / compatible spreadsheet software – Requirements Table
- Draw.io / UML diagramming tool – Use-Case Diagram
- PDF export – Diagram and Use-Case Flow documents

## Reference

**Problem Statement #53 – Freelance Content Creator Escrow Platform**

The problem statement requires exactly 5 Functional Requirements, 2 Non-Functional Requirements, a UML Use-Case Diagram containing actors and primary use cases with at least one `«include»` and one `«extend»` relationship, and a one-page Use-Case Flow Specification.
