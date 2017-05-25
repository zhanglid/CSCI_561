import os
import re
vedio_url = raw_input('Please input url for the vedio: ')
vedio_name = re.compile(r'([A-Z]+\d+_\d+)(?:\.mp4)').search(vedio_url).group(1)
vedio_down_url = re.compile(r'\S+\.m3u8').search(vedio_url).group()
os.system('ffmpeg -i \"' + vedio_down_url + '\" -c copy -bsf:a aac_adtstoasc ' + vedio_name + '.mkv')
