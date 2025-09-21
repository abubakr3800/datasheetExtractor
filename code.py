import pdfplumber
import re
import pandas as pd
import json

# Define important fields
FIELDS = ["Model", "Power_W", "LuminousFlux_lm", "CCT_K", "CRI",
          "Efficiency_lm_W", "IP_Rating", "Dimensions_mm", 
          "Material", "Driver"]

def extract_from_text(text):
    data = {}
    # Simple regex-based extraction (expandable with ML later)
    data["Model"] = re.search(r"Model[:\s]+([\w\- ]+)", text, re.I)
    data["Power_W"] = re.search(r"(\d+)\s*W", text, re.I)
    data["LuminousFlux_lm"] = re.search(r"(\d+)\s*lm", text, re.I)
    data["CCT_K"] = re.search(r"(\d+)\s*K", text, re.I)
    data["CRI"] = re.search(r"CRI[:\s]+(\d+)", text, re.I)
    data["Efficiency_lm_W"] = re.search(r"(\d+)\s*lm/W", text, re.I)
    data["IP_Rating"] = re.search(r"(IP\d{2})", text, re.I)
    data["Dimensions_mm"] = re.search(r"(\d+\s*[xØ]\s*\d+)", text, re.I)
    data["Material"] = re.search(r"Material[:\s]+([\w ,]+)", text, re.I)
    data["Driver"] = re.search(r"Driver[:\s]+([\w ,]+)", text, re.I)

    # Normalize
    result = {}
    for f in FIELDS:
        result[f] = data[f].group(1) if data[f] else "NA"
    return result

def process_pdf(path):
    with pdfplumber.open(path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return extract_from_text(text)

# Example run
fixture = process_pdf("sample_datasheet.pdf")

# Save JSON
with open("output.json", "w") as f:
    json.dump(fixture, f, indent=4)

# Save CSV
df = pd.DataFrame([fixture])
df.to_csv("output.csv", index=False)
