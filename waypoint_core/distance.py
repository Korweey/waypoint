"""
waypoint_core/distance.py
--------------------------
Distance value type for the Waypoint trail-finder.

Week 8 update: operator overloading added.
    __add__  — Distance + Distance
    __sub__  — Distance - Distance
    __eq__   — Distance == Distance
    __lt__   — Distance < Distance
    __gt__   — Distance > Distance

Mixed-unit rule: when two Distance objects with different
units are combined, the right-hand operand is auto-converted
to match the left-hand unit before the operation. This keeps
the result unit predictable (always the left operand's unit).
"""


class Distance:
    """
    Represents a trail distance with a magnitude and unit.

    Parameters:
        magnitude (float) : The distance value. Must be >= 0.
        unit      (str)   : 'km' or 'mi'.

    Raises:
        ValueError: If magnitude is negative.
        ValueError: If unit is not 'km' or 'mi'.
    """

    _KM_TO_MI  = 0.621371
    _MI_TO_KM  = 1.60934
    VALID_UNITS = ('km', 'mi')

    def __init__(self, magnitude, unit):
        """
        Initialise a Distance, rejecting negatives and
        invalid units.

        Parameters:
            magnitude (float) : Distance value >= 0.
            unit      (str)   : 'km' or 'mi'.

        Returns: None
        """
        if magnitude < 0:
            raise ValueError(
                f"Distance magnitude cannot be negative. Got: {magnitude}"
            )
        unit = unit.lower().strip()
        if unit not in self.VALID_UNITS:
            raise ValueError(
                f"Invalid unit '{unit}'. Must be one of: {self.VALID_UNITS}"
            )
        self._magnitude = float(magnitude)
        self._unit      = unit

    # --------------------------------------------------
    # Read-only accessors
    # --------------------------------------------------

    @property
    def magnitude(self):
        """Return the distance magnitude. Returns: float"""
        return self._magnitude

    @property
    def unit(self):
        """Return the distance unit. Returns: str"""
        return self._unit

    # --------------------------------------------------
    # convert() — return new Distance in opposite unit
    # --------------------------------------------------

    def convert(self):
        """
        Convert to the other unit and return a new Distance.
        Does not modify self.

        Returns:
            Distance: New Distance in the opposite unit.
        """
        if self._unit == 'km':
            return Distance(self._magnitude * self._KM_TO_MI, 'mi')
        else:
            return Distance(self._magnitude * self._MI_TO_KM, 'km')

    # --------------------------------------------------
    # Helper: convert other to same unit as self
    # --------------------------------------------------

    def _to_same_unit(self, other):
        """
        Return other as a Distance in self's unit.
        If units already match, return other unchanged.

        Parameters:
            other (Distance) : The other Distance.

        Returns:
            Distance: other in self's unit.
        """
        if other.unit != self._unit:
            return other.convert()
        return other

    # --------------------------------------------------
    # Operator overloading (Week 8 — WP-202)
    # --------------------------------------------------

    def __add__(self, other):
        """
        Add two Distance objects. Mixed units: the right-hand
        operand is auto-converted to the left-hand unit.

        Parameters:
            other (Distance) : Distance to add.

        Returns:
            Distance: Sum in self's unit.

        Raises:
            TypeError: If other is not a Distance.
        """
        if not isinstance(other, Distance):
            return NotImplemented
        other = self._to_same_unit(other)
        return Distance(self._magnitude + other.magnitude, self._unit)

    def __sub__(self, other):
        """
        Subtract two Distance objects. Mixed units: auto-converted.
        Result is clamped to 0 if subtraction would go negative.

        Parameters:
            other (Distance) : Distance to subtract.

        Returns:
            Distance: Difference in self's unit (min 0).

        Raises:
            TypeError: If other is not a Distance.
        """
        if not isinstance(other, Distance):
            return NotImplemented
        other  = self._to_same_unit(other)
        result = self._magnitude - other.magnitude
        return Distance(max(0.0, result), self._unit)

    def __eq__(self, other):
        """
        Two Distance objects are equal if their magnitudes are
        equal after converting to the same unit.

        Parameters:
            other (Distance) : Distance to compare.

        Returns:
            bool: True if equal within floating-point tolerance.
        """
        if not isinstance(other, Distance):
            return NotImplemented
        other = self._to_same_unit(other)
        return abs(self._magnitude - other.magnitude) < 1e-6

    def __lt__(self, other):
        """
        Less-than comparison after unit alignment.

        Parameters:
            other (Distance) : Distance to compare.

        Returns:
            bool: True if self < other.
        """
        if not isinstance(other, Distance):
            return NotImplemented
        other = self._to_same_unit(other)
        return self._magnitude < other.magnitude

    def __gt__(self, other):
        """
        Greater-than comparison after unit alignment.

        Parameters:
            other (Distance) : Distance to compare.

        Returns:
            bool: True if self > other.
        """
        if not isinstance(other, Distance):
            return NotImplemented
        other = self._to_same_unit(other)
        return self._magnitude > other.magnitude

    # --------------------------------------------------
    # String representations
    # --------------------------------------------------

    def __str__(self):
        """Human-readable: '5.00 km'. Returns: str"""
        return f"{self._magnitude:.2f} {self._unit}"

    def __repr__(self):
        """Developer repr: Distance(5.0, 'km'). Returns: str"""
        return f"Distance({self._magnitude!r}, {self._unit!r})"
