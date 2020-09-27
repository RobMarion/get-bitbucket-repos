# get-bitbucket-repos
Get all repos in a bitbucket project. I wrote this script because I often needed to download all repos in a Bitubucket project, which had to be done manually one at a time.
Stashy did not have that functionality, for some reason.

# install
pip install -r requirements.txt

# run
python getAllRepos.py <repo-key> [output directory]
Rename get_all_repos.template.json to get_all_repos.json and fill in the Bitbucket token and url of the Bitbucket server.

# assumes
Assumes you have Python 3.n installed and read access to a Bitbucket server and a Bitbucket authentication token

# TODO
Only grabs the Master branch. Add support for any branch

# Author
Robert Marion 
Copyright 2020 MIT License
