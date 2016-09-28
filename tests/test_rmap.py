# -*- coding: utf-8 -*-
import httpretty
from nose.tools import *  # flake8: noqa

from framework.auth.core import Auth
from website import settings

from website.project.views.rmap import _rmap_url_for_node, _rmap_url_for_user
from website.util import api_url_for

from tests.base import OsfTestCase
from tests.factories import AuthUserFactory, ProjectFactory


class TestRmapNodeViews(OsfTestCase):

    def setUp(self):
        super(TestRmapNodeViews, self).setUp()
        self.user = AuthUserFactory()
        self.project = ProjectFactory(creator=self.user, is_public=True)
        self.url = self.project.api_url_for('node_rmap_post')

        self._old_rmap_url = settings.RMAP_BASE_URL
        self._old_rmap_pass = settings.RMAP_PASS

        settings.RMAP_BASE_URL = 'rmaptest.test/'
        settings.RMAP_PASS = 'myprecious'

        self._set_up_mock_response_for_node(self.project)

    def _set_up_mock_response_for_node(self, node):
        rmap_url = _rmap_url_for_node(node)
        httpretty.register_uri(
            httpretty.POST,
            rmap_url,
            body='abc123',
            status=200
        )

    def tearDown(self):
        super(TestRmapNodeViews, self).tearDown()
        settings.RMAP_BASE_URL = self._old_rmap_url
        settings.RMAP_PASS = self._old_rmap_pass

    def test_rmap_post_valid(self):
        res = self.app.post_json(self.url, {}, auth=self.user.auth)
        assert_equal(res.status_code, 201)
        self.project.reload()

        rmap_id = self.project.get_identifier('disco')
        assert_true(bool(rmap_id))
        assert_equal(rmap_id.value, 'abc123')

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


class TestRmapUserViews(OsfTestCase):

    def setUp(self):
        super(TestRmapUserViews, self).setUp()
        self.user = AuthUserFactory()
        self.url = api_url_for('user_rmap_post')

        self._old_rmap_url = settings.RMAP_BASE_URL
        self._old_rmap_pass = settings.RMAP_PASS

        settings.RMAP_BASE_URL = 'rmaptest.test/'
        settings.RMAP_PASS = 'myprecious'

        self._set_up_mock_response_for_user(self.user)

    def _set_up_mock_response_for_user(self, user):
        rmap_url = _rmap_url_for_user(user)
        httpretty.register_uri(
            httpretty.POST,
            rmap_url,
            body='abc123',
            status=200
        )

    def tearDown(self):
        super(TestRmapUserViews, self).tearDown()
        settings.RMAP_BASE_URL = self._old_rmap_url
        settings.RMAP_PASS = self._old_rmap_pass

    def test_rmap_post_valid(self):
        res = self.app.post_json(self.url, {}, auth=self.user.auth)
        assert_equal(res.status_code, 201)
        self.user.reload()

        rmap_id = self.user.get_identifier('disco')
        assert_true(bool(rmap_id))
        assert_equal(rmap_id.value, 'abc123')
