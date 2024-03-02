import requests
import os
from dotenv import load_dotenv
import json
import pandas as pd

load_dotenv()

API_KEY = os.getenv("API_KEY")
api_url = 'https://api.github.com/graphql'

headers = {'Authorization': 'Bearer %s' % API_KEY}
allResults = {"resultados": []}


def run_query(numRepos):
  endCursor = None

  for i in range (int(numRepos/20)):
      variables = {
        "endCursor": endCursor
      }
      query = """
    query ($endCursor: String) {
      search(query: "stars:>1", type: REPOSITORY, first: 20, after: $endCursor) {
    edges {
      node {
        ... on Repository {
          name
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
      
    }pageInfo {
        endCursor
        hasNextPage
      }
  }
}
"""    
      request = requests.post(
        url=api_url, json={'query': query, 'variables': variables}, headers=headers)
      resp = request.json()
      allResults["resultados"].append(resp)
      endCursor = resp['data']['search']['pageInfo']['endCursor']

    
  if request.status_code == 200:
      return allResults
  else:
      raise Exception("Query failed to run by returning code of {}. {}".format(
          request.status_code, query))




numRespos = 100
result = run_query(numRespos)
print(result)
# Create the directory if not exists
os.makedirs('scripts/dataset/json', exist_ok=True)

# Save the result in a json archive
with open('scripts/dataset/json/data.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# Load the json file
with open('scripts/dataset/json/data.json', 'r') as f:
    data = json.load(f)

# Create a dataframe
df = pd.json_normalize(data['data']['search']['edges'])

# Save the dataframe in a csv file
df.to_csv('scripts/dataset/csv/data.csv', index=False)