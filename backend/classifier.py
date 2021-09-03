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


filename = "dummy.txt"
paragraphs = []
with open(filename, "r") as f:
    paragraphs = f.readlines()
f.close()

context = []
temp = []
for i in range(5, len(paragraphs), 5):
    temp = " ".join(paragraphs[0:i])
    context.append(temp)
context.append("".join(paragraphs[i:]))

# print(context)

# paragraphs = input_data.split("\n\n")
# print(paragraphs)

sum_of_values = [0 for i in range(26)]
skipped = 0
for para in context:
    if len(para) < 2:
        skipped += 1
        continue
    try:
        # print(para)
        output = query(para)
        for i in range(len(output[0])):
            sum_of_values[i] += output[0][i]["score"]
    except:
        skipped += 1
        print(output)
        print("paragraphs are too long to be evaluated")

values = [None for i in range(26)]
for i in range(26):
    values[i] = sum_of_values[i] / (len(context) - skipped)
# output = query(input_data)


def checksum(scores):
    total = 0
    for i in range(len(scores)):
        total += scores[i]
    print(total)


print(checksum(values))
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
# values = []
# for info in output[0]:
#     values.append(info["score"])


data = {"factors": factors, "values": values}
df_unmerged = pd.DataFrame(data=data)

e = [13, 15, 19, 20, 21, 23, 24, 25, 17]
s = [2, 8, 9, 10, 6, 11, 14, 16]
g = [0, 1, 3, 4, 5, 7, 12, 18, 22]

values_e = 0
values_s = 0
values_g = 0
for idx in e:
    values_e += df_unmerged.iloc[idx, 1]
for idx in s:
    values_s += df_unmerged.iloc[idx, 1]
for idx in g:
    values_g += df_unmerged.iloc[idx, 1]


factors = ["e", "s", "g"]
values = [values_e, values_s, values_g]
data = {"factors": factors, "values": values}
df_merged = pd.DataFrame(data=data)


print(df_merged.to_numpy)
