from geoaggr import GeoAggr
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, StrictInt, StrictStr, StrictFloat
from typing import Union
import sys
import uvicorn


class SuccessResponse(BaseModel):
    aggr_type: StrictStr
    aggr_field: StrictStr
    result: Union[StrictInt, StrictFloat, StrictStr]


class ItemHexes(BaseModel):
    geometry: dict
    field: StrictStr
    aggr: StrictStr
    r: StrictInt


class ItemPolygon(BaseModel):
    geometry: dict
    field: StrictStr
    aggr: StrictStr


app = FastAPI()
geoaggr = GeoAggr()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    if not isinstance(exc.body, dict):
        detail = {"invalid_json": "You must set the request body as valid JSON"}
    else:
        missing_fields = []
        wrong_type_fields = []
        for elem in exc.errors():
            if elem["type"] == "type_error.str" or elem["type"] == "type_error.integer":
                wrong_type_fields.append(elem["loc"][1] + ': ' + elem['msg'])
            else:
                missing_fields.append(elem["loc"][1])

        if missing_fields and wrong_type_fields:
            detail = {"missing_fields": f'You have missing fields in request body JSON - {", ".join(missing_fields)}',
                      "wrong_types": f'You have wrong types of fields in request body JSON - {", ".join(wrong_type_fields)}'}
        elif missing_fields:
            detail = {"missing_fields": f'You have missing fields in request body JSON - {", ".join(missing_fields)}'}
        elif wrong_type_fields:
            detail = {"wrong_types": f'You have wrong types of fields in request body JSON - {", ".join(wrong_type_fields)}'}

    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                        content=jsonable_encoder({"detail": detail}))


@app.post("/aggr_hexes", response_class=JSONResponse)
async def aggr_hexs(data: ItemHexes):
    try:
        result = SuccessResponse(aggr_type=data.aggr, aggr_field=data.field,
                                 result=geoaggr.aggr_hexs(data.geometry, data.field, data.aggr, data.r))
    except ValueError as error:
        raise HTTPException(status_code=422, detail=eval(str(error)))

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(result))


@app.post("/aggr_polygon", response_class=JSONResponse)
async def aggr_polygon(data: ItemPolygon):
    try:
        result = SuccessResponse(aggr_type=data.aggr, aggr_field=data.field,
                                 result=geoaggr.aggr_polygon(data.geometry, data.field, data.aggr))
    except ValueError as error:
        raise HTTPException(status_code=422, detail=eval(str(error)))

    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=jsonable_encoder(result))


if __name__ == "__main__":
    host = sys.argv[1]
    uvicorn.run("main:app", host=host, port=8000, reload=True)
