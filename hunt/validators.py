def validate_hunting_place_data(data):
    errors = []
    name = data.get('name', '')
    character_levels = data.get('character_levels', '')
    hunt_type = data.get('hunt_type', '')
    exp_on_hour = data.get('exp_on_hour') if data.get('exp_on_hour') else 0
    exp_factor = data.get('exp_factor') if data.get('exp_factor') else 100
    gold_on_hour = data.get('gold_on_hour') if data.get('gold_on_hour') else None
    rune = data.get('rune', '')
    eq_with_resistance = data.get('eq_with_resistance', '')
    description = data.get('description', '')

    if not name:
       errors.append('Field name is required')
    if hunt_type not in ('solo', 'duo'):
        errors.append('Field hunt type can be set to solo or duo')

    try:
        exp_on_hour = int(exp_on_hour)
    except ValueError:
        errors.append('Field exp on hour must be a number')

    try:
        exp_factor = int(exp_factor)
    except ValueError:
        errors.append('Field exp factor must be a number')

    if gold_on_hour:
        try:
            gold_on_hour = int(gold_on_hour)
        except ValueError:
            errors.append('Fields gold on hour must be a number')

    if len(name) > 250:
        errors.append('Field name has more than 250 characters')
    if len(character_levels) > 50:
        errors.append('Field character levels has more than 50 characters')
    if len(rune) > 50:
        errors.append('Field rune has more than 50 characters')
    if len(eq_with_resistance) > 50:
        errors.append('Field equipment with resistance has more than 50 characters')

    return errors, {
        'name': name,
        'character_levels': character_levels,
        'hunt_type': hunt_type,
        'exp_on_hour': exp_on_hour,
        'exp_factor': exp_factor,
        'gold_on_hour': gold_on_hour,
        'rune': rune,
        'eq_with_resistance': eq_with_resistance,
        'description': description
    }
