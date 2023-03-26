from pyngrok import ngrok, conf
import yaml
import subprocess
import requests

with open('start_conf.yaml', 'r') as stream:
    try:
        config = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        exit(-1)

conf.get_default().region = 'eu'
ngrok.set_auth_token(config['ngrok']['auth-token'])
mc_tunnel = ngrok.connect(25565, 'tcp')
server_ip = mc_tunnel.public_url.replace("tcp://", "")

print(f'✅  Opened the NGROK tunnel!\nThe ip is {server_ip}\n')

webhook = config['discord']['webhook']
webhook_request = requests.post(webhook, {
    "content": f"**The server is currently starting up!**\nAfter it starts, it will be available at\n\n`{server_ip}`",
    "username": config['discord']['username'],
})

if webhook_request.status_code - 200 < 10:
    print("✅  Message sent to Discord!\nStarting the server now...\n\n")
else:
    print("❌ Something went wrong when sending a message to Discord!")

subprocess.run(
    f'java -jar -Xmx{config["minecraft"]["max-mem"]} -Xms{config["minecraft"]["min-mem"]} {config["minecraft"]["jar-file"]} --nogui', shell=True, check=True)

print("✅  Server stopped and NGROK tunnel closed!")

webhook = config['discord']['webhook']
webhook_request = requests.post(webhook, {
    "content": f"**The server has been closed!**\nThe next time it starts, a new message with the new IP will be sent!",
    "username": config['discord']['username'],
})
