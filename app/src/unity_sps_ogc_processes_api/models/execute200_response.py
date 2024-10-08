# coding: utf-8

"""
    OGC API - Processes

    Example API Definition for OGC API - Processes

    The version of the OpenAPI document: 0.1
    Contact: info@ogc.org
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations

import re  # noqa: F401
from typing import Any, Dict, List, Union

from pydantic import FilePath, RootModel, field_validator

from unity_sps_ogc_processes_api.models.bbox import Bbox
from unity_sps_ogc_processes_api.models.link import Link
from unity_sps_ogc_processes_api.models.qualified_input_value import QualifiedInputValue

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class Execute200Response(RootModel):
    root: Union[
        Dict[
            str,
            Union[Bbox, List[Any], bool, float, int, str, Link, QualifiedInputValue],
        ],
        List[Any],
        bool,
        FilePath,
        float,
        int,
        Dict[str, Any],
        str,
    ]

    @field_validator("root")
    def validate_root(cls, v):
        if isinstance(v, dict):
            for key, value in v.items():
                if not isinstance(key, str):
                    raise ValueError(
                        f"Dictionary keys must be strings, got {type(key)}"
                    )
                if not isinstance(
                    value,
                    (Bbox, list, bool, float, int, str, Link, QualifiedInputValue),
                ):
                    raise ValueError(f"Invalid value type for key {key}: {type(value)}")
        return v

    @classmethod
    def from_dict(cls, obj: Dict[str, Any]) -> Self:
        return cls(root=obj)

    def to_dict(self) -> Dict[str, Any]:
        return self.root if isinstance(self.root, dict) else {"value": self.root}

    def __getattr__(self, name: str) -> Any:
        if isinstance(self.root, dict):
            return self.root.get(name)
        raise AttributeError(f"'Execute200Response' object has no attribute '{name}'")

    def __repr__(self) -> str:
        return f"Execute200Response({self.root!r})"
