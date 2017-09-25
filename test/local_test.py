import mdk
import requests


class MockRequest(object):

    def __init__(self):
        self.data = None
        self.get = self.repeater
        self.post = self.repeater
        self.put = self.repeater
        self.delete = self.repeater
        self.status = 200

    def repeater(self, url, params=None, headers=None, body=None):
        response = requests.Response()
        response.status_code = self.status
        response.url = url
        response.headers = headers
        self.data = {"_request_url": url, "_request_headers": headers, "_request_params": params, "_request_body": body}
        response.json = self.json
        return response

    def json(self):
        return self.data

SERVER_ADDRESS = "server_address"
SERVICE_URL = SERVER_ADDRESS + "/alfresco/service"

ORG_ID = "org_id"
ORG_URL = SERVICE_URL + "/orgs/" + ORG_ID

PROJECT_ID = "project_id"
PROJECT_URL = SERVICE_URL + "/projects/" + PROJECT_ID

REF_ID = "ref_id"
REF_URL = PROJECT_URL + "/refs/" + REF_ID

ELEMENT_ID = "element_id"
ELEMENT_URL = REF_URL + "/elements/" + ELEMENT_ID


if __name__ == "__main__":
    mock = MockRequest()
    mms_connector = mdk.MmsConnection("server_address", "username", "password")
    mms_connector._requests = MockRequest()

    response_json = mms_connector.get_projects(project_id=PROJECT_ID)
    if response_json["_request_url"] != PROJECT_URL:
        print("Project url error")
    if response_json["_request_body"] is not None:
        print("Project get body error")

    response_json = mms_connector.get_refs(PROJECT_ID, ref_id=REF_ID)
    if response_json["_request_url"] != REF_URL:
        print("Ref url error")
    if response_json["_request_body"] is not None:
        print("Ref get body error")

    response_json = mms_connector.get_element(PROJECT_ID, ELEMENT_ID, ref_id=REF_ID)
    if response_json["_request_url"] != ELEMENT_URL:
        print("Element url error")
    if response_json["_request_body"] is not None:
        print("Element get body error")

    response_json = mms_connector.get_element(PROJECT_ID, ELEMENT_ID)
    if response_json["_request_url"] != ELEMENT_URL.replace(REF_ID, "master"):
        print("Element url error")
    if response_json["_request_body"] is not None:
        print("Element get body error")

    print("testing complete")

        # projectId = raw_input("projectId: ")
        # elementIds = [raw_input("elementId %d: " % (x + 1)) for x in range(3)]
        # orgId = raw_input("orgId: ")
        # element = mms_connector.get_element(projectId, elementIds[0])
        # elements = mms_connector.get_elements(projectId, elementIds[1:3])
        # element["name"] = 'testNameMon4'
        # elements[0]["name"] = 'testNameMon5'
        # elements[1]["name"] = 'testNameMon6'
        # mms_connector.get_element_history(projectId, elementIds[0])
        # mms_connector.get_orgs()
        # project = mms_connector.get_project(projectId)
        # project["name"] = "brandonWasHere"
        # mms_connector.get_project()
        # ref = mms_connector.get_refs(projectId)
        # ref[0]['name'] = "testRef2"
        # mms_connector.get_project_history(projectId)
        # mms_connector.get_project_groups(projectId)
        # mms_connector.get_project_documents(projectId)
        # mms_connector.create_ref(projectId, ref[0])
        # mms_connector.update_element(projectId, element)
        # mms_connector.update_element(projectId, elements)
        # mms_connector.update_project(orgId, project)
        # mms_connector.delete_element(projectId, elementIds[0])
        # mms_connector.delete_elements(projectId, elementIds[1:3])
