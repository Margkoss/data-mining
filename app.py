from src.main import bootstrap_application

if __name__ == "__main__":
    bootstrap_application()
else:
    raise Exception("Cannot be imported, meant as standalone")
