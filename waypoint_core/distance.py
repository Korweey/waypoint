"""
waypoint_core/distance.py
--------------------------
Distance value type for the Waypoint trail-finder.

Stores a magnitude (a non-negative number) and a unit
('km' or 'mi'). Provides a read-only accessor and a
convert() method to switch between units.
"""


class Distance:
    """
    Represents a trail distance with a magnitude and unit.

    Parameters:
        magnitude (float) : The distance value. Must be >= 0.
        unit      (str)   : The unit of measurement.
                            Must be 'km' or 'mi'.

    Raises:
        ValueError: If magnitude is negative.
        ValueError: If unit is not 'km' or 'mi'.
    """

    # Conversion factor between km and miles
    _KM_TO_MI = 0.621371
    _MI_TO_KM = 1.60934

    # Valid units
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
        # Validate magnitude — must not be negative
        if magnitude < 0:
            raise ValueError(
                f"Distance magnitude cannot be negative. "
                f"Got: {magnitude}"
            )

        # Validate unit — must be 'km' or 'mi'
        unit = unit.lower().strip()
        if unit not in self.VALID_UNITS:
            raise ValueError(
                f"Invalid unit '{unit}'. "
                f"Must be one of: {self.VALID_UNITS}"
            )

        # Store as private attributes (encapsulation)
        self._magnitude = float(magnitude)
        self._unit      = unit

    # --------------------------------------------------
    # Read-only accessor (property)
    # --------------------------------------------------

    @property
    def magnitude(self):
        """
        Read-only accessor for the distance magnitude.

        Returns:
            float: The distance value.
        """
        return self._magnitude

    @property
    def unit(self):
        """
        Read-only accessor for the distance unit.

        Returns:
            str: 'km' or 'mi'.
        """
        return self._unit

    # --------------------------------------------------
    # convert() — return a new Distance in the other unit
    # --------------------------------------------------

    def convert(self):
        """
        Convert this distance to the other unit and return
        a new Distance object. Does not modify self.

        Returns:
            Distance: A new Distance in the opposite unit.

        Example:
            Distance(5, 'km').convert() -> Distance(3.107, 'mi')
        """
        if self._unit == 'km':
            new_magnitude = self._magnitude * self._KM_TO_MI
            new_unit      = 'mi'
        else:
            new_magnitude = self._magnitude * self._MI_TO_KM
            new_unit      = 'km'

        return Distance(new_magnitude, new_unit)

    # --------------------------------------------------
    # String representations (stretch goal)
    # --------------------------------------------------

    def __str__(self):
        """
        Human-readable string representation.

        Returns:
            str: e.g. '5.00 km'
        """
        return f"{self._magnitude:.2f} {self._unit}"

    def __repr__(self):
        """
        Developer-friendly representation.

        Returns:
            str: e.g. "Distance(5.0, 'km')"
        """
        return f"Distance({self._magnitude!r}, {self._unit!r})"
