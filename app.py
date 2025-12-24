import connexion

app = connexion.App(__name__, specification_dir="./static")
app.add_api("swagger.yml")

application = app.app

if __name__ == "__main__":
    application.run(debug=True)
