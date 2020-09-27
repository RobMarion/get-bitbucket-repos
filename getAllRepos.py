#Copyright 2020 Robert Marion MIT License
#
# getAllRepos.py
# downloads zip files of all the repos in a Bitbucket project
# requires: stashy, requests
# usage: python getAllRepos <PROJECT_KEY> [Output directory]
# pip install -r requirements.txt
# TODO: only grabs from master branch -- will add others soon

import os
import stashy
import argparse
import requests
import json

# Add the location of your config file
CONFIG_FILE = '<location of your config file>/get_all_repos.json'

def main():
    config = get_config()
    parser = argparse.ArgumentParser(description='Download all the repos in a Bitbucket project.')
    parser.add_argument('projectKey', metavar='projKey', type=str, help="Bitbucket project key (required)")
    parser.add_argument('output', nargs='?', type=str)
    args = parser.parse_args()
    out_dir = args.output

    if not out_dir:
        out_dir = '.'

    if not os.path.isdir(out_dir):
        print('The path specified does not exist. Using current directory as default')
        out_dir = '.'

    getbitbucket_repos(config, args.projectKey, out_dir)

# looks like:
# curl -X GET https://some.url.net/rest/api/latest/projects/<REPO_KEY>/repos/baggage/archive?format=zip --output Fred.zip

def get_config():
    try:
        with open(CONFIG_FILE) as config:
            config = json.load(config)
    except:
        print("Unable to open config file. Quitting")
        exit()
    return(config)

def getbitbucket_repos(config, project, output_directory):
    if output_directory == '.':
        output_directory = ''
    elif output_directory[-1] != os.sep:
        output_directory += os.sep
    try:
        stash = stashy.client.Stash(config['site_url'], token=config['bitbucket_token'])
    except:
        print("Unable to access the Bitbucket project: ", project)
        exit()

    try:
        bitbucket_repos = stash.projects[project].repos.list()
    except:
        print("Unable to access the Bitbucket project: ", project)
        exit()

    #bitbucket_repos[0]['project']['key']
    base_url = config['site_url'] + 'rest/api/latest/projects'
    token = {'Authorization': 'Bearer '  + config['bitbucket_token']}

    for repo in bitbucket_repos:
        url = base_url + '/' + project + '/repos/' + repo['name']+'/archive?format=zip'
        result = requests.get(url, headers=token)
        status = "Download Failed"
        if result.status_code == 200:
            status = "Download Success"
        print(repo['name'] + ": " + status)
        with open(output_directory + repo['name']+'.zip', 'wb') as zip_file:
            zip_file.write(result.content)

if __name__ == '__main__':
    main()
