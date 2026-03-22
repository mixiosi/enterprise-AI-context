# Enterprise AI Infrastructure

## The Objective
This repository serves as a localized, secure implementation of a production-grade enterprise AI environment for HPC Data Center Construction. It demonstrates that AI can operate safely using structured context and secure integrations without exposing highly classified internal data.

## Part 1: Architectural Framework (Enterprise Context Management)
Located in `context_management/architecture.py`, this demonstrates the **"AI Context Skyscraper"**:
1. **The Penthouse:** System Prompts & Guardrails (Non-negotiable compliance rules, e.g., "Never expose PII").
2. **The Executive Suite:** Subsystem Prompts (Role-specific instructions).
3. **The Middle Floors:** Results & Explainability (Immutable audit logs).
4. **The Lower Floors:** Retrieved Context (Active RAG layer).

We utilize the **Model Context Protocol (MCP)** to enforce "least privilege" access, connecting the AI to local databases via standardized JSON-RPC rather than brittle glue code.

---

## Part 2: Integrated Workflows

### Workflow A: Construction RFI & Blueprint RAG Pipeline
*   **Path:** `workflow_a_rfi_rag/app.py`
*   **Goal:** Reduce 180-minute manual document searches to 10-20 minutes.
*   **Tech Stack:** Streamlit, LangChain, ChromaDB, PyPDF.
*   **How to run:** 
    ```bash
    streamlit run workflow_a_rfi_rag/app.py
    ```

### Workflow B: CapEx Invoice Reconciliation Engine (MCP Server)
*   **Path:** `workflow_b_capex_reconciliation/`
*   **Goal:** Cross-reference incoming subcontractor invoices against a master project budget to prevent revenue leakage using MCP.
*   **Setup Data:** First, run the synthetic data generator to create 500 fake invoices and the ERP database.
    ```bash
    python workflow_b_capex_reconciliation/generate_data.py
    ```
*   **Run Server:** Expose the tools to an AI client (like Claude Desktop) using FastMCP.
    ```bash
    python workflow_b_capex_reconciliation/mcp_server.py
    ```

### Workflow C: Edge AI Safety Monitoring (Computer Vision)
*   **Path:** `workflow_c_edge_safety/yolo_monitor.py`
*   **Goal:** Simulate real-time compliance tracking to detect PPE violations using computer vision.
*   **Tech Stack:** Python, Ultralytics YOLOv8, OpenCV.
*   **How to run:** (Place a `sample_construction.jpg` in the folder first, then run:)
    ```bash
    python workflow_c_edge_safety/yolo_monitor.py
    ```

## Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
