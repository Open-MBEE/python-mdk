# Python MMS Integration
import base64
import requests
import json


class MmsConnection(object):

    @staticmethod
    def _listify(arg):
        new_list = list()
        new_list.append(arg)
        return new_list

    @staticmethod
    def add_json_wrapper(element_type, elements):
        if not isinstance(elements, list):
            elements = MmsConnection._listify(elements)
        if not isinstance(elements[0], dict):
            elements = [{"id": element_id} for element_id in elements]
        data = {element_type: elements, "source": "python-mms"}
        return data

    #
    #

    def __init__(self, server, username=None, password=None):
        self.server = server
        self._username = username
        self._password = password
        self._generate_header()
        self._requests = requests

    def _generate_header(self):
        if self._username is None or self._password is None:
            self._header = None
        else:
            self._header = {"Authorization": "Basic " + base64.b64encode(":".join((self._username, self._password))),
                            "Content-Type": "application/json"}

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username
        self._generate_header()

    @property
    def password(self):
        return None

    @password.setter
    def password(self, password):
        self._password = password
        self._generate_header()

    def set_credentials(self, username, password):
        self._username = username
        self._password = password
        self._generate_header()

    def clear_credentials(self):
        self.set_credentials(None, None)
        self._generate_header()

    #
    #

    def generate_orgs_url(self, org_id=None):
        url = self.server + "/alfresco/service/orgs"
        if org_id is not None:
            url += "/" + org_id
        return url

    def generate_projects_url(self, project_id=None, org_id=None):
        if org_id is not None:
            url = self.generate_orgs_url(org_id) + "/projects"
        else:
            url = self.server + "/alfresco/service/projects"
            if project_id is not None:
                url = url + "/" + project_id
        return url

    def generate_refs_url(self, project_id=None, ref_id=None):
        url = self.generate_projects_url(project_id) + "/refs"
        if ref_id is not None:
            url += "/" + ref_id
        return url

    def generate_elements_url(self, project_id=None, ref_id=None, element_id=None):
        url = self.generate_refs_url(project_id, ref_id) + "/elements"
        if element_id is not None:
            url += "/" + element_id
        return url

    #
    #

    def mms_delete_request(self, url, data=None, parameters=None, headers=None):
        return self._mms_request(url, method=self._requests.delete, data=data, parameters=parameters, headers=headers)

    def mms_get_request(self, url, parameters=None, headers=None):
        return self._mms_request(url, method=self._requests.get, data=None, parameters=parameters, headers=headers)

    def mms_post_request(self, url, data=None, parameters=None, headers=None):
        return self._mms_request(url, method=self._requests.post, data=data, parameters=parameters, headers=headers)

    def mms_put_request(self, url, data=None, parameters=None, headers=None):
        return self._mms_request(url, method=self._requests.put, data=data, parameters=parameters, headers=headers)

    def _mms_request(self, url, method, data=None, parameters=None, headers=None):
        if headers is None:
            headers = self._header
        if data is None:
            response = method(url, params=parameters, headers=headers)
        else:
            response = method(url, data=json.dumps(data), params=parameters, headers=headers)
        if response.status_code != 200:
            raise IOError((response.status_code, "Unable to complete request. Error code: " + str(response.status_code)
                          + ". Message: " + str(response.json().get("message"))))
        return response

    #
    #

    def get_element(self, project_id, element_id, ref_id="master", timestamp=None):
        url = self.generate_elements_url(project_id, ref_id, element_id)
        params = None
        if timestamp is not None:
            params = {"timestamp": timestamp}
        response = self.mms_get_request(url, parameters=params)
        return response.json()

    def get_elements(self, project_id, element_ids, ref_id="master", timestamp=None):
        url = self.generate_elements_url(project_id, ref_id)
        body = self.add_json_wrapper("elements", element_ids)
        params = None
        if timestamp is not None:
            params = {"timestamp": timestamp}
        response = self.mms_put_request(url, data=body, parameters=params)
        return response.json()

    def get_element_history(self, project_id, element_id, ref_id="master"):
        url = self.generate_elements_url(project_id, ref_id, element_id) + "/history"
        response = self.mms_get_request(url)
        return response.json()

    def get_refs(self, project_id, ref_id=None):
        url = self.generate_refs_url(project_id, ref_id)
        response = self.mms_get_request(url)
        return response.json()

    def get_project(self, project_id):
        return self.get_projects(project_id=project_id)

    def get_projects(self, org_id=None, project_id=None):
        url = self.generate_projects_url(project_id, org_id)
        response = self.mms_get_request(url)
        return response.json()

    def get_project_history(self, project_id, ref_id="master"):
        url = self.generate_refs_url(project_id, ref_id) + "/history"
        response = self.mms_get_request(url)
        return response.json()

    def get_project_groups(self, project_id, ref_id="master"):
        url = self.generate_refs_url(project_id, ref_id) + "/groups"
        response = self.mms_get_request(url)
        return response.json()

    def get_project_documents(self, project_id, ref_id="master"):
        url = self.generate_refs_url(project_id, ref_id) + "/documents"
        response = self.mms_get_request(url)
        return response.json()

    def get_orgs(self, org_id=None):
        url = self.generate_orgs_url(org_id)
        response = self.mms_get_request(url)
        return response.json()

    #
    #

    def create_element(self, project_id, element_json, ref_id="master"):
        return self.create_elements(project_id, element_json, ref_id=ref_id)

    def create_elements(self, project_id, element_json_list, ref_id="master"):
        url = self.generate_elements_url(project_id, ref_id)
        body = self.add_json_wrapper("elements", element_json_list)
        response = self.mms_post_request(url, data=body)
        return response.json()

    def create_refs(self, project_id, ref_json_list):
        url = self.generate_refs_url(project_id)
        body = self.add_json_wrapper("refs", ref_json_list)
        response = self.mms_post_request(url, data=body)
        return response.json()

    def create_project(self, org_id, project_json_list):
        url = self.generate_orgs_url(org_id)
        body = self.add_json_wrapper("projects", project_json_list)
        response = self.mms_post_request(url, data=body)
        return response.json()

    #
    #

    def update_element(self, project_id, element_json, ref_id="master"):
        return self.create_elements(project_id, element_json, ref_id=ref_id)

    def update_elements(self, project_id, element_json_list, ref_id="master"):
        return self.create_elements(project_id, element_json_list, ref_id=ref_id)

    # def update_ref(self, project_id, ref_json):
    #     url = self.generate_refs_url(project_id, ref_json["id"])
    #     body = self.add_json_wrapper("refs", ref_json)
    #     return self.mms_post_request(url, data=body)

    def update_project(self, project_json):
        url = self.generate_projects_url(project_json["id"])
        body = self.add_json_wrapper("projects", project_json)
        response = self.mms_post_request(url, data=body)
        return response.json()

    #
    #

    def delete_element(self, project_id, element_id, ref_id="master"):
        url = self.generate_elements_url(project_id, ref_id, element_id)
        response = self.mms_delete_request(url)
        return response.json()

    def delete_elements(self, project_id, element_ids, ref_id="master"):
        url = self.generate_elements_url(project_id, ref_id)
        body = self.add_json_wrapper("elements", element_ids)
        response = self.mms_delete_request(url, data=body)
        return response.json()

    # def delete_ref(self, project_id, ref_id):
    #     url = self.generate_refs_url(project_id, ref_id)
    #     return self.mms_delete_request(url)
    #
    # def delete_project(self, project_id):
    #     url = self.generate_projects_url(project_id)
    #     return self.mms_delete_request(url)
