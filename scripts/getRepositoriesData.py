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
    
    calculate_repositories_age(df)
    calculate_repositories_update(df)
    calculate_pull_requests(df)
    calculate_releases(df)
    calculate_popular_languages(df)
    calculate_closed_issues_ratio(df)
    

def calculate_repositories_age(df):
    # Convert the 'createdAt' column to datetime format
    df['createdAt'] = pd.to_datetime(df['node.createdAt']).dt.tz_localize(None) 

    # Calculate the repository age in days
    df['repository_age'] = (pd.to_datetime('today').tz_localize(None) - df['createdAt']).dt.days

    print(df['repository_age'])


def calculate_repositories_update(df):
    # Convert the 'updatedAt' column to datetime format
    df['updatedAt'] = pd.to_datetime(df['node.updatedAt']).dt.tz_localize(None) 

    # Calculate the repository last update in days
    df['repository_update'] = (pd.to_datetime('today').tz_localize(None) - df['updatedAt']).dt.days

    print(df['repository_update'])


def calculate_pull_requests(df):
    total_pull_requests = df['node.pullRequests.totalCount']
    print('Total de Pull Requests Aceitas:')
    print(total_pull_requests)


def calculate_releases(df):
    total_releases = df['node.releases.totalCount']
    print('Total de Releases:')
    print(total_releases)


def calculate_popular_languages(df):
    popular_languages = df['node.primaryLanguage.name'].value_counts()
    print('Linguagens Mais Populares:')
    print(popular_languages)


def calculate_closed_issues_ratio(df):
    df['closed_issues_ratio'] = df['node.closedIssues.totalCount'] / df['node.totalIssues.totalCount']
    
    print('Razão entre Issues Fechadas e Total de Issues:')
    print(df['closed_issues_ratio'])


result = fetch_repository_data(100)
save_to_csv(result)

