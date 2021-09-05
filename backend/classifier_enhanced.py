import json
import numpy as np
import pandas as pd
import requests


def compute(input_data):
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

    paragraphs = input_data

    sum_of_values = [0 for i in range(26)]
    skipped = 0

    esg_most_points = [0 for x in range(26)]

    # try:
    #     # print(para)
    #     output = query(para)
    #     print(para)
    #     max_idx = 0
    #     max_score = 0
    #     for i in range(len(output[0])):
    #         if output[0][i]["score"] > max_score:
    #             max_score = output[0][i]["score"]
    #             max_idx = i
    #         sum_of_values[i] += output[0][i]["score"]

    #     esg_most_points[max_idx] += 1

    # except:

    #     print(output)
    #     print("Tensor size reached maximum capacity")

    # print(para)
    output = query(paragraphs)
    # print(paragraphs)
    max_idx = 0
    max_score = 0
    for i in range(len(output[0])):
        if output[0][i]["score"] > max_score:
            max_score = output[0][i]["score"]
            max_idx = i
        sum_of_values[i] += output[0][i]["score"]

    esg_most_points[max_idx] += 1

    # print("hello")
    values = [None for i in range(26)]
    for i in range(26):
        values[i] = sum_of_values[i] / (len(paragraphs))
    # output = query(input_data)

    def checksum(scores):
        total = 0
        for i in range(len(scores)):
            total += scores[i]
        # print(total)

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

    # print(return_json_obj)
    return return_json_obj


def main(input_data):
    paragraphs = input_data.split("\n\n")
    # print(paragraphs)
    current_para = 1
    # para_and_tag = {"paragraph": [], "tags": []}
    data = []
    for para in paragraphs:
        # print(current_para)
        # print(para)
        output = compute(para)
        if output["top_5_factors"] == []:
            tag = None
        else:
            tag = output["top_5_factors"][0]

        temp = {}
        temp["paragraph"] = para
        temp["tag"] = tag
        data.append(temp)

        current_para += 1
    print(data)
    return data


if __name__ == "__main__":

    input_data = """
    Even with a 171-year history, we at Siemens keep asking ourselves: What kind of company do we want to be? What is 
it that drives our 379,000 employees to give their best every day? The answers to these questions lie in our purpose. 
We defined that purpose as our aspiration to provide innovations that improve quality of life and create value for 
people all over the world. We make real what matters. And every Siemens business will serve this purpose, for all our 
stakeholders  for investors, employees, customers, partners, and societies alike. 

We put this purpose at the center of our Vision 2020+ company concept. It builds upon our Vision 2020 strategy 
 program, which we started in 2014. With Vision 2020+, were enforcing our commitment to sustainable practices. To 
measure  the  value  we  create  for  society,  Siemens  uses  the  United  Nations  Agenda  2030  and  its  17  Sustainable 
 Development Goals (SDGs) as a guideline. The SDGs provide a comprehensive definition of sustainability, ranging 
from good health and well-being, affordable and clean energy and climate action to quality education, peace, justice 
and strong institutions. 

Siemens can positively impact practically all of these, directly or indirectly, by defining what kind of business we want 
to conduct and how we conduct it. We have therefore developed the Business to Society approach to measure the value 
we create for societies. First, we identify issues that are relevant for the countries and communities in which we are 
active. Then, we assess the impact were making as we strive to address these issues  through our portfolio as well as 
through our local operations and our corporate citizenship activities. 

For example, this fiscal year, we completed the worlds largest power plant project in Egypt. It will provide clean 
 electricity to 40 million people. By using our efficient H-class gas turbine technology, the country will save more than 
$ 1 billion annually on fuel costs through better fuel utilization. In the North Sea, we installed our HVDC converter station 
BorWin3. It will go into operation in 2019 and will provide more than 1 million German households with clean electric-
ity from wind energy. 

With buildings representing 40 percent of primary energy use globally, energy-efficiency measures enable a significant 
contribution to decarbonization. At Melbourne Museum, for example, our efficiency improvements have already helped 
reduce greenhouse gas emissions by 35 percent and bring electricity costs down by 32 percent. The investments within 
our Energy Performance Contracting agreement will be paid back over seven years through the energy savings achieved. 

Decarbonization is a major lever in fighting climate change. The technologies in our environmental portfolio are a 
major element of our global decarbonization efforts. In fiscal 2018, the technologies in our environmental portfolio 
enabled customers all over the world to reduce their CO2 emissions by 609 million metric tons, which translates to 
roughly 75 % of the annual emissions of Germany. 

But we are not only helping our customers achieve energy efficiency and reduce carbon emissions. We have also set 
an ambitious target for ourselves: We aim to become carbon neutral by 2030, as the first global industrial company 
to have set this goal. And we are firmly on track to achieve this target. Since fiscal 2014, we've managed to cut our  
CO2 emissions by approximately 33 percent  from 2.2 million tons to 1.5 million tons in fiscal 2018. In Germany, 80 % 
of the electricity consumption of our sites is already covered by renewables. Our total investment in these measures, 
which will total about  100 million by 2020, will pay off in the long run. We expect to achieve accumulated annual 
savings of  20 million by that date. 

Were also making a difference for society in the way we conduct business. We firmly believe that developing local jobs 
and skills is a value in itself. Training is one of the pillars of our companys future. Thats why we invest more than 
 500 million annually in training and education for our employees. We continually adapt our training courses to meet 
new requirements to make sure our employees are as fit as possible for the future. Today, digital skills such as data 
analytics, software development, and data security are part of all our curricula. And with approximately 11,000 young 
women and men worldwide  currently enrolled in training or two-track programs at Siemens, which combine theory 
and practice, we are one of the worlds largest private training companies.
"""
    from get_pdf_text import get_pdf_text

    input_data = get_pdf_text("./uploads/CYHI_2021_-_Kickoff_Briefing.pdf")
    print(input_data)
    main(input_data)
