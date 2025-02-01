from flask import Flask
from flask_restful import Api

from OrchestrationAdapter import OrchestrationAdapter
from controller.OrchestrationController import OrchestrationController

app = Flask(__name__)
api = Api(app)

orchestration_controller = OrchestrationController()

api.add_resource(OrchestrationAdapter, "/orchestrate",
                 resource_class_kwargs={'orchestration_controller': orchestration_controller})

if __name__ == "__main__":
    print("🚀 Flask API iniciando en http://127.0.0.1:8000")
    app.run(host="127.0.0.1", port=8000, debug=True)