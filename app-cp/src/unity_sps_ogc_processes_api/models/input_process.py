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

import json
import pprint
import re  # noqa: F401
from typing import Any, ClassVar, Dict, List, Optional

from pydantic import BaseModel, Field, StrictStr

from unity_sps_ogc_processes_api.models.fields_modifiers_properties import (
    FieldsModifiersProperties,
)
from unity_sps_ogc_processes_api.models.output_workflows1 import OutputWorkflows1
from unity_sps_ogc_processes_api.models.subscriber import Subscriber

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self


class InputProcess(BaseModel):
    """
    InputProcess
    """  # noqa: E501

    process: StrictStr = Field(
        description="URI to the process execution end point (i.e., `.../processes/{processId}/execution`)"
    )
    inputs: Optional[Dict[str, InputWorkflows1]] = None
    outputs: Optional[Dict[str, OutputWorkflows1]] = None
    subscriber: Optional[Subscriber] = None
    filter: Optional[StrictStr] = None
    properties: Optional[FieldsModifiersProperties] = None
    sort_by: Optional[List[StrictStr]] = Field(default=None, alias="sortBy")
    __properties: ClassVar[List[str]] = [
        "process",
        "inputs",
        "outputs",
        "subscriber",
        "filter",
        "properties",
        "sortBy",
    ]

    model_config = {
        "populate_by_name": True,
        "validate_assignment": True,
        "protected_namespaces": (),
    }

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of InputProcess from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        _dict = self.model_dump(
            by_alias=True,
            exclude={},
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of each value in inputs (dict)
        _field_dict = {}
        if self.inputs:
            for _key in self.inputs:
                if self.inputs[_key]:
                    _field_dict[_key] = self.inputs[_key].to_dict()
            _dict["inputs"] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of each value in outputs (dict)
        _field_dict = {}
        if self.outputs:
            for _key in self.outputs:
                if self.outputs[_key]:
                    _field_dict[_key] = self.outputs[_key].to_dict()
            _dict["outputs"] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of subscriber
        if self.subscriber:
            _dict["subscriber"] = self.subscriber.to_dict()
        # override the default output from pydantic by calling `to_dict()` of properties
        if self.properties:
            _dict["properties"] = self.properties.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Dict) -> Self:
        """Create an instance of InputProcess from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate(
            {
                "process": obj.get("process"),
                "inputs": (
                    dict(
                        (_k, InputWorkflows1.from_dict(_v))
                        for _k, _v in obj.get("inputs").items()
                    )
                    if obj.get("inputs") is not None
                    else None
                ),
                "outputs": (
                    dict(
                        (_k, OutputWorkflows1.from_dict(_v))
                        for _k, _v in obj.get("outputs").items()
                    )
                    if obj.get("outputs") is not None
                    else None
                ),
                "subscriber": (
                    Subscriber.from_dict(obj.get("subscriber"))
                    if obj.get("subscriber") is not None
                    else None
                ),
                "filter": obj.get("filter"),
                "properties": (
                    FieldsModifiersProperties.from_dict(obj.get("properties"))
                    if obj.get("properties") is not None
                    else None
                ),
                "sortBy": obj.get("sortBy"),
            }
        )
        return _obj


from unity_sps_ogc_processes_api.models.input_workflows1 import InputWorkflows1

# TODO: Rewrite to not use raise_errors
InputProcess.model_rebuild(raise_errors=False)
