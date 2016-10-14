import requests
import httplib as http

from framework.auth.decorators import must_be_logged_in
from framework.exceptions import HTTPError
from website.project.decorators import (
    must_be_valid_project,
    must_have_permission,
    must_be_contributor_or_public,
)
from website.util.permissions import ADMIN
from website import settings


def _rmap_url_for_node(node):
    target = 'osf_registration' if node.is_registration else 'osf_node'
    ret = 'http://{rmap_pass}@{base_url}/transforms/{target}/?id={nid}'.format(
        rmap_pass=settings.RMAP_PASS,
        base_url=settings.RMAP_BASE_URL.rstrip('/'),
        target=target,
        nid=node._id
    )
    disco_id = node.get_identifier_value('disco')
    if disco_id:
        ret += '&discoid={}'.format(disco_id)
    return ret

def _rmap_url_for_user(user):
    ret = 'http://{rmap_pass}@{base_url}/transforms/osf_user/?id={uid}'.format(
        rmap_pass=settings.RMAP_PASS,
        base_url=settings.RMAP_BASE_URL.rstrip('/'),
        uid=user._id
    )
    disco_id = user.get_identifier_value('disco')
    if disco_id:
        ret += '&discoid={}'.format(disco_id)
    return ret

def _create_rmap_for_node(node):
    if not settings.RMAP_BASE_URL or not settings.RMAP_PASS:
        # Need to configure RMAP_URL
        raise HTTPError(503, data=dict(message_long='RMap service disabled at this time.'))
    url = _rmap_url_for_node(node)
    response = requests.post(url)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        raise HTTPError(response.status_code)
    return response.text  # the DiscoID

def _create_rmap_for_user(user):
    if not settings.RMAP_BASE_URL or not settings.RMAP_PASS:
        # Need to configure RMAP_URL
        raise HTTPError(503, data=dict(message_long='RMap service disabled at this time.'))
    url = _rmap_url_for_user(user)
    response = requests.post(url)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        raise HTTPError(response.status_code)
    return response.text  # the DiscoID


@must_be_valid_project
@must_be_contributor_or_public
def node_rmap_get(node, **kwargs):
    """Retrieve identifiers for a node. Node must be a public registration.
    """
    if not node.is_public:
        raise HTTPError(http.BAD_REQUEST)
    return {
        'disco_id': node.get_identifier_value('disco'),
    }


@must_be_valid_project
@must_have_permission(ADMIN)
def node_rmap_post(node, auth, *args, **kwargs):
    if not node.is_public:
        raise HTTPError(400, data=dict(message_long='RMaps can only be created '
                                       'for public projects. Make your project public '
                                       'and retry your request.'))
    disco_id = _create_rmap_for_node(node)
    node.set_identifier_value('disco', disco_id)
    return {
        'disco_id': disco_id
    }, 201


@must_be_logged_in
def user_rmap_post(auth, *args, **kwargs):
    disco_id = _create_rmap_for_user(auth.user)
    auth.user.set_identifier_value('disco', disco_id)
    return {
        'disco_id': 'foo'
    }, 201
