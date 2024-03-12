import requests
import os
from dotenv import load_dotenv
import pandas as pd
import matplotlib.pyplot as plt

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
    df['repository_age'] = (pd.to_datetime('today').tz_localize(None) - df['createdAt']).dt.days / 365

    box_plot(df, 'repository_age', 'Idade dos Repositórios', 'Idade (anos)')

    grafico_dispersao(df, 'repository_age', 'node.stargazers.totalCount', 'Idade do Repositório (anos)', 'Número de Estrelas', 'Gráfico de Dispersão de Idade x Número de Estrelas')


def calculate_repositories_update(df):
    # Convert the 'updatedAt' column to datetime format
    df['updatedAt'] = pd.to_datetime(df['node.updatedAt'], utc=True)

    # Calculate the repository last update in days
    df['repository_update'] = (pd.Timestamp.utcnow() - df['updatedAt']).dt.days

    print("Idade mínima de atualização dos repositórios:", df['repository_update'].min())
    print("Idade máxima de atualização dos repositórios:", df['repository_update'].max())

    print(df['repository_update'])

    box_plot(df, 'repository_update', 'Idade da Última Atualização', 'Idade (dias)')

    grafico_dispersao(df, 'repository_update', 'node.stargazers.totalCount', 'Idade da Última Atualização (dias)', 'Número de Estrelas', 'Gráfico de Dispersão da Última Atualização x Número de Estrelas')



def calculate_pull_requests(df):
    df['node.pullRequests.totalCount']
    
    box_plot(df, 'node.pullRequests.totalCount', 'Número de Pull Requests', 'Número de Pull Requests')

    grafico_dispersao(df, 'node.pullRequests.totalCount', 'node.stargazers.totalCount', 'Número de Pull Requests', 'Número de Estrelas', 'Gráfico de Dispersão de Pull Requests x Número de Estrelas')


def calculate_releases(df):
    df['node.releases.totalCount']
    
    box_plot(df, 'node.releases.totalCount', 'Número de Releases', 'Número de Releases')

    grafico_dispersao(df, 'node.releases.totalCount', 'node.stargazers.totalCount', 'Número de Releases', 'Número de Estrelas', 'Gráfico de Dispersão de Releases x Número de Estrelas')
    

def calculate_popular_languages(df):
    popular_languages = df['node.primaryLanguage.name'].value_counts()

    plot_popular_languages_bar_chart(popular_languages)

    grafico_dispersao_popular_languages(df, 'node.primaryLanguage.name', 'node.stargazers.totalCount', 'Linguagens populares', 'Número de Estrelas', 'Gráfico de Dispersão de Linguagens Populares x Número de Estrelas')


def calculate_closed_issues_ratio(df):
    df['closed_issues_ratio'] = ((df['node.closedIssues.totalCount'] / df['node.totalIssues.totalCount']) * 100).round(2)
    
    plot_closed_issues_box_plot(df)

    grafico_dispersao(df, 'closed_issues_ratio', 'node.stargazers.totalCount', 'Razão de Issues Fechadas (%)', 'Número de Estrelas', 'Gráfico de Dispersão de Issues Fechadas x Número de Estrelas')


def box_plot(df, column, title, xlabel):
    plt.figure(figsize=(10, 6))
    plt.boxplot(df[column], vert=False)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.show()

def plot_popular_languages_bar_chart(popular_languages):
    plt.figure(figsize=(10, 6))
    popular_languages.plot(kind='bar')
    plt.title('Linguagens Mais Populares')
    plt.xlabel('Linguagem')
    plt.ylabel('Número de Repositórios')
    plt.show()

def plot_closed_issues_box_plot(df):
    plt.figure(figsize=(10, 6))
    plt.boxplot(df['node.closedIssues.totalCount'], vert=False)
    plt.title('Distribuição do Número de Issues Fechadas')
    plt.xlabel('Número de Issues Fechadas')
    plt.show()

def grafico_dispersao(df, coluna_x: str, coluna_y: str, label_x=None, label_y=None, title: str = ''):
    label_x = coluna_x if label_x is None else label_x
    label_y = coluna_y if label_y is None else label_y

    plt.figure(figsize=(10, 6))
    plt.scatter(df[coluna_x], df[coluna_y])
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.title(title)
    plt.grid(True)
    plt.show()

def grafico_dispersao_popular_languages(df, x_column, y_column, xlabel, ylabel, title):
    xlabel = x_column if xlabel is None else xlabel
    ylabel = y_column if ylabel is None else ylabel

    data_counts = df[x_column].value_counts().reset_index()
    data_counts.columns = [x_column, 'count']

    merged_df = pd.merge(df, data_counts, left_on=x_column, right_on=x_column)

    plt.figure(figsize=(12, 8)) 
    plt.scatter(merged_df[x_column], merged_df[y_column], s=50)  
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45) 
    plt.grid(True)
    plt.tight_layout() 
    plt.show()


def main():
    result = fetch_repository_data(1000)
    df = save_to_csv(result)

    calculate_repositories_age(df)
    calculate_repositories_update(df)
    calculate_pull_requests(df)
    calculate_releases(df)
    calculate_popular_languages(df)
    calculate_closed_issues_ratio(df)


main()
