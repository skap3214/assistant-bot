from langchain.tools.ifttt import IFTTTWebhook
from decouple import config
import os
key = config('IFTTT')
os.environ['IFTTTKey'] = config('IFTTT')
url = f"https://maker.ifttt.com/trigger/add_to_google_drive/json/with/key/{key}"
tool = IFTTTWebhook(name="add_to_google_drive", description="Add a file url to google drive. This url should be a globally accessable link. The input should ONLY be the file url", url=url)

def add_to_google_drive_tool():
    return [tool]