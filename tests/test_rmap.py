# -*- coding: utf-8 -*-
import mock
from nose.tools import *  # flake8: noqa

from framework.auth.core import Auth
from tests.base import OsfTestCase

from tests.factories import AuthUserFactory, ProjectFactory


class TestRmapViews(OsfTestCase):

    def setUp(self):
        super(TestRmapViews, self).setUp()
        self.user = AuthUserFactory()
        self.project = ProjectFactory(creator=self.user, is_public=True)
        self.url = self.project.api_url_for('node_rmap_post')

    @mock.patch('website.project.views.rmap._create_rmap_for_node')
    def test_rmap_post_valid(self, mock_create_rmap):
        mock_create_rmap.return_value = 'abc123'
        res = self.app.post_json(self.url, {}, auth=self.user.auth)
        assert_equal(res.status_code, 201)
        self.project.reload()
        # Project now has a rmap identifier
        rmap_id = self.project.get_identifier('rmap')
        assert_true(bool(rmap_id))
        assert_equal(rmap_id.value, 'abc123')

        # Request was made
        mock_create_rmap.assert_called()
        mock_create_rmap.assert_called_with(self.project)

    def test_rmap_post_non_contributor_should_error(self):
        noncontrib = AuthUserFactory()
        res = self.app.post_json(self.url, {}, auth=noncontrib.auth, expect_errors=True)
        assert_equal(res.status_code, 403)

    def test_rmap_post_non_admin_contributor_should_error(self):
        non_admin = AuthUserFactory()
        self.project.add_contributor(non_admin, permissions=['read', 'write'], auth=Auth(self.user))
        self.project.save()
        res = self.app.post_json(self.url, {}, auth=non_admin.auth, expect_errors=True)
        assert_equal(res.status_code, 403)

    def test_rmap_post_non_public_project_should_error(self):
        private_project = ProjectFactory(creator=self.user, is_public=False)
        url = private_project.api_url_for('node_rmap_post')
        res = self.app.post_json(url, {}, auth=self.user.auth, expect_errors=True)
        assert_equal(res.status_code, 400)
