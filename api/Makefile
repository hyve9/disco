NETWORK=disco
PG_PASS=
PG_USER=postgres

network:
	-docker network create $(NETWORK)

run-postgres: network
	docker run -d -e POSTGRES_PASSWORD=$(PG_PASS) -e POSTGRES_USER=$(PG_USER) --network $(NETWORK) -p 5432:5432 -v $(CURDIR)/initdb:/docker-entrypoint-initdb.d --name pg_api postgres:latest

run-node: run-postgres
	npm start

cleanup:
	-npm stop
	-docker kill pg_api
	-docker rm pg_api
	-docker network remove $(NETWORK)
