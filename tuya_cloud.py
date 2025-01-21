import os
from typing import NamedTuple

import pydantic
import pydantic.error_wrappers
import tinytuya
from dotenv import load_dotenv
from pydantic import BaseModel, model_validator

from exceptions import APITuyaException

# Turn on Debug Mode
# tinytuya.set_debug(True)

# Connect to Tuya Cloud
load_dotenv()

Celcius = float
Percent = float


class Answer_dict(BaseModel):
    code: str = "code"
    value: int


class ResponseModel(BaseModel):
    data: dict[str, int]

    @model_validator(mode="before")
    def transform_result_to_dict(cls, values):
        # Преобразование списка result в словарь
        result_list = values.get("result", [])
        if result_list != []:
            values["data"] = {
                item["code"]: item["value"] for item in result_list
            }
            return values
        else:
            raise APITuyaException


class SensorData(NamedTuple):
    temperature: Celcius
    humidity: Percent
    battery: int


c = tinytuya.Cloud(
    apiRegion="eu",
    apiKey=os.getenv("API_KEY"),
    apiSecret=os.getenv("API_SECRET"),
    apiDeviceID=os.getenv("TEMP_ID"),
)

# Display list of devices


def get_temp():
    response = c.getstatus(os.getenv("TEMP_ID")) or {}
    # print(response)
    try:
        result = ResponseModel(**response)
    except pydantic.error_wrappers.ValidationError:
        raise APITuyaException
    return SensorData(
        temperature=result.data["temp_current"] / 10,
        humidity=result.data["humidity_value"] / 10,
        battery=result.data["battery_percentage"],
    )


if __name__ == "__main__":
    print(get_temp())
