HelloFresh DevOps Test
========================

Hello and thanks for taking the time to try this out.

The goal of this test is to assert (to some degree) your coding, testing and documentation skills. You're given a simple problem, so you can focus on showcasing your techniques.

## Problem definition
HelloFresh Tech is growing and we decided to have one AWS account per team. We would like to change each AWS account alias name to reflect team name for billing purposes. Since we love automating things, we decided to create an Ansible role that takes **AWS alias name** as parameter and takes care of compliance.

_Note: While we love open source here at HelloFresh, please do not create a public repo with your test in! This challenge is only shared with people interviewing, and for obvious reasons we'd like it to remain this way._

## Instructions
1. Clone this repository.
2. Create a new `dev` branch.
3. Solve the task and commit your code. Commit often, we like to see small commits that build up to the end result of your test, instead of one final commit with all the code.
4. Do a pull request from the `dev` branch to the `master` branch. More on that right below.
5. Reply to the thread you are having with our HR department so we can start reviewing your code.

When you're finished, please do a pull request to `master` and make sure to write about your approach in the description. One or more of our engineers will then perform a code review. We will ask questions which we expect you to be able to answer. Code review is an important part of our process; this gives you as well as us a better understanding of how working together might be like.

We believe it will take 4 to 8 hours to develop this task, however, feel free to invest as much time as you want.

## Requirements
* Create the Ansible role that encapsulates an Ansible module
* The Ansible **role** MUST accept following parameters:
  * **aws_account_alias** - if set, changes AWS account alias name. If this parameter is not set, role should do nothing.
  * **aws_account_state** - if set to absent, removes account alias. Accepts 'present', 'absent', defaults to present.
  * **aws_access_key** - if not set, then the value of the AWS_ACCESS_KEY_ID environment variable should be used.
  * **aws_secret_key** - if not set, then the value of the AWS_SECRET_ACCESS_KEY environment variable should be used.
* The module MUST always output the following unless exception happened:
  * **changed** - boolean, reflects if account alias name changed.
  * **aws_account_id** - The AWS account ID.
  * **aws_account_alias** - The current account alias, as known to AWS.
```json
{
    "changed" : true,
    "aws_account_id": 123123123,
    "aws_account_alias": "SuperTeamA"
}
```
* In your **role** you MUST [register](http://docs.ansible.com/ansible/playbooks_variables.html#registered-variables) the variable **aws_alias_status** with the result of the task that uses your module:
```yaml
    - name: Ensure AWS alias name
      YourSuperModule:
        name="{{ SuperTeamVarName }}"
      register: aws_alias_status
```
* The module MUST be idempotent, and change AWS account alias name only if required.
* The module MUST handle network, AWS and permission exceptions.
* You MUST write tests for your module.
* For extra points you can support *diff* and *dry run* in your module.
* For more extra points you can write tests for your role and provide tests to assert it works with Ansible 2.0, 2.1 and 2.2.

## Rules
* You MUST use *Python*, *Ruby*, or *Go* to develop the Ansible module.
* You can use AWS [SDK](https://aws.amazon.com/tools/), or any other SDK.
* If your module requires external modules, e.g. Ruby Gems or Python Packages, your module should fail with the corresponding message, but keep it minimal.
* Your MUST create your role in [aws_alias_role](aws_alias_role) directory.
* We will execute [run_tests.sh](run_tests.sh) to run all unit, integration and role tests. This should be the entry point of your tests. You can split your tests accross different test frameworks, files, etc.
* You can use any testing, mocking libraries provided that you state the reasoning and it's simple to install and run.
* You can use an integration framework, like [test-kitchen](https://github.com/test-kitchen/), [molecule](https://github.com/metacloud/molecule) or any other you prefer.
* You SHOULD document your role and module.
* We will use Ansible 2.2.1.0 to run your code.

## Reference & hints
* You will probably need to create a [free AWS](http://aws.amazon.com/en/free/) (if you don't already have one). If you are unable to create an account please contact us.
* AWS aliases are unique account identifiers, and they can not conflict with existing accounts, think of failing scenarios.
* Documentation on [AWS Account ID and Alias](http://docs.aws.amazon.com/IAM/latest/UserGuide/console_account-alias.html).
* You can embed modules inside roles by creating a `library` directory in the root of the role.
See [Ansible Documentation](http://docs.ansible.com/ansible/dev_guide/developing_modules_general.html).
