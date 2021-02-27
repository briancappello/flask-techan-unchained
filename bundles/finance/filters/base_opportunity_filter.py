import pandas as pd

from typing import *


class OpportunityFilterNameDescriptor:
    def __get__(self, instance, cls):
        return ''.join(cls.__name__.rsplit("Filter", 1))


class OpportunityFilter:
    name = OpportunityFilterNameDescriptor()

    @classmethod
    def run(cls, df: Dict[str, pd.DataFrame]) -> List[str]:
        raise NotImplementedError
