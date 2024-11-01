image:
	docker build -t recapcha-solver .

run:
	docker run -d --rm --name recapcha-solver -p 9987:9987 recapcha-solver 