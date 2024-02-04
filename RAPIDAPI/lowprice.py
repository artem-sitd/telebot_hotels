import datetime
import traceback

from config_data.config import headers

from .responses import get_detail as GT
from .responses import get_lists


def process_data(
    gaiaId: str,
    checkin: datetime.date,
    checkout: datetime.date,
    count_hotels: int,
    bestdeal: bool = False,
    distance=None,
    min_price: float = 0,
    max_price: float = 1000,
    sort_by: int = 1,
    count_photo: int = None,
):
    if bestdeal:  # убираем не подходящие по удаленности от центра
        pre_response = get_lists(
            gaiaId, checkin, checkout, min_price=min_price, max_price=max_price
        )
        response = []
        for k, v in enumerate(pre_response):
            if len(response) < count_hotels and k <= len(pre_response):
                if (
                    float(v["destinationInfo"]["distanceFromDestination"]["value"])
                    <= distance
                ):
                    response.append(v)
        response = sorted(
            response,
            key=lambda x: float(
                x["destinationInfo"]["distanceFromDestination"]["value"]
            ),
        )
    else:
        response = get_lists(gaiaId, checkin, checkout, count_hotels=count_hotels)
    data = []
    try:
        for i in response[::sort_by]:
            propertyId = i["id"]
            temp = {
                "Название отеля": i["name"],
                "Растояние от центра (км)": float(
                    i["destinationInfo"]["distanceFromDestination"]["value"]
                ),
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

        if bestdeal:  # Если это конмада bestdeal - тогда сортирует по расстоянию
            return sorted(data, key=lambda x: x["Растояние от центра (км)"])
        return data
    except KeyError as ke:
        print("нет ключа", ke, traceback.format_exc())
        return None


def get_detail(propertyId, count_photo=None):
    response = GT(propertyId, count_photo=count_photo)
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
