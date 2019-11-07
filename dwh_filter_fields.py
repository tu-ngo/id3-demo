import httplib
import json
import time

from decision_tree import DecisionTree
from dwh_reader import DwhMetadataReader


def filter_field(metadata):
    tables = metadata['tables']
    print tables
    cols = []
    for table in tables:
        for col in table['columns']:
            row = dict()
            row['DataType'] = col['dataType']['dataTypeName'].upper()
            row['Length'] = 'null'

            if not (col['dataType']['length'] is None):
                row['Length'] = str(col['dataType']['length'])
            if not (col['dataType']['precision'] is None):
                row['Length'] = row['Length'] + '.' + str(col['dataType']['precision'])

            result = tree_field.evaluate(tree_field_dict, row)
            if result == 'T':
                cols.append(col)
            else:
                print('Removed :', col)

        print ('Final cols for table ' + table['name'] + ': ', cols)
        table['columns'] = cols

        # TODO: remove prefix hard-code
        metadata['prefix'] = 'hackathon-'
    return metadata


def create_views(generateViewRequest, data_source_id='5dc4724d0c542fc4740c3837', username='bear@gooddata.com',
                 password='',
                 poll_delay=5):
    c = httplib.HTTPSConnection("hnh0511.na.intgdc.com")
    # TODO: remove hardcode for authentication
    # authentication = base64.b64encode(b'%s:%s' % (username, password)).decode("ascii")
    authentication = u'YmVhckBnb29kZGF0YS5jb206amluZHJpc3NrYQ=='
    headers_post = {'Authorization': 'Basic %s' % authentication,
                    'User-Agent': 'GoodData/MSF-GREST',
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'}

    headers_get = {'Authorization': 'Basic %s' % authentication,
                   'User-Agent': 'GoodData/MSF-GREST',
                   'Accept': 'application/json, text/plain'}
    metadata_url = '/gdc/dataload/dataSources/' + data_source_id + '/generateView'
    json_body = json.dumps(generateViewRequest)

    print json_body
    c.request('POST', metadata_url, body=json_body, headers=headers_post)
    response = c.getresponse()
    data = json.loads(response.read())
    print data

    # poll task until finished
    while True:
        poll_task_url = data['asyncTask']['links']['poll']
        c.request('GET', poll_task_url, headers=headers_get)
        response = c.getresponse()
        data = json.loads(response.read())
        async_task = data.get('asyncTask')
        print data
        if async_task is None:
            break
        time.sleep(poll_delay)

    return data


dwh_reader = DwhMetadataReader()
tree_field = DecisionTree('field.csv')
tree_field_dict = tree_field.create_tree_dict(tree_field.training_data, tree_field.classes, tree_field.features)

metadata = dwh_reader.get_metadata()
filtered_metadata = filter_field(metadata)

generateViewRequest = {'generateViewRequest': {'cloudResourceMetadata': filtered_metadata}}
create_views(generateViewRequest)
