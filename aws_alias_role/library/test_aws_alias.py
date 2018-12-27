import ansible
import json
import mock
import os
import unittest
import boto3

from ansible.module_utils import basic
from aws_alias import (get_acct_id, get_acct_alias, change_account_alias, remove_acct_alias)

import datetime
import botocore.session
from botocore.stub import Stubber


class TestAwsAlias(unittest.TestCase):
    def setUp(self):
        self.aws_account_alias = "test-lat"
        self.aws_account_state = "present"
        self.aws_access_key = "lat-key"
        self.aws_secret_key = "lat-secret"

        self.module = self.test_module()
        self.client = boto3.client('iam', aws_access_key_id=self.aws_access_key,
                                   aws_secret_access_key=self.aws_secret_key)
        self.stubber = Stubber(self.client)

    def test_module(self):
        # Set Ansible Module Arguments

        basic._ANSIBLE_ARGS = json.dumps(dict(
            ANSIBLE_MODULE_ARGS=dict(
                aws_account_alias=self.aws_account_alias,
                aws_account_state=self.aws_account_state,
                aws_access_key=self.aws_access_key,
                aws_secret_key=self.aws_secret_key
            )
        ))

    def test_get_account_id_when_response_is_ok(self):
        client = self.client
        module = self.module
        http_code = 200
        expected_result = 123456789012

        response = {
            'User': {
                'Path': '/',
                'UserName': 'test_lat',
                'UserId': 'test_lat_id_2018',
                'Arn': 'arn:aws:iam::123456789012:user/test_lat',
                'CreateDate': datetime.datetime(2016, 1, 20, 22, 9)
            }
        }

        self.stubber.add_response('get_user', response)
        self.stubber.activate()

        result = int(get_acct_id(module, client))

        self.assertEqual(expected_result, result)

    def test_get_account_id_when_response_is_not_ok(self):
        client = self.client
        module = self.module
        http_code = 400
        error_code = 'AccessDeniedException'
        message = 'You do not have sufficient access to perform this action.'

        self.stubber.add_client_error('get_user', http_code, error_code, message)
        self.stubber.activate()

        self.assertRaises(Exception)


    def test_get_account_alias_when_alias_exists(self):
        client = self.client
        module = self.module
        http_code = 200
        expected_result = "lat-alias"
        response = {
            "AccountAliases" : ["lat-alias"]
        }

        self.stubber.add_response('list_account_aliases', response)
        self.stubber.activate()

        result = get_acct_alias(module,client)

        self.assertEqual(expected_result, result)

    def test_get_account_alias_when_alias_does_not_exist(self):
        client = self.client
        module = self.module
        http_code = 200
        expected_result = ""
        response = {
            "AccountAliases" : [ ]
        }

        self.stubber.add_response('list_account_aliases', response)
        self.stubber.activate()

        result = get_acct_alias(module,client)
        print("result is ", result)

        self.assertEqual(expected_result, result)


    def test_change_account_alias_when_current_alias_is_different_from_new_alias(self):
        client = self.client
        module = self.module
        http_code = 200
        alias = "test-lat"
        new_alias = "test-lat-new"
        response = {
            'ResponseMetadata': {
                'HTTPStatusCode':http_code,
                'RequestId': 'ead8f062-651e-11e8-b86a-9d13b8551895',
            }
        }

        self.stubber.add_response('create_account_alias', response)
        self.stubber.activate()

        changed = True
        result = changed

        self.assertTrue(result)

    def test_change_account_alias_when_current_alias_is_same_as_new_alias(self):
        client = self.client
        module = self.module
        http_code = 409
        alias = "test-lat"
        new_alias = "test-lat"

        error_code = 'EntityAlreadyExists'
        message = 'The request was rejected because it attempted to create a resource that already exists.'

        self.stubber.add_client_error('create_account_alias',error_code,http_code,message)
        self.stubber.activate()

        changed = False
        result = changed

        self.assertRaises(Exception)
        self.assertFalse(changed)

    def test_remove_existing_account_alias(self):
        client = self.client
        module = self.module
        alias = "test-lat"
        alias_to_remove = "test-lat"
        http_code = 200
        response = {
            'ResponseMetadata': {
                'HTTPStatusCode': http_code,
                'RequestId': 'ead8f062-651e-11e8-b86a-9d13b8551908',
            }
        }

        self.stubber.add_response('delete_account_alias', response, alias_to_remove)
        self.stubber.activate()

        changed = True
        result = changed

        self.assertTrue(result)

    def test_remove_account_when_non_existent_account_alias(self):
        client = self.client
        module = self.module
        http_code = 404
        alias = "test-lat"
        new_alias = "test-lat"
        self.aws_account_state = "absent"

        error_code = 'NoSuchEntity'
        message = 'The request was rejected because it referenced an entity that does not exist. The error message describes the entity.'

        self.stubber.add_client_error('delete_account_alias',error_code,http_code,message)
        self.stubber.activate()

        changed = False
        result = changed

        self.assertRaises(Exception)
        self.assertFalse(result)
