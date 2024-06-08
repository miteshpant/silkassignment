from enum import Enum

class Params(Enum):
    SKIP_LIMIT = 1
    CURSOR = 2

class Config:
    MONGO_URI = 'mongodb://localhost:27017/silk'
    SOURCES = [
        {
            "name": "qualys",
            "api_url": "https://api.recruiting.app.silk.security/api/qualys/hosts/get",
            "param_type": Params.SKIP_LIMIT
        },
        {
            "name": "crowdstrike",
            "api_url": "https://api.recruiting.app.silk.security/api/crowdstrike/hosts/get",
            "param_type": Params.SKIP_LIMIT
        },
        {
            "name": "tenable",
            "api_url": "https://api.recruiting.app.silk.security/api/tenable/hosts/get",
            "param_type": Params.CURSOR
        },
    ]
    API_HOST_LIMIT = 1
    TOTAL_HOSTS_TO_BE_PROCESSED = 7
    TOKEN = 'mitesh.pant@gmail.com_81ee2bd7-9be8-4002-9038-253415e2a1bc'
