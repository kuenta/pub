import requests
import argparse
import time

print('running')

if __name__ == "__main__":

  parser = argparse.ArgumentParser(description='API for export credits.')

  parser.add_argument('--env', type=str, help='optional - environment where the api run - test stage demo prod - default localhost ')
  parser.add_argument('--client_id', type=str, help='')
  parser.add_argument('--client_secret', type=str, help='')
  parser.add_argument('--before', type=str, help='format yyyy-mm-dd')
  parser.add_argument('--after', type=str, help='format yyyy-mm-dd')
  parser.add_argument('--entity_id', type=str, help='')
  parser.add_argument('--path', type=str, help='optional - path to save file - /path/to/save/ - /path/to/save/renameFile.csv (end with ´.csv´ is required)')

  args = parser.parse_args()

  env = 'local' if args.env is None else args.env
  client_id = args.client_id
  client_secret = args.client_secret
  entity_id = args.entity_id
  auth_url = 'https://test-auth-api.kuenta.co/v1/oauth/token'
  api_url = 'https://localhost:3443'
  before = args.before
  after = args.after
  file_path = args.path


  if not client_id is None and not client_secret is None and not before is None and not after is None and not entity_id is None :
    if env == 'stage' :
      auth_url = "https://stage-auth-api.kuenta.co/v1/oauth/token"
      api_url = 'https://stage-api.kuenta.co'
    elif env == 'test' :
      auth_url = 'https://test-auth-api.kuenta.co/v1/oauth/token'
      api_url = 'https://test-api.kuenta.co'
    elif env == 'demo' :
      auth_url = "https://demo-auth-api.kuenta.co/v1/oauth/token"
      api_url = 'https://demo-api.kuenta.co'
    elif env == 'prod' :
      auth_url = "https://auth-api.kuenta.co/v1/oauth/token"
      api_url = 'https://api.kuenta.co'

    login_data = {
      'grant_type': 'client_credentials',
      'client_id': client_id,
      'client_secret': client_secret
    }
    login_response = requests.post(auth_url, data=login_data, verify=False)

    #valid login
    if login_response.status_code == 200:
      token = login_response.json()['access_token']
      headers = {
        'Authorization': f"Bearer {token}",
        'Config-Organization-ID': entity_id,
        'Organization-ID': entity_id
      }

      before = f"{before}T23:59:59-05:00" if not ("T" in before) else before
      after = f"{after}T00:00:00-05:00" if not ("T" in after) else after

      response = requests.get(f"{api_url}/v1/export/receivables?before={before}&after={after}", headers=headers, verify=False)

      if response.status_code == 200:
        retry_download = True
        tries = 0
        current_date = time.strftime("%Y-%m-%d", time.localtime())

        while retry_download and tries < 4:
          print(f'try #{tries}')

          time.sleep(500)
          response_exports = requests.get(f"{api_url}/v1/export/orders/receivables", headers=headers, verify=False)

          if response_exports.status_code == 200:
            exports = response_exports.json()

            for export in exports:
              if current_date in export.get('createdAt') and export.get('after')==after and export.get('before')==before and export.get('status')==1 and export.get('exportType')=="1":
                response_receivable = requests.get(f"{api_url}/v1/export/orders/file/{export.get('fileID')}", headers=headers, verify=False)

                if response_receivable.status_code == 200:
                  export_after = export.get('after').split('T')[0]
                  export_before = export.get('before').split('T')[0]

                  if file_path is None:
                    file_name = f"creditos_{export_after}_{export_before}.csv"
                  elif file_path.endswith('.csv'):
                    file_name = file_path
                  elif file_path.endswith('/'):
                    file_name = f"{file_path}creditos_{export_after}_{export_before}.csv"
                  else:
                    file_name = f"{file_path}/creditos_{export_after}_{export_before}.csv"

                  with open(file_name, 'wb') as file:
                    file.write(response_receivable.content)
                    print('File Generated')

                  retry_download = False
                else:
                  print('Error descargando el archivo. Intentando nuevamente.')
                  print(response_receivable.content)
                break

            if retry_download == True:
              tries = tries + 1
          else:
            tries = tries + 1
            print(f"Error al exportar el archivo: {response_exports.json()}")
      else:
        print(f"Error al exportar el archivo: {response.json()}")
    else:
      print('Error al iniciar sesión')
  else:
    print('Params missing.. run with --help')
