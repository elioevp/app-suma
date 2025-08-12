import logging
import json
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        x = req_body.get('x')
        y = req_body.get('y')
    except (ValueError, AttributeError):
        try:
            x = req.params.get('x')
            y = req.params.get('y')
        except AttributeError:
            return func.HttpResponse(
                "Please pass x and y in the query string or in the request body",
                status_code=400
            )

    if x is not None and y is not None:
        try:
            x_float = float(x)
            y_float = float(y)
            z = x_float + y_float
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
