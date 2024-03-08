import requests
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

API_KEY = os.getenv("API_KEY")
api_url = 'https://api.github.com/graphql'

headers = {'Authorization': 'Bearer %s' % API_KEY}
allResults = list()


def fetch_repository_data(numRepos):
    endCursor = None

    for i in range(int(numRepos/20)):
        variables = {"endCursor": endCursor}
        query_result = make_graphql_request(variables)
        allResults.append(query_result)
        endCursor = query_result['data']['search']['pageInfo']['endCursor']

    return allResults


def make_graphql_request(variables):
    query = """
    query ($endCursor: String) {
        search(query: "stars:>1 fork:false sort:stars-desc", type: REPOSITORY, first:20, after: $endCursor) {
            edges {
                node {
                    ... on Repository {
                        nameWithOwner
                        name
                        owner {
                            login
                        }
                        createdAt
                        updatedAt
                        primaryLanguage {
                            name
                        }
                        totalIssues: issues {
                            totalCount
                        }
                        closedIssues: issues(states: CLOSED) {
                            totalCount
                        }
                        pullRequests(states: MERGED) {
                            totalCount
                        }
                        releases {
                            totalCount
                        }
                    }
                }
            }
            pageInfo {
                endCursor
                hasNextPage
            }
        }
    }
    """
    request = requests.post(url=api_url, json={'query': query, 'variables': variables}, headers=headers)

    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(
            request.status_code, query))


def save_to_csv(result):
    df = pd.DataFrame()
    dfs = []

    for i in range(len(result)):
        normalized_data = pd.json_normalize(result[i]['data']['search']['edges'])
        dfs.append(normalized_data)

    df = pd.concat(dfs, ignore_index=True)

    # Save the dataframe directly to a CSV file
    df.to_csv('scripts/dataset/csv/data.csv', index=False)


result = fetch_repository_data(1000)
save_to_csv(result)
