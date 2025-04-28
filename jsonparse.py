import random

def parse_value(value):
    """Parse loot values, handling random ranges."""
    if isinstance(value, str) and value.startswith('random(') and value.endswith(')'):
        nums = value[7:-1].split(',')
        return random.randint(int(nums[0]), int(nums[1]))
    return value