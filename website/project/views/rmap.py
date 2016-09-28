from framework.exceptions import HTTPError
from website.project.decorators import (
    must_be_valid_project,
    must_have_permission,
)
from website.util.permissions import ADMIN


def _create_rmap_for_node(node):
    # TODO: Make request to RMAP service
    return '<rmapid would be returned>'


@must_be_valid_project
@must_have_permission(ADMIN)
def node_rmap_post(node, auth, *args, **kwargs):
    if not node.is_public:
        raise HTTPError(400, data=dict(message_long='RMaps can only be created '
                                       'for public projects. Make your project public '
                                       'and retry your request.'))
    rmap_id = _create_rmap_for_node(node)
    node.set_identifier_value('rmap', rmap_id)
    return {
        'rmap_id': rmap_id
    }, 201
