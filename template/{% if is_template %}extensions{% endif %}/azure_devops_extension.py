import requests
from jinja2.ext import Extension

def extant_azdo_org(org):
    """
    Checks if Azure DevOps organization exists.
    """
    r = requests.get(f"https://dev.azure.com/{org}")
    if r.status_code == 203:
        return True
    else:
        return False

def valid_azdo_token_for_org(token, org):
    """
    Checks if Azure DevOps token is valid.
    """
    # This doesn't currently work
    return True
    # try:
    #     headers = {
    #         "Content-Type": "application/json",
    #         "Accept": "application/json"
    #     }
    #     r = requests.get(f"https://dev.azure.com/{org}/_apis/projects?api-version=7.1-preview.1", auth=('', token), headers=headers)
    #     r.raise_for_status()
    #     return True
    # except:
    #     return False

def available_azdo_repo_name_for_token_and_org_and_project(repo, token, org, project):
    """
    Checks if an Azure DevOps repo name is available.
    """
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    r = requests.get(f"https://dev.azure.com/{org}/{project}/_apis/git/repositories?api-version=7.1-preview.1", auth=('', token), headers=headers)
    r.raise_for_status()
    repos = []
    for item in r.json()["value"]:
        repos.append(item["name"])
    if repo not in repos:
        return True
    else:
        return False


class AzureDevOpsExtension(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.tests["extant_azdo_org"] = extant_azdo_org
        environment.tests["valid_azdo_token_for_org"] = valid_azdo_token_for_org
        environment.tests["valid_azdo_project_for_token_and_org"] = valid_azdo_project_for_token_and_org
        environment.tests["available_azdo_repo_name_for_token_and_org_and_project"] = available_azdo_repo_name_for_token_and_org_and_project
