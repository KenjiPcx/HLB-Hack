import json
import numpy as np
import pandas as pd
import requests


def main(input_data, size):
    API_URL = ""
    url = ""
    API_TOKEN = ""
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    def query(payload):
        data = json.dumps(payload)
        response = requests.request("POST", API_URL, headers=headers, data=data)
        return json.loads(response.content.decode("utf-8"))

    # filename = "dummy.txt"
    # paragraphs = []
    # with open(filename, "r") as f:
    #     paragraphs = f.readlines()
    # f.close()

    paragraphs = input_data.split("\n")

    context = []
    temp = []
    # size = 2
    num_of_lines_read = 0
    tensor_full = False
    for i in range(size, len(paragraphs), size):
        temp = " ".join(paragraphs[0:i])
        context.append(temp)
    context.append("".join(paragraphs[i:]))

    sum_of_values = [0 for i in range(26)]
    skipped = 0

    esg_most_points = [0 for x in range(26)]

    for para in context:
        try:
            # print(para)
            output = query(para)
            max_idx = 0
            max_score = 0
            for i in range(len(output[0])):
                if output[0][i]["score"] > max_score:
                    max_score = output[0][i]["score"]
                    max_idx = i
                sum_of_values[i] += output[0][i]["score"]

            esg_most_points[max_idx] += 1
            if not tensor_full:
                num_of_lines_read += 1

        except:
            tensor_full = True
            skipped += 1
            print(output)
            print("Tensor size reached maximum capacity")

    values = [None for i in range(26)]
    for i in range(26):
        values[i] = sum_of_values[i] / (len(context))
    # output = query(input_data)

    def checksum(scores):
        total = 0
        for i in range(len(scores)):
            total += scores[i]
        print(total)

    factors = [
        "Business Ethics",
        "Data Security",
        "Access And Affordability",
        "Business Model Resilience",
        "Competitive Behavior",
        "Critical Incident Risk Management",
        "Customer Welfare",
        "Director Removal",
        "Employee Engagement Inclusion And Diversity",
        "Employee Health and Safety",
        "Human Rights And Community Relations",
        "Labor Practices",
        "Management Of Legal And Regulatory Framework",
        "Physical Impacts of Climate Change",
        "Product Quality and Safety",
        "Product Design and Lifecycle Management",
        "Selling Practices and Product Labeling",
        "Supply Chain Management",
        "Systemic Chain Management",
        "Waste and Hazardous Materials Management",
        "Water And Wastewater Management",
        "Air Quality",
        "Customer Privacy",
        "Ecological Impacts",
        "Energy Management",
        "Ghg Emissions",
    ]

    data = {"factors": factors, "values": values}
    df_unmerged = pd.DataFrame(data=data)

    e = [13, 15, 19, 20, 21, 23, 24, 25, 17]
    s = [2, 8, 9, 10, 6, 11, 14, 16]
    g = [0, 1, 3, 4, 5, 7, 12, 18, 22]

    total_e = 0
    total_s = 0
    total_g = 0
    for idx in e:
        total_e += df_unmerged.iloc[idx, 1]
    for idx in s:
        total_s += df_unmerged.iloc[idx, 1]
    for idx in g:
        total_g += df_unmerged.iloc[idx, 1]

    factors_esg = ["Environmental", "Social", "Governance"]
    values_esg = [total_e, total_s, total_g]
    data = {"factors": factors_esg, "values": values_esg}
    df_merged = pd.DataFrame(data=data)

    def convert_to_whole(values):
        total = sum(values)
        for i in range(len(values)):
            values[i] = values[i] / total

    factors_e = [factors[idx] for idx in e]
    factors_s = [factors[idx] for idx in s]
    factors_g = [factors[idx] for idx in g]

    values_e = [values[idx] for idx in e]
    values_s = [values[idx] for idx in s]
    values_g = [values[idx] for idx in g]

    convert_to_whole(values_e)
    convert_to_whole(values_s)
    convert_to_whole(values_g)

    data_e = {"factors": factors_e, "values": values_e}
    data_s = {"factors": factors_s, "values": values_s}
    data_g = {"factors": factors_g, "values": values_g}

    df_e = pd.DataFrame(data=data_e)
    df_s = pd.DataFrame(data=data_s)
    df_g = pd.DataFrame(data=data_g)

    # compute scoring scale
    print(esg_most_points)
    e_points = 0
    s_points = 0
    g_points = 0
    for idx in e:
        e_points += esg_most_points[idx]
    for idx in s:
        s_points += esg_most_points[idx]
    for idx in g:
        g_points += esg_most_points[idx]

    print(e_points, s_points, g_points)

    # output
    # print(df_unmerged.to_numpy)
    # print(df_merged.to_numpy)
    # print(df_e.to_numpy)
    # print(df_s.to_numpy)
    # print(df_g.to_numpy)

    # compute top 3/5
    def remove_null_scores(lst):
        for i in range(len(lst) - 1, -1, -1):
            if lst[i][0] == 0:
                lst.pop()
        return lst

    combine = list(zip(esg_most_points, factors))
    combine.sort(reverse=True)
    combine_without_null = remove_null_scores(combine[:5])
    # print(combine)
    factors_sorted = [factors for esg_most_points, factors in combine_without_null]
    print(factors_sorted)

    df_unmerged = df_unmerged.values.tolist()
    df_merged = df_merged.values.tolist()
    df_e = df_e.values.tolist()
    df_s = df_s.values.tolist()
    df_g = df_g.values.tolist()

    return_json_obj = {
        "unmerged": df_unmerged,
        "merged": df_merged,
        "enviromental": df_e,
        "social": df_s,
        "governance": df_g,
        "esg_points": [e_points, s_points, g_points],
        "top_5_factors": factors_sorted,
    }

    print(return_json_obj)
    return return_json_obj


if __name__ == "__main__":
    input_data = """
    Even with a 171-year history, we at Siemens keep asking ourselves: What kind of company do we want to be? What is 
it that drives our 379,000 employees to give their best every day? The answers to these questions lie in our purpose. 
We defined that purpose as our aspiration to provide innovations that improve quality of life and create value for 
people all over the world. We make real what matters. And every Siemens business will serve this purpose, for all our 
stakeholders  for investors, employees, customers, partners, and societies alike. 
"""
    main(input_data, 1)
