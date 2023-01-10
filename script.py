from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials


def main():
    site_url = input('Site url:')
    start_date = input('Start date:')
    end_date = input('End date:')
    key_file = input('Key file path:')
    scopes = ['https://www.googleapis.com/auth/webmasters.readonly']

    creds = Credentials.from_service_account_file(key_file, scopes=scopes)
    service = build('webmasters', 'v3', credentials=creds)

    body = {
        'startDate': start_date,
        'endDate': end_date,
        'dimensions': ['date', 'page']
    }
    response = service.searchanalytics().query(siteUrl=site_url, body=body).execute()
    if 'rows' in response:
        for row in response['rows']:
            print(row['page'])


if __name__ == '__main__':
    main()
