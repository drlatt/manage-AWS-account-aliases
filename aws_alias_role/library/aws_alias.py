#!/usr/bin/python

DOCUMENTATION = '''
module: aws_alias
short_description: Manage AWS account Aliases
version_added: "2.2.1.0"
author: Lateef Koshemani (@drlatt)
options:
    aws_account_alias:
        description: This option ensures the AWS account alias is changed to the value provided.
            - default: False
            - required: False

    aws_account_state:
        description: This value determines if the AWS account alias is created or deleted.
            - default: present
            - choices: ["present", "absent"]

    aws_access_key:
        description: AWS access key for the AWS account you intend to make changes to
            - required: True

    aws_secret_key:
        description: AWS secret key for the AWS account you intend to make changes to
            - required: True

'''

EXAMPLES = '''

- name: Ensure AWS alias name
  aws_alias:
    aws_account_alias: "{{ aws_account_alias }}"
    aws_account_state: "present"
    aws_access_key: "{{ aws_access_key }}"
    aws_secret_key: "{{ aws_secret_key }}"
  register: aws_alias_status

'''

# Import boto3 and handle import error
try:
    import boto3
    boto_present = True
except ImportError:
    boto_present = False

import os
from ansible.module_utils.basic import AnsibleModule
from botocore.exceptions import ClientError

# get aws_account_id and handle exceptions
account_id = ""
def get_acct_id(module,client):
    global account_id
    try:
        response = client.get_user()
        acct_id_hold = str(response['User']['Arn']).split(':')
        account_id = acct_id_hold[4]
    except Exception as e:
        module.fail_json(msg=str(e))

    return account_id


# get aws_account_alias and handle exceptions
acct_alias = ""
def get_acct_alias(module,client):
    global acct_alias
    try:
        response = client.list_account_aliases()
        acct_aliases = response["AccountAliases"]

        if acct_aliases:
            acct_alias = acct_aliases[0]
        else:
            acct_alias = ""
    except Exception as e:
        module.fail_json(msg=str(e))

    return acct_alias


# change aws_account_alias and handle exceptions
def change_account_alias(module, client, acct_alias):
    changed = False
    try:
        response = client.create_account_alias(AccountAlias=acct_alias)
        changed = True
    except Exception as e:
        module.fail_json(msg=str(e))

    return changed


# remove aws_account_alias and handle exceptions
def remove_acct_alias(module, client, acct_alias):
    changed = False
    try:
        response = client.delete_account_alias(AccountAlias=acct_alias)
        changed = True
    except Exception as e:
        module.fail_json(msg=str(e))

    return changed


def main():

    fields = dict(
        aws_account_alias=dict(default=None, required=False),
        aws_account_state=dict(default='present', choices=['present', 'absent']),
        aws_access_key=dict(default=None, required=True),
        aws_secret_key=dict(default=None, required=True),
    )

    # Initialize instance of AnsibleModule
    module = AnsibleModule(argument_spec=fields)

    # is boto3 installed
    if not boto_present:
        module.fail_json(msg="boto3 is required to run this module, kindly install it")

    aws_account_alias=module.params.get('aws_account_alias')
    aws_account_state=module.params.get('aws_account_state')
    aws_access_key=module.params.get('aws_access_key')
    aws_secret_key=module.params.get('aws_secret_key')

    # make aws_secret_key and aws_access_key default to those set in the operating system's environment variables if not provided
    if not aws_access_key:
        try:
            aws_access_key = os.environ.get('AWS_ACCESS_KEY_ID')
        except:
            module.fail_json(msg="no value available for aws_access_key")

    if not aws_secret_key:
        try:
            aws_secret_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
        except:
            module.fail_json(msg="no value available for aws_secret_key")

    # use the client service, create IAM client
    client = boto3.client('iam',aws_access_key_id=aws_access_key,aws_secret_access_key=aws_secret_key)

    # Initialize variables
    changed = False
    current_alias = get_acct_alias(module, client)
    acct_id = get_acct_id(module, client)

    # if aws_account_alias is set, changes AWS account alias name. If this parameter is not set, role should do nothing.
    if aws_account_alias:
        if aws_account_alias != current_alias and aws_account_state == "present":
            changed = change_account_alias(module, client, aws_account_alias)
            current_alias = aws_account_alias

        # if aws_account_state set to absent, removes account alias. Accepts 'present', 'absent', defaults to present.
        elif aws_account_alias == current_alias and aws_account_state == "absent":
            changed = remove_acct_alias(module, client, acct_alias)
            current_alias = get_acct_alias(module,client)


    module.exit_json(
        changed=changed,
        aws_account_id=acct_id,
        aws_account_alias=current_alias
    )



if __name__ == '__main__':
    main()
