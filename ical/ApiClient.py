import urequests
import json
class ApiClient:
    url: str
    content: str
    

    def __init__(self, url, mock = False):
        self.url = url
        if mock:
            self.content = str(mock)
        else:
            self.load()

    def load(self):
        print('request to: {0}'.format(self.url))
        request = urequests.get(self.url)
        print('request status: {0}'.format(request.status_code))
        self.content = request.content
        request.close()

        if request.status_code != 200:
            raise RuntimeError('Error loading URL {0}: Status code {1}'.format(self.url, self.request.status_code))

    def parseResponse(self):
        jsonData = json.loads(self.content)
