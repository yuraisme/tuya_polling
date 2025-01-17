import os
from typing import NamedTuple
import tinytuya
from dotenv import load_dotenv
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

c = tinytuya.Cloud(
        apiRegion="eu", 
        apiKey =  os.getenv("API_KEY"),
        apiSecret=  os.getenv("API_SECRET"),
        apiDeviceID=os.getenv("TEMP_ID"))

# Display list of devices


def get_temp():
    result = c.getstatus(os.getenv("TEMP_ID"))
    if result and isinstance(result, dict):
        # for item in result['result']:
            # print(item['code'],item['value'])
        return SensorData(
            temperature=result['result'][0]['value'],
            humidity=result['result'][1]['value'],
            battery=result['result'][2]['value'],
        )
    else:
        raise APITuyaException



if __name__=="__main__":
    print(get_temp())