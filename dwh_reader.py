import httplib
import json
import time


class DwhMetadataReader:
    def __init__(self, data_source_id='5dc4724d0c542fc4740c3837', username='bear@gooddata.com', password='',
                 poll_delay=5):
        c = httplib.HTTPSConnection("hnh0511.na.intgdc.com")
        # TODO: remove hardcode for authentication
        # authentication = base64.b64encode(b'%s:%s' % (username, password)).decode("ascii")
        authentication = u'YmVhckBnb29kZGF0YS5jb206amluZHJpc3NrYQ=='
        headers = {'Authorization': 'Basic %s' % authentication,
                   'User-Agent': 'GoodData/MSF-GREST',
                   'Accept': 'application/json'}
        metadata_url = '/gdc/dataload/dataSources/' + data_source_id + '/metadata/'
        c.request('GET', metadata_url, headers=headers)
        response = c.getresponse()
        data = json.loads(response.read())
        print data

        # poll task until finished
        while True:
            poll_task_url = data['asyncTask']['links']['poll']
            c.request('GET', poll_task_url, headers=headers)
            response = c.getresponse()
            data = json.loads(response.read())
            async_task = data.get('asyncTask')
            print data
            if async_task is None:
                break
            time.sleep(poll_delay)

        self.metadata = data

    def get_metadata(self):
        return self.metadata


