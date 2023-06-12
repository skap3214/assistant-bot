from langchain.tools.ifttt import IFTTTWebhook
from decouple import config
import os
key = config('IFTTT')
os.environ['IFTTTKey'] = config('IFTTT')
url = f"https://maker.ifttt.com/trigger/find_my_phone/json/with/key/{key}"
tool = IFTTTWebhook(name="find_my_phone", description="Useful when you need to find the users device. Once this tool is used, ask the user if they found their phone.", url=url)
def find_my_device_tool():
    return [tool]