import json

# 从文件中读取数据（假设文件名为TV_info.json，你可以根据实际情况修改）
with open(r'D:\AAAPycharmProjects\TV\TV_info.json', 'r', encoding="UTF-8") as file:
    data = json.load(file)

new_data = []
for item in data:
    num = item["num"]
    if "-" in num:
        start, end = map(int, num.split("-"))
        for i in range(start, end + 1):
            new_item = item.copy()
            new_item["num"] = str(i)
            new_data.append(new_item)
    else:
        new_data.append(item)

# 将处理后的数据保存到新的json文件（这里保存为new_TV_info.json，可按需修改）
with open('new_TV_info.json', 'w') as outfile:
    json.dump(new_data, outfile, indent=4)