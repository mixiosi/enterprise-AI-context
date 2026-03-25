# Workflow C: Enterprise Safety Onboarding Automation

This workflow emulates an AI-driven automation flow for an Enterprise Safety Manager. It demonstrates how an AI model can autonomously monitor communications (like emails), identify when a new person is coming to a job site for the first time, and proactively handle the administrative overhead.

## The Problem
When subcontractors or new personnel arrive on site without prior notice, the Safety Manager has to scramble to get them through safety orientation and find the correct Personal Protective Equipment (PPE). This causes delays, non-compliance risks, and frustration.

## The AI Solution
By integrating an AI Agent into the corporate email stream, the system can:
1. **Contextually Read Emails:** The AI scans emails and understands that "John from Apex Electric is coming next Tuesday" means a site visit is scheduled.
2. **Database Cross-Referencing:** It checks the `site_roster` database. If John isn't listed, it knows he is a "New Visitor".
3. **Automated Scheduling:** It automatically finds an open slot in the `orientation_schedule` database and books John for a safety class.
4. **Inventory Validation:** It checks the `ppe_inventory` database to ensure a hardhat, high-vis vest, safety glasses, and the correctly sized steel-toe boots are in stock.
5. **Proactive Alerting:** It drafts a comprehensive "Heads Up" email to the Safety Manager outlining exactly who is arriving, when their orientation is booked, and if any PPE needs to be ordered.
6. **Exception Handling:** If the email didn't mention John's shoe size, the AI flags this to the Safety Manager and drafts a follow-up email requesting the missing information.

## How to Run the Demonstration

1. **Setup the Mock Databases:**
   Run the setup script to create the local `site_safety.db` SQLite database populated with mock personnel, inventory, and class schedules.
   ```bash
   python setup_db.py
   ```

2. **Execute the AI Agent Workflow:**
   Run the orchestrator script to see the AI process three distinct incoming emails (a perfect run, a run missing data, and a run where inventory is out of stock).
   ```bash
   python safety_agent.py
   ```
   *Watch the terminal output as the AI breaks down its reasoning, queries the databases, and generates the final alerts.*
