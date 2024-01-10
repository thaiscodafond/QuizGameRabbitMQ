.PHONY: run

run_client:
	cd client_side && node client_side_server.js

run_server:
	cd game_engine && python3 main.py

