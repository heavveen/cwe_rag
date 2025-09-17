import xmltodict
import json

# 读取XML文件
xml_file_path = r"C:\Users\38308\Desktop\cwec_latest.xml\cwec_v4.17.xml"
with open(xml_file_path, 'r', encoding='utf-8') as file:
    xml_data = xmltodict.parse(file.read())

# 提取CWE弱点数据
cwe_entries = xml_data.get('Weakness_Catalog', {}).get('Weaknesses', {}).get('Weakness', [])

# 组织数据为列表
cwe_data = []
for entry in cwe_entries:
    cwe_item = {
        'ID': entry.get('@ID'),
        'Name': entry.get('@Name'),
        'Description': entry.get('Description'),
        'Extended_Description': entry.get('Extended_Description', ''),
        'Potential_Mitigations': entry.get('Potential_Mitigations', {}).get('Mitigation', []),
        'Related_Attack_Patterns': entry.get('Related_Attack_Patterns', {}).get('Related_Attack_Pattern', [])
    }
    cwe_data.append(cwe_item)

# 保存为JSON文件
json_file_path = r"C:\Users\38308\Desktop\cwe_data.json"
with open(json_file_path, 'w', encoding='utf-8') as file:
    json.dump(cwe_data, file, indent=4)
