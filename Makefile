NETWORK=disco
SITE=website
AUTH_TOKEN=$(shell pass show dev/ngrok.io)
QR="qrcode.png"
AUDIO="audio/type.wav"

network: 
	-docker network create $(NETWORK)

build-webserver:
	docker build -t hyve9/disco .

run-webserver: network build-webserver
	docker run -d -p 80 --network $(NETWORK) --name $(SITE) hyve9/disco 

run-ngrok: run-webserver
	docker run -d -p 4040:4040 --network $(NETWORK) --name ngrok wernight/ngrok ngrok http $(SITE):80 --authtoken $(AUTH_TOKEN)
	sleep 3
print-ngrok: 
	curl 0.0.0.0:4040/api/tunnels | jq ".tunnels[0].public_url"
show-qr: run-ngrok
	python makeqr.py $(QR)
	gwenview $(QR)

player:
	pasuspender -- disco-player.py [URL] $(AUDIO)

cleanup:
	-docker kill ngrok $(SITE)
	-docker rm ngrok $(SITE)
	-docker network remove $(NETWORK)
