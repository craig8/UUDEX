# coding: utf-8

"""
    UUDEXApi

    uudex api  # noqa: E501

    OpenAPI spec version: 1.0
    Contact: jeff.welsh@pnnl.gov
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import uudex_client
from api.subject_policy_api import SubjectPolicyApi  # noqa: E501
from uudex_client.rest import ApiException


class TestSubjectPolicyApi(unittest.TestCase):
    """SubjectPolicyApi unit test stubs"""

    def setUp(self):
        self.api = api.subject_policy_api.SubjectPolicyApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_create_acl_constraint(self):
        """Test case for create_acl_constraint

        Create a ACL Constraint for a given Subject Policy  # noqa: E501
        """
        pass

    def test_create_subject_policy(self):
        """Test case for create_subject_policy

        Creates a Subject Policy and attaches it to given Participant  # noqa: E501
        """
        pass

    def test_delete_acl_constraint(self):
        """Test case for delete_acl_constraint

        Delete a single ACL Constraint for a given Subject Policy  # noqa: E501
        """
        pass

    def test_delete_subject_policy(self):
        """Test case for delete_subject_policy

        Delete a single Subject Policy  # noqa: E501
        """
        pass

    def test_get_acl_constraint(self):
        """Test case for get_acl_constraint

        Return a single ACL Constraint for a given Subject Policy  # noqa: E501
        """
        pass

    def test_get_all_acl_constraints(self):
        """Test case for get_all_acl_constraints

        Return all ACL Constraints for a given Subject Policy  # noqa: E501
        """
        pass

    def test_get_subject_policies(self):
        """Test case for get_subject_policies

        Returns a collection of Subject Policies  # noqa: E501
        """
        pass

    def test_get_subject_policy(self):
        """Test case for get_subject_policy

        Return a single Subject Policy  # noqa: E501
        """
        pass

    def test_update_subject_policy(self):
        """Test case for update_subject_policy

        Update a single Subject Policy  # noqa: E501
        """
        pass


if __name__ == '__main__':
    unittest.main()
