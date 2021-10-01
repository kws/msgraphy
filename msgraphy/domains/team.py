from msgraphy.client.graph_client import GraphResponse
from msgraphy.data import ListResponse, ApiIterable
from msgraphy.data.group import Group
from msgraphy.data.team import Team


class TeamGraphApi:

    def __init__(self, api):
        self._api = api

    def list_teams(self, search=None) -> GraphResponse[ListResponse[Group]]:
        filter_team = lambda g: "Team" in g.resource_provisioning_options
        if search:
            filter = lambda g: filter_team(g) and search.lower() in g.display_name.lower()
        else:
            filter = filter_team

        response_type = ApiIterable(self._api.client, Group, filter=filter)

        return self._api.client.make_request(url="/groups", response_type=response_type)

    def create_team(self, team: Team, template: str = "https://graph.microsoft.com/v1.0/teamsTemplates('standard')"):
        data = team.asdict()
        data['template@odata.bind'] = template
        print(data)
        return self._api.client.make_request(url="/teams", method="post", json=data)
