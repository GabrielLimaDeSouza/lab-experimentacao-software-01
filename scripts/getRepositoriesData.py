import requests
import os
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

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
                        stargazers{
                            totalCount
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

    return df


def calculate_repositories_age(df):
    # Convert the 'createdAt' column to datetime format
    df['createdAt'] = pd.to_datetime(df['node.createdAt']).dt.tz_localize(None)

    # Calculate the repository age in days
    df['repository_age'] = (pd.to_datetime('today').tz_localize(None) - df['createdAt']).dt.days

    plot_repositories_age_box_plot(df)


def calculate_repositories_update(df):
    # Convert the 'updatedAt' column to datetime format
    df['updatedAt'] = pd.to_datetime(df['node.updatedAt'], utc=True)

    # Calculate the repository last update in days
    df['repository_update'] = (pd.Timestamp.utcnow() - df['updatedAt']).dt.days

    print("Idade mínima de atualização dos repositórios:", df['repository_update'].min())
    print("Idade máxima de atualização dos repositórios:", df['repository_update'].max())

    print(df['repository_update'])


def calculate_pull_requests(df):
    df['node.pullRequests.totalCount']
    
    plot_pull_requests_box_plot(df)


def calculate_releases(df):
    df['node.releases.totalCount']
    
    plot_releases_box_plot(df)
    

def calculate_popular_languages(df):
    popular_languages = df['node.primaryLanguage.name'].value_counts()

    plot_popular_languages_bar_chart(popular_languages)


def calculate_closed_issues_ratio(df):
    df['closed_issues_ratio'] = ((df['node.closedIssues.totalCount'] / df['node.totalIssues.totalCount']) * 100).round(2)
    
    plot_closed_issues_box_plot(df)


def plot_repositories_age_box_plot(df):
    plt.figure(figsize=(10, 6))
    plt.boxplot(df['repository_age'], vert=False)
    plt.title('Distribuição da Idade dos Repositórios')
    plt.xlabel('Idade (dias)')
    plt.show()


def plot_popular_languages_bar_chart(popular_languages):
    plt.figure(figsize=(10, 6))
    popular_languages.plot(kind='bar')
    plt.title('Linguagens Mais Populares')
    plt.xlabel('Linguagem')
    plt.ylabel('Número de Repositórios')
    plt.show()


def plot_pull_requests_box_plot(df):
    plt.figure(figsize=(10, 6))
    plt.boxplot(df['node.pullRequests.totalCount'], vert=False)
    plt.title('Distribuição do Número de Pull Requests')
    plt.xlabel('Número de Pull Requests')
    plt.show()


def plot_releases_box_plot(df):
    plt.figure(figsize=(10, 6))
    plt.boxplot(df['node.releases.totalCount'], vert=False)
    plt.title('Distribuição do Número de Releases')
    plt.xlabel('Número de Releases')
    plt.show()


def plot_closed_issues_box_plot(df):
    plt.figure(figsize=(10, 6))
    plt.boxplot(df['node.closedIssues.totalCount'], vert=False)
    plt.title('Distribuição do Número de Issues Fechadas')
    plt.xlabel('Número de Issues Fechadas')
    plt.show()


def main():
    result = fetch_repository_data(100)
    df = save_to_csv(result)

    calculate_repositories_age(df)
    calculate_repositories_update(df)
    calculate_pull_requests(df)
    calculate_releases(df)
    calculate_popular_languages(df)
    calculate_closed_issues_ratio(df)


main()
