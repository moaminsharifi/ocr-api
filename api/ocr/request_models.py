from pydantic import BaseModel, ValidationError, validator

import numpy as np
from typing import Deque, Dict, FrozenSet, List, Optional, Sequence, Set, Tuple, Union


class ProcessOcrRequest(BaseModel):
    image: str
