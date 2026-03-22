# EnterpriseAI: Technical Architecture Diagram

This document illustrates the data flow and technology stack powering the EnterpriseAI infrastructure. The architecture is designed to keep proprietary data localized while leveraging advanced language models for orchestration and reasoning.

## Full System Data Flow

The following diagram uses Mermaid syntax (supported natively by GitHub) to visualize how the three core workflows interact with the centralized AI Orchestrator.

```mermaid
graph TD
    %% Define User and Interface
    User([Site Engineer / Project Manager])
    UI[Client Interface]
    
    User -->|1. Natural Language Query| UI
    
    %% The LLM Orchestrator
    subgraph The AI Orchestrator
        SystemPrompt[System Prompts & Guardrails]
        LLM{Large Language Model}
        SystemPrompt -.->|Enforces Compliance| LLM
    end
    
    UI -->|2. Orchestration Request| LLM
    
    %% Workflow A: RAG
    subgraph Workflow A: Document Intelligence RAG
        Docs[PDF Specs, Blueprints, Manuals]
        TextSplit[Text Splitter]
        Embed[Embedding Model: all-MiniLM-L6-v2]
        VDB[(Local ChromaDB Vector Store)]
        
        Docs -->|Ingestion| TextSplit
        TextSplit -->|Chunks| Embed
        Embed -->|Vectors| VDB
        
        LLM -->|3a. Semantic Search| VDB
        VDB -->|Top-K Context Chunks| LLM
    end
    
    %% Workflow B: MCP
    subgraph Workflow B: Financial Guardrails
        MCP[FastMCP Server]
        ERP[(SQLite ERP Database)]
        
        LLM -->|3b. Tool Call JSON-RPC| MCP
        MCP -->|SQL Query| ERP
        ERP -->|Budget Remaining| MCP
        MCP -->|Validation Status| LLM
    end
    
    %% Workflow C: Edge AI
    subgraph Workflow C: Edge Safety
        Camera[Edge Camera Feed]
        YOLO[YOLOv8 Vision Model]
        Alerts[Compliance Subsystem]
        
        Camera -->|Frames| YOLO
        YOLO -->|PPE Detection Metrics| Alerts
        Alerts -.->|Aggregated Alerts| LLM
    end

    %% Final Response
    LLM -->|4. Synthesized Answer with Citations & Audits| UI
    UI -->|Result| User

    classDef database fill:#f9f,stroke:#333,stroke-width:2px;
    classDef llm fill:#bbf,stroke:#333,stroke-width:2px;
    classDef edge fill:#bfb,stroke:#333,stroke-width:2px;
    
    class VDB,ERP database;
    class LLM llm;
    class YOLO edge;
```

## Component Breakdown

1. **The AI Orchestrator (The Brain):** The Large Language Model acts as the reasoning engine. It does not store factual data in its weights; instead, it is restricted by strict system prompts (the "Penthouse Rules") to only answer based on the context provided to it.
2. **Retrieval-Augmented Generation (RAG):** When asked about specifications, the Orchestrator queries the local ChromaDB. The mathematical embedding model runs entirely on local CPUs, ensuring that massive, proprietary PDF blueprints never leave the secure network.
3. **Model Context Protocol (MCP):** When asked to approve financial invoices, the Orchestrator cannot guess. It utilizes MCP to execute a secure, predefined tool call that queries the ERP database. This enforces "least privilege" access, allowing the AI to read the budget without giving it direct SQL write access.
4. **Edge AI Monitoring:** Computer vision runs on localized hardware near the cameras. Instead of streaming gigabytes of video to the cloud for analysis, the YOLO model processes frames on the edge and only sends lightweight text alerts (e.g., "Hardhat violation detected") back to the central system.
