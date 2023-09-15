from pydantic import BaseModel


class CreateComputation(BaseModel):
    name: str
    parameter: int
