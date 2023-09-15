from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from celery.result import AsyncResult
import logging
from celery.signals import after_setup_logger

from app.api.dependencies import get_analytics_db
from app.db.models import Computation as ComputationDB
from app.schemas.computation import CreateComputation as CreateComputationSchema

from app.tasks import celery_tasks

logging.basicConfig(level=logging.INFO, format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

router = APIRouter()


@after_setup_logger.connect
def setup_celery_logger(logger, *args, **kwargs):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("tasks")


class TaskOut(BaseModel):
    id: str
    status: str


def map_computations_list_to_dict_list(computations_list) -> List[dict]:
    return [
        computation.__dict__ for computation in computations_list
    ]


def _to_task_out(r: AsyncResult) -> TaskOut:
    return TaskOut(id=r.task_id, status=r.status)


@router.get(
    "/computations",
    summary="Retrieves Computations",
)
def get_computations(
    db: Session = Depends(get_analytics_db),
):
    return map_computations_list_to_dict_list(db.query(ComputationDB).all())


@router.post(
    "/computations",
    summary="Add Computations",
)
def add_computation(
        computation: CreateComputationSchema,
        db: Session = Depends(get_analytics_db),
):
    try:
        if computation.parameter > 5:
            r = celery_tasks.slow_dummy_task.delay(computation.parameter)
        else:
            r = celery_tasks.fast_dummy_task.delay(computation.parameter)

        # Make sure computation id is task id
        comp_dict = computation.dict()
        comp_dict['id'] = str(r.id)
        db_obj = ComputationDB(**comp_dict)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        logger.info("Successfully added new computation")
    except Exception as e:
        logger.error(f"Exception adding new computation:  {e}")


@router.get("/computations_status")
def status(computation_id: str) -> TaskOut:
    r = AsyncResult(computation_id)
    return _to_task_out(r)


@router.delete("/computations", summary="Stop task and delete computation")
def delete(
    computation_id: str,
    db: Session = Depends(get_analytics_db)
):
    try:
        AsyncResult(computation_id).revoke(terminate=True, signal="SIGKILL")
        comp_to_be_deleted = db.query(ComputationDB).where(ComputationDB.id == computation_id).first()
        db.delete(comp_to_be_deleted)
        db.commit()

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"failed with {e}"
        )
