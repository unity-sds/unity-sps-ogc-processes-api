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
from typing import Any, Dict, List, Optional, Union

from pydantic import (
    BaseModel,
    StrictBool,
    StrictBytes,
    StrictFloat,
    StrictInt,
    StrictStr,
    ValidationError,
    field_validator,
)
from typing_extensions import Literal

from unity_sps_ogc_processes_api.models.bbox1 import Bbox1
from unity_sps_ogc_processes_api.models.input_collection import InputCollection
from unity_sps_ogc_processes_api.models.input_parameterized import InputParameterized

try:
    from typing import Self
except ImportError:
    from typing_extensions import Self

INPUTVALUENOOBJECTWORKFLOWS_ONE_OF_SCHEMAS = [
    "Bbox1",
    "InputCollection",
    "InputParameterized",
    "InputProcess",
    "List[object]",
    "bool",
    "float",
    "int",
    "str",
]


class InputValueNoObjectWorkflows(BaseModel):
    """
    InputValueNoObjectWorkflows
    """

    # data type: str
    oneof_schema_1_validator: Optional[StrictStr] = None
    # data type: float
    oneof_schema_2_validator: Optional[Union[StrictFloat, StrictInt]] = None
    # data type: int
    oneof_schema_3_validator: Optional[StrictInt] = None
    # data type: bool
    oneof_schema_4_validator: Optional[StrictBool] = None
    # data type: List[object]
    oneof_schema_5_validator: Optional[List[Dict[str, Any]]] = None
    # data type: str
    oneof_schema_6_validator: Optional[Union[StrictBytes, StrictStr]] = None
    # data type: Bbox1
    oneof_schema_7_validator: Optional[Bbox1] = None
    # data type: InputCollection
    oneof_schema_8_validator: Optional[InputCollection] = None
    # data type: InputProcess
    oneof_schema_9_validator: Optional[InputProcess] = None
    # data type: InputParameterized
    oneof_schema_10_validator: Optional[InputParameterized] = None
    actual_instance: Optional[
        Union[
            Bbox1,
            InputCollection,
            InputParameterized,
            InputProcess,
            List[object],
            bool,
            float,
            int,
            str,
        ]
    ] = None
    one_of_schemas: List[str] = Literal[
        "Bbox1",
        "InputCollection",
        "InputParameterized",
        "InputProcess",
        "List[object]",
        "bool",
        "float",
        "int",
        "str",
    ]

    model_config = {
        "validate_assignment": True,
        "protected_namespaces": (),
    }

    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError(
                    "If a position argument is used, only 1 is allowed to set `actual_instance`"
                )
            if kwargs:
                raise ValueError(
                    "If a position argument is used, keyword arguments cannot be used."
                )
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @field_validator("actual_instance")
    def actual_instance_must_validate_oneof(cls, v):
        instance = InputValueNoObjectWorkflows.model_construct()
        error_messages = []
        match = 0
        # validate data type: str
        try:
            instance.oneof_schema_1_validator = v
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # validate data type: float
        try:
            instance.oneof_schema_2_validator = v
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # validate data type: int
        try:
            instance.oneof_schema_3_validator = v
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # validate data type: bool
        try:
            instance.oneof_schema_4_validator = v
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # validate data type: List[object]
        try:
            instance.oneof_schema_5_validator = v
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # validate data type: str
        try:
            instance.oneof_schema_6_validator = v
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # validate data type: Bbox1
        if not isinstance(v, Bbox1):
            error_messages.append(f"Error! Input type `{type(v)}` is not `Bbox1`")
        else:
            match += 1
        # validate data type: InputCollection
        if not isinstance(v, InputCollection):
            error_messages.append(
                f"Error! Input type `{type(v)}` is not `InputCollection`"
            )
        else:
            match += 1
        # validate data type: InputProcess
        if not isinstance(v, InputProcess):
            error_messages.append(
                f"Error! Input type `{type(v)}` is not `InputProcess`"
            )
        else:
            match += 1
        # validate data type: InputParameterized
        if not isinstance(v, InputParameterized):
            error_messages.append(
                f"Error! Input type `{type(v)}` is not `InputParameterized`"
            )
        else:
            match += 1
        if match > 1:
            # more than 1 match
            raise ValueError(
                "Multiple matches found when setting `actual_instance` in InputValueNoObjectWorkflows with oneOf schemas: Bbox1, InputCollection, InputParameterized, InputProcess, List[object], bool, float, int, str. Details: "
                + ", ".join(error_messages)
            )
        elif match == 0:
            # no match
            raise ValueError(
                "No match found when setting `actual_instance` in InputValueNoObjectWorkflows with oneOf schemas: Bbox1, InputCollection, InputParameterized, InputProcess, List[object], bool, float, int, str. Details: "
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

        # deserialize data into str
        try:
            # validation
            instance.oneof_schema_1_validator = json.loads(json_str)
            # assign value to actual_instance
            instance.actual_instance = instance.oneof_schema_1_validator
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into float
        try:
            # validation
            instance.oneof_schema_2_validator = json.loads(json_str)
            # assign value to actual_instance
            instance.actual_instance = instance.oneof_schema_2_validator
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into int
        try:
            # validation
            instance.oneof_schema_3_validator = json.loads(json_str)
            # assign value to actual_instance
            instance.actual_instance = instance.oneof_schema_3_validator
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into bool
        try:
            # validation
            instance.oneof_schema_4_validator = json.loads(json_str)
            # assign value to actual_instance
            instance.actual_instance = instance.oneof_schema_4_validator
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into List[object]
        try:
            # validation
            instance.oneof_schema_5_validator = json.loads(json_str)
            # assign value to actual_instance
            instance.actual_instance = instance.oneof_schema_5_validator
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into str
        try:
            # validation
            instance.oneof_schema_6_validator = json.loads(json_str)
            # assign value to actual_instance
            instance.actual_instance = instance.oneof_schema_6_validator
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into Bbox1
        try:
            instance.actual_instance = Bbox1.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into InputCollection
        try:
            instance.actual_instance = InputCollection.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into InputProcess
        try:
            instance.actual_instance = InputProcess.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into InputParameterized
        try:
            instance.actual_instance = InputParameterized.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError(
                "Multiple matches found when deserializing the JSON string into InputValueNoObjectWorkflows with oneOf schemas: Bbox1, InputCollection, InputParameterized, InputProcess, List[object], bool, float, int, str. Details: "
                + ", ".join(error_messages)
            )
        elif match == 0:
            # no match
            raise ValueError(
                "No match found when deserializing the JSON string into InputValueNoObjectWorkflows with oneOf schemas: Bbox1, InputCollection, InputParameterized, InputProcess, List[object], bool, float, int, str. Details: "
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


from unity_sps_ogc_processes_api.models.input_process import InputProcess

# TODO: Rewrite to not use raise_errors
InputValueNoObjectWorkflows.model_rebuild(raise_errors=False)