"""XP rules"""


def calculate_xp(minutes):
    # one minute is one XP
    """
    Convert practice minutes directly to XP, with no bonus multiplier.
    """
    return minutes


def xp4next_level(level):
    # 50 XP for the first jump, then 25 more for each later jump
    """
    Return the next upgrade cost: 50 XP at level one, then 25 more per
    level.
    """
    return 50 + (level - 1) * 25


def caculate_level(total_xp):
    # take away XP used by old levels; what is left goes in the progress bar
    """
    Subtract completed level costs and return the level, remaining XP and
    next cost.
    """
    level = 1
    remaining = total_xp
    needed = xp4next_level(level)
    while remaining >= needed:
        remaining =remaining- needed
        level =level + 1
        needed = xp4next_level(level)
    return level, remaining, needed


def calculate_level(total_xp):
    """
    Return just the level from the full XP calculation.
    """
    return caculate_level(total_xp)[0]
