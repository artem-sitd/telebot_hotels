"""
1. locations/v3/search - предоставляет ответ по выбранной локации из которого
 нужно вытянуть `id` локации

2. properties/v2/list - предоставляет ответ с информацией по отелям: id отеля,
название, цена. Ожидает от вас `id` локации

3. properties/v2/detail - предоставляет ответ с подробной информацией об отеле:
 точный адрес, фотографии. Ожидает от вас `id` отеля
"""
import traceback
import datetime
import json
import requests
from config_data.config import headers


# Возврат ID локации + Проверка на корректность указания города
def check_city(city):
    url = "https://hotels4.p.rapidapi.com/locations/v3/search"
    querystring = {"q": city, "locale": "ru_RU"}
    try:
        response = json.loads(
            requests.get(url, headers=headers, params=querystring).text
        )
        return response["sr"][0]["gaiaId"]
    except (json.decoder.JSONDecodeError, IndexError, KeyError):
        print(traceback.format_exc())
        return None


# Получение списка отелей POST properties/v2/list
def get_lists(
        gaiaId: str,
        checkin: datetime.date,
        checkout: datetime.date,
        count_hotels: int,
        count_photo: int = None,
):
    url = "https://hotels4.p.rapidapi.com/properties/v2/list"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "destination": {"regionId": gaiaId},
        "checkInDate": {
            "day": checkin.day,
            "month": checkin.month,
            "year": checkin.year,
        },
        "checkOutDate": {
            "day": checkout.day,
            "month": checkout.month,
            "year": checkout.year,
        },
        "rooms": [{"adults": 2, "children": [{"age": 5}, {"age": 7}]}],
        "resultsStartingIndex": 0,
        "resultsSize": int(count_hotels),
        "sort": "PRICE_LOW_TO_HIGH",
        "filters": {"price": {"max": 250, "min": 10}},
    }

    try:
        response = json.loads(requests.post(url, json=payload, headers=headers).text)[
            "data"
        ]["propertySearch"]["properties"]
    except (json.decoder.JSONDecodeError, IndexError, KeyError):
        return None
    data = []

    try:
        for i in response:
            propertyId = i["id"]
            # Проверить работоспособность этого кода (строка ниже)
            temp = {
                "Название отеля": i["name"],
                "Растояние от центра (км)": i["destinationInfo"][
                    "distanceFromDestination"
                ]["value"],
            }
            try:
                temp["Соседний город"] = i["neighborhood"]["name"]
            except TypeError:
                temp["Соседний город"] = "нет информации"
            temp["Сумма"] = i["price"]["displayMessages"][1]["lineItems"][0]["value"]

            if count_photo:  # Если пользователь указал кол-во фото
                detail = get_detail(propertyId, count_photo)
                temp["Адрес"] = detail["address"]
                temp["Фото"] = detail["images"]
            else:
                temp["Адрес"] = get_detail(propertyId)["address"]
            data.append(temp)
        return data
    except KeyError as ke:
        print("какая-то ошибка", ke, traceback.format_exc())
        return None


# Детальная информация по отелю с фото POST properties/v2/detail
def get_detail(propertyId, count_photo=None):
    url = "https://hotels4.p.rapidapi.com/properties/v2/detail"

    payload = {
        "currency": "USD",
        "eapid": 1,
        "locale": "ru_RU",
        "siteId": 300000001,
        "propertyId": propertyId,
    }
    try:
        response = json.loads(requests.post(url, json=payload, headers=headers).text)[
            "data"
        ]["propertyInfo"]
    except (json.decoder.JSONDecodeError, IndexError, KeyError) as ke:
        print("какая-то ошибка", ke, traceback.format_exc())
        return None
    if count_photo:
        try:
            data = {
                "address": response["summary"]["location"]["address"]["addressLine"],
                "images": [
                    response["propertyGallery"]["images"][j]["image"]["url"]
                    for j in range(count_photo)
                ],
            }
            return data
        except KeyError as ke:
            print("какая-то ошибка", ke, traceback.format_exc())
            return None
    else:
        try:
            data = {
                "address": response["summary"]["location"]["address"]["addressLine"]
            }
            return data
        except KeyError as ke:
            print("какая-то ошибка", traceback.format_exc(), ke)
            return None

# Проверка работоспособности
# get_lists('2734', datetime.date(2023, 12, 24), datetime.date(2024, 1, 5), 10, 3)
