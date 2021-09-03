import json
import numpy as np
import pandas as pd
import requests

API_URL = "https://api-inference.huggingface.co/models/limivan/bert-esg"
url = "https://huggingface.co/limivan/bert-esg"
API_TOKEN = "api_NyUsmLJdCTDdyjRIKxaSEigKVGRWZYRoIL"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))


output = query(
    """In fiscal year 2019, we reduced our comprehensive carbon footprint for the fourth
consecutive year—down 35 percent compared to 2015, when Apple’s carbon emissions
peaked, even as net revenue increased by 11 percent over that same period. In the past
year, we avoided over 10 million metric tons from our emissions reduction initiatives—like
our Supplier Clean Energy Program, which lowered our footprint by 4.4 million metric tons.

"""
)

factors = [
    "business_ethics",
    "data_security",
    "access_and_affordability",
    "business_model_resilience",
    "competitive_behavior",
    "critical_incident_risk_management",
    "customer_welfare",
    "director_removal",
    "employee_engagement_inclusion_and_diversity",
    "employee_health_and_safety",
    "human_rights_and_community_relations",
    "labor_practices",
    "management_of_legal_and_regulatory_framework",
    "physical_impacts_of_climate_change",
    "product_quality_and_safety",
    "product_design_and_lifecycle_management",
    "selling_practices_and_product_labeling",
    "supply_chain_management",
    "systemic_chain_management",
    "waste_and_hazardous_materials_management",
    "water_and_wastewater_management",
    "air_quality",
    "customer_privacy",
    "ecological_impacts",
    "energy_management",
    "ghg_emissions",
]
values = []
for info in output[0]:
    values.append(info["score"])

data = {"factors": factors, "values": values}
df = pd.DataFrame(data=data)
print(df)
