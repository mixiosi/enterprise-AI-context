from fpdf import FPDF
import os

# Create directory for mock documents if it doesn't exist
os.makedirs("mock_documents", exist_ok=True)

class PDF(FPDF):
    def header(self):
        self.set_font("helvetica", "B", 12)
        self.cell(0, 10, "CONFIDENTIAL - High-Performance Computing Data Center Specification", border=False, ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")

# Document 1: Cooling Systems & HVAC
pdf1 = PDF()
pdf1.add_page()
pdf1.set_font("helvetica", size=11)

content1 = """
Section 4: Data Center Cooling Systems and HVAC Regulations

4.1 Primary Cooling Loop (PCL)
The Primary Cooling Loop (PCL) is responsible for regulating the temperature of the core server racks. 
The minimum required pipe thickness for the primary cooling loop is 0.25 inches (Schedule 40). 
All joints must be TIG welded and pressure tested to 150 PSI.

4.2 Secondary Cooling Loop (SCL)
The Secondary Cooling Loop (SCL) handles the heat exchange with the exterior environment. 
According to recent architectural revisions, the required pipe thickness for the secondary cooling loop is exactly 0.375 inches (Schedule 80) to accommodate higher pressure thresholds during peak summer loads.

4.3 OSHA Standard Compliance - Refrigerant Handling
OSHA Standard 1910.119 (Process Safety Management of Highly Hazardous Chemicals) mandates that all personnel handling R-410A or similar refrigerants must wear Level B PPE. 
In the event of a leak, automated ventilation systems must activate within 3.5 seconds, exchanging the room air volume at a rate of 12 ACH (Air Changes per Hour). Cost-saving measures that delay sensor activation are strictly prohibited and violate OSHA standards.
"""
pdf1.multi_cell(0, 6, content1)
pdf1.output("mock_documents/HPC_Cooling_Specs_v2.pdf")

# Document 2: Structural Integrity
pdf2 = PDF()
pdf2.add_page()
pdf2.set_font("helvetica", size=11)

content2 = """
Section 7: Structural Integrity and Load-Bearing Specifications

7.1 Raised Floor Infrastructure
To support the density of the new AI-cluster racks, the raised floor infrastructure must maintain a structural integrity rating of at least 3,500 lbs per square foot (PSF). 
The pedestal support grid must be anchored using 0.5-inch titanium bolts to prevent lateral shifting during seismic events.

7.2 Roof Load Limits for Cooling Towers
The installation of the external cooling towers requires significant structural reinforcement of the roof. 
The maximum allowable dead load for the reinforced roof section is 15,000 lbs. 
OSHA Standard 1926.501 (Fall Protection) dictates that guardrail systems must be erected around the entire perimeter of the cooling tower installation zone, measuring no less than 42 inches in height.

7.3 Emergency Exits and Pathways
All emergency pathways must remain unobstructed. The structural integrity of the fire-rated walls separating the server halls from the administrative sections must provide a minimum of 4 hours of fire resistance.
"""
pdf2.multi_cell(0, 6, content2)
pdf2.output("mock_documents/HPC_Structural_Integrity_v1.pdf")

print("Mock PDFs generated successfully in the 'mock_documents' folder.")
