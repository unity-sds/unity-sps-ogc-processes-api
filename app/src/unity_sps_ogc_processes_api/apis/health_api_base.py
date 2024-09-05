from abc import ABC, abstractmethod
from typing import ClassVar, Tuple

from unity_sps_ogc_processes_api.models.health_check import HealthCheck


class BaseHealthApi(ABC):
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseHealthApi.subclasses = BaseHealthApi.subclasses + (cls,)

    @abstractmethod
    def get_health(self) -> HealthCheck:
        """
        Get the health status of the API.

        Returns:
            HealthCheck: The health status of the API.
        """
        pass
