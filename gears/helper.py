def step_to_big_gear(rotations_of_small_gear_for_one_big_gear_rotation, increment_of_small_gear_in_degrees):
    degrees_in_full_rotation = 360
    increments_in_one_rotation_of_small_gear = degrees_in_full_rotation / increment_of_small_gear_in_degrees
    increments_for_one_big_gear_rotation = increments_in_one_rotation_of_small_gear * rotations_of_small_gear_for_one_big_gear_rotation

    print(increments_for_one_big_gear_rotation)
    print(360/increments_for_one_big_gear_rotation)
    
rotations_of_small_gear_for_one_big_gear_rotation = 2.8125
increment_of_small_gear_in_degrees = 0.703125

step_to_big_gear(rotations_of_small_gear_for_one_big_gear_rotation, increment_of_small_gear_in_degrees)


def calculate_steps_for_degrees(steps_per_full_rotation, desired_degrees):
    """
    Calculate the number of steps needed to rotate a specific number of degrees.

    :param steps_per_full_rotation: Number of steps for a full 360-degree rotation.
    :param desired_degrees: The degrees of rotation desired.
    :return: The number of steps needed for the desired degrees of rotation.
    """
    # Calculating the fraction of a full rotation
    fraction_of_full_rotation = desired_degrees / 360

    # Calculating the number of steps for the desired degrees
    steps_for_desired_degrees = fraction_of_full_rotation * steps_per_full_rotation

    return steps_for_desired_degrees

# Example usage
steps_per_full_rotation = 512  # Example value, this should be the actual steps for a full rotation of your gear/motor
desired_degrees = 1  # Example: Number of degrees we want to rotate

# steps_needed = calculate_steps_for_degrees(steps_per_full_rotation, desired_degrees)
# print(steps_needed)
