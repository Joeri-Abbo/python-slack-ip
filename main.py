import socket
import requests
import json
import yaml
import os

config = yaml.safe_load(open(os.path.dirname(__file__) + '/config.yml'))


def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        st.connect(('10.255.255.255', 1))
        ip = st.getsockname()[0]
    except Exception:
        ip = '127.0.0.1'
    finally:
        st.close()
    return ip


def send_to_slack(message):
    requests.post(
        config['slack']['webhook'], data=json.dumps({'text': message}),
        headers={'Content-Type': 'application/json'}
    )


if __name__ == '__main__':
    send_to_slack('Ip: ' + extract_ip())
