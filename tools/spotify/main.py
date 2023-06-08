from langchain.tools.ifttt import IFTTTWebhook
from decouple import config
import os
key = config('IFTTT')
os.environ['IFTTTKey'] = config('IFTTT')

url = f"https://maker.ifttt.com/trigger/add_song/json/with/key/{key}"
tool = IFTTTWebhook(name="add_song", description="Add a song to spotify playlist. The input is the song name ONLY", url=url)
print(tool.run('Baby'))
def add_song_tool():
    return [tool]