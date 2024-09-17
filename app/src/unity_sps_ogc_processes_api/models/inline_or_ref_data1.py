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
from typing import Dict, List, Optional, Union

from pydantic import BaseModel, ValidationError, field_validator
from typing_extensions import Literal

from unity_sps_ogc_processes_api.models.input_value_no_object1 import (
    InputValueNoObject1,
)
from unity_sps_ogc_processes_api.models.link import Link
from unity_sps_ogc_processes_api.models.qualified_input_value1 import (
    QualifiedInputValue1,
)

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

INLINEORREFDATA1_ONE_OF_SCHEMAS = [
    "InputValueNoObject1",
    "Link",
    "QualifiedInputValue1",
]


class InlineOrRefData1(BaseModel):
    """
    InlineOrRefData1
    """

    # data type: InputValueNoObject1
    oneof_schema_1_validator: Optional[InputValueNoObject1] = None
    # data type: QualifiedInputValue1
    oneof_schema_2_validator: Optional[QualifiedInputValue1] = None
    # data type: Link
    oneof_schema_3_validator: Optional[Link] = None
    actual_instance: Optional[Union[InputValueNoObject1, Link, QualifiedInputValue1]] = None
    one_of_schemas: List[str] = Literal["InputValueNoObject1", "Link", "QualifiedInputValue1"]

    model_config = {
        "validate_assignment": True,
        "protected_namespaces": (),
    }

    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError("If a position argument is used, only 1 is allowed to set `actual_instance`")
            if kwargs:
                raise ValueError("If a position argument is used, keyword arguments cannot be used.")
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @field_validator("actual_instance")
    def actual_instance_must_validate_oneof(cls, v):
        InlineOrRefData1.model_construct()
        error_messages = []
        match = 0
        # validate data type: InputValueNoObject1
        if not isinstance(v, InputValueNoObject1):
            error_messages.append(f"Error! Input type `{type(v)}` is not `InputValueNoObject1`")
        else:
            match += 1
        # validate data type: QualifiedInputValue1
        if not isinstance(v, QualifiedInputValue1):
            error_messages.append(f"Error! Input type `{type(v)}` is not `QualifiedInputValue1`")
        else:
            match += 1
        # validate data type: Link
        if not isinstance(v, Link):
            error_messages.append(f"Error! Input type `{type(v)}` is not `Link`")
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError(
                "Multiple matches found when setting `actual_instance` in InlineOrRefData1 with oneOf schemas: InputValueNoObject1, Link, QualifiedInputValue1. Details: "
                + ", ".join(error_messages)
            )
        elif match == 0:
            # no match
            raise ValueError(
                "No match found when setting `actual_instance` in InlineOrRefData1 with oneOf schemas: InputValueNoObject1, Link, QualifiedInputValue1. Details: "
                + ", ".join(error_messages)
            )
        else:
            return v

    @classmethod
    def from_dict(cls, obj: dict) -> Self:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Returns the object represented by the json string"""
        instance = cls.model_construct()
        error_messages = []
        match = 0

        # deserialize data into InputValueNoObject1
        try:
            instance.actual_instance = InputValueNoObject1.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into QualifiedInputValue1
        try:
            instance.actual_instance = QualifiedInputValue1.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into Link
        try:
            instance.actual_instance = Link.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError(
                "Multiple matches found when deserializing the JSON string into InlineOrRefData1 with oneOf schemas: InputValueNoObject1, Link, QualifiedInputValue1. Details: "
                + ", ".join(error_messages)
            )
        elif match == 0:
            # no match
            raise ValueError(
                "No match found when deserializing the JSON string into InlineOrRefData1 with oneOf schemas: InputValueNoObject1, Link, QualifiedInputValue1. Details: "
                + ", ".join(error_messages)
            )
        else:
            return instance

    def to_json(self) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        to_json = getattr(self.actual_instance, "to_json", None)
        if callable(to_json):
            return self.actual_instance.to_json()
        else:
            return json.dumps(self.actual_instance)

    def to_dict(self) -> Dict:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        to_dict = getattr(self.actual_instance, "to_dict", None)
        if callable(to_dict):
            return self.actual_instance.to_dict()
        else:
            # primitive type
            return self.actual_instance

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.model_dump())
