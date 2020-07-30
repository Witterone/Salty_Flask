import logging

from fastapi import APIRouter

import pandas as pd

from pydantic import BaseModel, Field, validator

import model

log = logging.getLogger(__name__)

router = APIRouter()



class Item(BaseModel):
    """Use this data model to parse the request body JSON."""

    
    comment_id : int = Field(..., example=23970146)
    user_name : str = Field(..., example='gmfawcett')
    

    def to_df(self):
        """Convert pydantic object to pandas dataframe with 1 row."""
        return pd.DataFrame([dict(self)])

    @validator('comment_id')
    def comment_id_must_be_positive(cls, value):
        """Validate that comment_id is a positive number."""
        assert value > 0, f'comment_id == {value}, must be > 0'
        return value




@router.post('/predict')
async def predict(item: Item):
    """Make random baseline predictions for classification problem."""
    X_new = item.to_df()
    log.info(X_new)
    
    y_pred = model.get_score_by_comment_id(item.comment_id)
    U_pred = model.get_cummulative_score_for_user(item.user_name)
    return {
        
        'Score for comment from id': y_pred,
        'user cumulative comment score': U_pred
    }
