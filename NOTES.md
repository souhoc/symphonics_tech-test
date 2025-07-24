# FRESH START

## Run
```sh
export GCP_PROJECT_ID=""
export BIGQUERY_TABLE_ID=""

uvicorn app.main:app
```

## Structure
```
symphonics
-- app
  -- endpoints
  -- models
  -- schemas
  -- services
  -- repositories
-- tests
-- requrements.txt
```

## Docs
- https://fastapi.tiangolo.com
  - https://fastapi.tiangolo.com/reference/dependencies/
  - https://fastapi.tiangolo.com/reference/exceptions/
  - https://fastapi.tiangolo.com/reference/dependencies/
  - https://fastapi.tiangolo.com/reference/parameters/
- https://www.uvicorn.org
- https://docs.pydantic.dev
  - https://docs.pydantic.dev/latest/concepts/config/#configuration-propagation
  - https://docs.pydantic.dev/latest/concepts/validators/
  - https://docs.pydantic.dev/latest/concepts/validation_decorator/
