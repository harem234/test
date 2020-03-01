import connexion
app = connexion.FlaskApp(__name__, specification_dir='openapi/')
app.add_api('swagger.yaml')
# (test) D:\Projects\flask\test\openapi>   connexion run -dv swagger.yaml

if __name__ == '__main__':
    app.run()
