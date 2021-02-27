import importlib
import inspect
import pandas as pd

from typing import *

from .base_opportunity_filter import OpportunityFilter


class FiltersRunner:
    def __init__(self, filters_module_name):
        self.filters_module_name = filters_module_name

    def run(self,
            data: Dict[str, pd.DataFrame],
            ) -> Dict[str, Dict[str, Union[bool, int, float, str]]]:
        return {filter.name: filter.run(data) for filter in self.get_filters()}

    def get_filters(self) -> List[OpportunityFilter]:
        module = importlib.import_module(self.filters_module_name)
        filters = inspect.getmembers(module, lambda x: (isinstance(x, type)
                                                        and issubclass(x, OpportunityFilter)
                                                        and x != OpportunityFilter))
        return [cls for _, cls in filters]
