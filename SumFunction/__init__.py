import logging
import json
import uuid
import azure.functions as func

def main(req: func.HttpRequest, cosmosDB: func.Out[func.Document]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        x = req_body.get('x')
        y = req_body.get('y')
        id_usuario = req_body.get('id_usuario')
    except (ValueError, AttributeError):
        try:
            x = req.params.get('x')
            y = req.params.get('y')
            id_usuario = req.params.get('id_usuario')
        except AttributeError:
            return func.HttpResponse(
                "Please pass x, y and id_usuario in the query string or in the request body",
                status_code=400
            )

    if not id_usuario:
        logging.warning("id_usuario not provided. Using default value.")
        id_usuario = "default_user"

    if x is not None and y is not None:
        try:
            x_float = float(x)
            y_float = float(y)
            z = x_float + y_float

            doc = {
                'id': str(uuid.uuid4()),
                'x': x_float,
                'y': y_float,
                'z': z,
                'id_usuario': id_usuario
            }
            
            cosmosDB.set(func.Document.from_dict(doc))

            return func.HttpResponse(json.dumps({'z': z}))
        except ValueError:
            return func.HttpResponse(
                "Invalid input. Please provide numbers for x and y.",
                status_code=400
            )
    else:
        return func.HttpResponse(
             "Please pass x and y on the query string or in the request body",
             status_code=400
        )
