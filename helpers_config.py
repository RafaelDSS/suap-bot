import subprocess


def get_ngrok_url_proxy():
    url_proxy = subprocess.run(
        'curl -s localhost:4040/api/tunnels | jq -r .tunnels[0].public_url',
        capture_output=True,
        text=True,
        shell=True).stdout
    # Remove o \n no final da string.
    url_proxy = url_proxy[:-1]
    return f'{url_proxy}/'