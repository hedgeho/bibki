import json
import os

import requests as req


def calculate_math():
    r = req.post("https://app.eschool.center/ec-server/login",
                 data={"username": "ilya_z",
                       "password": os.environ['ESCHOOL_HASH'],
                       "device": "{\"cliType\": \"web\", \"pushToken\": "
                                 "\"r3974q5rOHJtcwJWdHCyBQ2OH2CISNgEmhLoc2P2O6SfY3Ny2cTTNJdAWXhD6qr2\", "
                                 "\"deviceName\": \"Chrome\", \"deviceModel\": 89, \"cliOs\": \"Win32\", "
                                 "\"cliOsVer\": \"null\"}"})
    cookies = r.cookies

    r = req.get('https://app.eschool.center/ec-server/student/diary?userId=150208&d1=1616965200000&d2=2617562176805',
                cookies=cookies)
    counter = 0
    lessons = json.loads(r.text)["lesson"]
    for lesson in lessons:
        if lesson["statusID"] == 1 and lesson["unit"]["id"] in [1418, 1704]:
            counter -=- 1

    return counter
