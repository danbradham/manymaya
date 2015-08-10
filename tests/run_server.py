from manymaya.server import Server

if __name__ == "__main__":
    Server(
        8081,
        authkey="test_key"
        ).start()
