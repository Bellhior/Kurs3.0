import json


from datetime import datetime


def get_data():
    """Получение данных"""
    with open("operations.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def get_filtered_data(data, filter_empty_from=False):
    """Фильтрация значений по выполненным операциям"""
    data = [x for x in data if "state" in x and x["state"] == "EXECUTED"]
    if filter_empty_from:
        data = [x for x in data if "from" in x]
    return data


def get_last_values(data, count_last_values):
    """Сортировка по дате и возвращение последних операций"""
    data = sorted(data, key=lambda x: x["date"], reverse=True)
    data = data[:count_last_values]
    return data


def get_formatted_data(data):
    """Приведение вывода к виду по условиям курсовой"""
    formatted_data = []
    for row in data:
        date = datetime.strptime(row["date"], '%Y-%m-%dT%H:%M:%S.%f').strftime("%d.%m.%Y")
        description = row["description"]
        operations_amount = f"{row['operationAmount']['amount']} {row['operationAmount']['currency']['name']}"
        if "from" in row:
            sender = row["from"].split()
            from_bill = sender.pop(-1)
            from_bill = f'{from_bill[:4]} {from_bill[4:6]}** **** {from_bill[-4:]}'
            from_info = " ".join(sender)
        else:
            from_info, from_bill = ", "
        if "to" in row:
            recipient = row["to"].split()
            to_bill = recipient.pop(-1)
            to_bill = f"**{to_bill[-4:]}"
            to_info = " ".join(recipient)
        else:
            continue
        formatted_data.append(f"""\
    {date} {description}
    {from_info} {from_bill} -> {to_info} {to_bill}
    {operations_amount}""")
    return formatted_data
