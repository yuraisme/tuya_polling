import os
from typing import NamedTuple

import tinytuya
from dotenv import load_dotenv

from exceptions import APITuyaException, EnvLoadException

try:
    # Загружаем .env
    load_dotenv()
    # tinytuya.scan()
    # Connect to Device
    TEMP_ID = os.getenv("TEMP_ID")
    GW_ID = os.getenv("GW_ID")
    LOCAL_KEY = os.getenv("LOCAL_KEY")
    NODE_ID = os.getenv("NODE_ID")
except Exception:
    raise EnvLoadException
    exit(0)

if NODE_ID is None:
    raise EnvLoadException
    exit(0)

Celcius = float
Percent = float
 
class SensorData(NamedTuple):
    temperature: Celcius
    humidity: Percent
    battery: int


def connect_to_device() -> dict[str, dict] | None:
    """Connect to tuya Gatewat to request data"""
    try:
        tuiya_gateway = tinytuya.Device(
            dev_id=GW_ID,
            address=None,
            local_key=LOCAL_KEY or "",
            persist=True,
            version=3.3,
        )

        print(tuiya_gateway.address)
        # print(tuiya_gateway.status())

        tuya_temp = tinytuya.OutletDevice(
            dev_id=TEMP_ID,
            cid=NODE_ID,
            # address=None,
            # local_key=LOCAL_KEY,
            parent=tuiya_gateway,
        )

    except Exception:
        raise APITuyaException

    if tuya_temp:
        return tuya_temp.status()
    else:
        raise APITuyaException


def get_tuya_temp(sensor_info: dict[str, dict] | None, debug: bool = False):
    """parse and return temp|humidity|Battery Status"""
    if sensor_info:
        parsed_data = sensor_info.get("dps", None)
        if debug:
            print(sensor_info)
    else:
        if debug:
            print("No valid data from sensor")
        raise APITuyaException

    if parsed_data and isinstance(parsed_data, dict):
        return SensorData(
            temperature=parsed_data.get("1", -100) / 10,
            humidity=parsed_data.get("2", -100) / 10,
            battery=parsed_data.get("4", -100),
        )
    else:
        raise APITuyaException


if __name__ == "__main__":
    response_sensor = connect_to_device()
    if response_sensor:
        print(get_tuya_temp(response_sensor).temperature)
        print(get_tuya_temp(response_sensor).humidity)
        print(get_tuya_temp(response_sensor).battery)

    else:
        print("Some fail came")
