from __future__ import annotations

from enum import Enum, unique

from attrs import converters, define, field, validators

from ..name import SchemaName
from .base import SchemaBase
from .registry import SCHEMAS

__all__ = ["ShiftState", "IndicatorState", "Indicators", "AdditionalInfo", "VehicleState"]


@unique
class ShiftState(str, Enum):
    """An enum to represent gear shift state."""

    PARK = "PARK"
    REVERSE = "REVERSE"
    NEUTRAL = "NEUTRAL"
    HIGH = "HIGH"
    FORWARD = "FORWARD"
    LOW = "LOW"
    NONE = "NONE"


@unique
class IndicatorState(str, Enum):
    """An enum to represent indicator state."""

    ON = "on"
    OFF = "off"


@define
class Indicators:
    """A dataclass to represent state of each indicator.

    Attributes:
        left (IndicatorState): State of the left indicator.
        right (IndicatorState): State of the right indicator.
        hazard (IndicatorState): State of the hazard lights.
    """

    left: IndicatorState = field(converter=IndicatorState)
    right: IndicatorState = field(converter=IndicatorState)
    hazard: IndicatorState = field(converter=IndicatorState)


@define
class AdditionalInfo:
    """A dataclass to represent additional state information of the ego vehicle.

    Attributes:
        speed (float | None): Speed of the ego vehicle.
    """

    speed: float | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(float)),
    )


@define(slots=False)
@SCHEMAS.register(SchemaName.VEHICLE_STATE)
class VehicleState(SchemaBase):
    """A dataclass to represent schema table of `vehicle_state.json`.

    Attributes:
        token (str): Unique record identifier.
        timestamp (int): Unix time stamp.
        accel_pedal (float | None): Accel pedal position [%].
        brake_pedal (float | None): Brake pedal position [%].
        steer_pedal (float | None): Steering wheel position [%].
        steering_tire_angle (float | None): Steering tire angle [rad].
        steering_wheel_angle (float | None): Steering wheel angle [rad].
        shift_state (ShiftState | None): Gear shift state.
        indicators (Indicators | None): State of each indicator.
        additional_info (AdditionalInfo | None): Additional state information.
    """

    timestamp: int = field(validator=validators.instance_of(int))
    accel_pedal: float | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(float)),
    )
    brake_pedal: float | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(float)),
    )
    steer_pedal: float | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(float)),
    )
    steering_tire_angle: float | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(float)),
    )
    steering_wheel_angle: float | None = field(
        default=None,
        validator=validators.optional(validators.instance_of(float)),
    )
    shift_state: ShiftState | None = field(
        default=None,
        converter=converters.optional(ShiftState),
        validator=validators.optional(validators.instance_of(ShiftState)),
    )
    indicators: Indicators | None = field(
        default=None,
        converter=lambda x: Indicators(**x) if isinstance(x, dict) else x,
        validator=validators.optional(validators.instance_of(Indicators)),
    )
    additional_info: AdditionalInfo | None = field(
        default=None,
        converter=lambda x: AdditionalInfo(**x) if isinstance(x, dict) else x,
        validator=validators.optional(validators.instance_of(AdditionalInfo)),
    )
