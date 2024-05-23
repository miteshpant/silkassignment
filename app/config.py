class Config:
    MONGO_URI = 'mongodb://localhost:27017/silk'
    API_URL = {
        'qualys': 'https://api.recruiting.app.silk.security/api/qualys/hosts/get',
        'crowdstrike': 'https://api.recruiting.app.silk.security/api/crowdstrike/hosts/get'
    }
    API_HOST_LIMIT = 1
    TOTAL_HOSTS_TO_BE_PROCESSED = 7
    SOURCES = ["qualys", "crowdstrike"]
    TOKEN = 'mitesh.pant@gmail.com_81ee2bd7-9be8-4002-9038-253415e2a1bc'