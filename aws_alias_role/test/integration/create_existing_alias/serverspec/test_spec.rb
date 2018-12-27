require_relative '../../helper_spec.rb'
require 'aws-sdk'

context "when creating an already existing alias" do
	client = Aws::IAM::Client.new(region: "eu-west-1")
  	response = client.list_account_aliases({})
  	aws_account_alias = response.account_aliases[0]
    it 'responds with 409'
    it { expect(aws_account_alias).to eql("test-lat") }
end
