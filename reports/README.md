# KUENTA Command Line Interface for Python Reports

## Requirements
1. python3 installed
2. Credentials: `--client_id` `--entity_id` `--cliente_secret`  
can be get it in the link: https://wiki.kuenta.net/books/desarrollo/page/documentacion-de-autenticacion-y-consumo-del-api-para-terceros 
3. Put the python executable under $HOME/ or a directory of your choice

## Usage

The command will make 4 attempts every 6 minutes to try to download the file. If the download is successful, the file will be saved by default in the directory where the command was executed or in a chosen directory if specified

- run the command `python3 api_client.py  --env [ENV] --client_id [client_id] --client_secret [cliente_secret] --after [Date-start] --before [Date-end] --entity_id [entity_id] `
- run the command `python3 api_client.py --help` for more info about [ENV] and download path

### Example
`python3 api_client.py  --env prod --client_id 000000-0000-0000-00000000 --client_secret 000000000000000aaaaaaa --after 2023-01-15 --before 2023-12-31 --entity_id 000000-0000-0000-00000000 `  