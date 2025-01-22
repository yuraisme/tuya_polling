import os
from typing import NamedTuple

import pydantic
import pydantic.error_wrappers
import tinytuya
from dotenv import load_dotenv
from pydantic import BaseModel, computed_field

from exceptions import APITuyaException

# Turn on Debug Mode
# tinytuya.set_debug(True)

# Connect to Tuya Cloud
load_dotenv()

Celcius = float
Percent = float


class SensorData(NamedTuple):
    temperature: Celcius
    humidity: Percent
    battery: int


class list_dict(BaseModel):
    code: str
    value: int


class MainModel(BaseModel):
    result: list[list_dict]

    @computed_field
    @property
    def temperature(self) -> float:
        return self.result[0].value / 10

    @computed_field
    @property
    def humidity(self) -> float:
        return self.result[1].value / 10

    @computed_field
    @property
    def battery_status(self) -> int:
        return self.result[2].value


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
        # result = ResponseModel(**response)
        request_result = MainModel(**response)
    except pydantic.error_wrappers.ValidationError:
        raise APITuyaException
    return SensorData(
        temperature=request_result.temperature,
        humidity=request_result.humidity,
        battery=request_result.battery_status,
    )


if __name__ == "__main__":
    print(get_temp())
