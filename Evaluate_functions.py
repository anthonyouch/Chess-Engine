def isolated_pawns(pawn_locations):
    """given a chess board find all the isolated pawns """
    column = [0 for _ in range(8)]
    for pawn in pawn_locations:
        column[pawn % 8] += 1

    isolated_pawn_count = 0

    if column[0] >= 1 and column[1] == 0:
        isolated_pawn_count += column[0]
    if column[1] >= 1 and column[0] == 0 and column[2] == 0:
        isolated_pawn_count += column[1]
    if column[2] >= 1 and column[1] == 0 and column[3] == 0:
        isolated_pawn_count += column[2]
    if column[3] >= 1 and column[2] == 0 and column[4] == 0:
        isolated_pawn_count += column[3]
    if column[4] >= 1 and column[3] == 0 and column[5] == 0:
        isolated_pawn_count += column[4]
    if column[5] >= 1 and column[4] == 0 and column[6] == 0:
        isolated_pawn_count += column[5]
    if column[6] >= 1 and column[5] == 0 and column[7] == 0:
        isolated_pawn_count += column[6]
    if column[7] >= 1 and column[6] == 0:
        isolated_pawn_count += column[7]

    return -(isolated_pawn_count * 10)


def passed_pawns(pawn_locations_white, pawn_locations_black):
    # calculate all the passed pawns for white
    white_pawns_column = [[] for i in range(8)]
    black_pawns_column = [[] for i in range(8)]

    passed_pawn_white_points = 0
    passed_pawn_black_points = 0

    # points of passed_pawns depending on what row it is on
    location_points = [None, 5, 10, 20, 35, 60, 100, None]

    # find out the rows and columns for each pawn
    for pawn in pawn_locations_white:
        white_pawns_column[pawn % 8].append(pawn // 8)
    for pawn in pawn_locations_black:
        black_pawns_column[pawn % 8].append(pawn // 8)
    # make sure there are no black pawns infront, to the left of to the right of the pawn
    for white_pawn in white_pawns_column[0]:
        # we are given the row of the pawn
        # if all the pawns of black is in a row lower than white's pawn we are good
        if all(black_pawn <= white_pawn for black_pawn in black_pawns_column[0]) and \
                all(black_pawn <= white_pawn for black_pawn in black_pawns_column[1]):
            passed_pawn_white_points += location_points[white_pawn]

    for white_pawn in white_pawns_column[1]:
        if all(black_pawn <= white_pawn for black_pawn in black_pawns_column[0]) and \
                all(black_pawn <= white_pawn for black_pawn in black_pawns_column[1]) and \
                all(black_pawn <= white_pawn for black_pawn in black_pawns_column[2]):
            passed_pawn_white_points += location_points[white_pawn]

    for white_pawn in white_pawns_column[2]:
        if all(black_pawn <= white_pawn for black_pawn in black_pawns_column[1]) and \
                all(black_pawn <= white_pawn for black_pawn in black_pawns_column[2]) and \
                all(black_pawn <= white_pawn for black_pawn in black_pawns_column[3]):
            passed_pawn_white_points += location_points[white_pawn]

    for white_pawn in white_pawns_column[3]:
        if all(black_pawn <= white_pawn for black_pawn in black_pawns_column[2]) and \
                all(black_pawn <= white_pawn for black_pawn in black_pawns_column[3]) and \
                all(black_pawn <= white_pawn for black_pawn in black_pawns_column[4]):
            passed_pawn_white_points += location_points[white_pawn]

    for white_pawn in white_pawns_column[4]:
        if all(black_pawn <= white_pawn for black_pawn in black_pawns_column[3]) and \
                all(black_pawn <= white_pawn for black_pawn in black_pawns_column[4]) and \
                all(black_pawn <= white_pawn for black_pawn in black_pawns_column[5]):
            passed_pawn_white_points += location_points[white_pawn]

    for white_pawn in white_pawns_column[5]:
        if all(black_pawn <= white_pawn for black_pawn in black_pawns_column[4]) and \
                all(black_pawn <= white_pawn for black_pawn in black_pawns_column[5]) and \
                all(black_pawn <= white_pawn for black_pawn in black_pawns_column[6]):
            passed_pawn_white_points += location_points[white_pawn]

    for white_pawn in white_pawns_column[6]:
        if all(black_pawn <= white_pawn for black_pawn in black_pawns_column[5]) and \
                all(black_pawn <= white_pawn for black_pawn in black_pawns_column[6]) and \
                all(black_pawn <= white_pawn for black_pawn in black_pawns_column[7]):
            passed_pawn_white_points += location_points[white_pawn]

    for white_pawn in white_pawns_column[7]:
        if all(black_pawn <= white_pawn for black_pawn in black_pawns_column[6]) and \
                all(black_pawn <= white_pawn for black_pawn in black_pawns_column[7]):
            passed_pawn_white_points += location_points[white_pawn]

    # do it for black now

    for black_pawn in black_pawns_column[0]:
        # we are given the row of the pawn
        # if all the pawns of black is in a row lower than white's pawn we are good
        if all(white_pawn >= black_pawn for white_pawn in white_pawns_column[0]) and \
                all(white_pawn >= black_pawn for white_pawn in white_pawns_column[1]):
            passed_pawn_black_points += location_points[7 - black_pawn]

    for black_pawn in black_pawns_column[1]:
        if all(white_pawn >= black_pawn for white_pawn in white_pawns_column[0]) and \
                all(white_pawn >= black_pawn for white_pawn in white_pawns_column[1]) and \
                all(white_pawn >= black_pawn for white_pawn in white_pawns_column[2]):
            passed_pawn_black_points += location_points[7 - black_pawn]

    for black_pawn in black_pawns_column[2]:
        if all(white_pawn >= black_pawn for white_pawn in white_pawns_column[1]) and \
                all(white_pawn >= black_pawn for white_pawn in white_pawns_column[2]) and \
                all(white_pawn >= black_pawn for white_pawn in white_pawns_column[3]):
            passed_pawn_black_points += location_points[7 - black_pawn]

    for black_pawn in black_pawns_column[3]:
        if all(white_pawn >= black_pawn for white_pawn in white_pawns_column[2]) and \
                all(white_pawn >= black_pawn for white_pawn in white_pawns_column[3]) and \
                all(white_pawn >= black_pawn for white_pawn in white_pawns_column[4]):
            passed_pawn_black_points += location_points[7 - black_pawn]

    for black_pawn in black_pawns_column[4]:
        if all(white_pawn >= black_pawn for white_pawn in white_pawns_column[3]) and \
                all(white_pawn >= black_pawn for white_pawn in white_pawns_column[4]) and \
                all(white_pawn >= black_pawn for white_pawn in white_pawns_column[5]):
            passed_pawn_black_points += location_points[7 - black_pawn]

    for black_pawn in black_pawns_column[5]:
        if all(white_pawn >= black_pawn for white_pawn in white_pawns_column[4]) and \
                all(white_pawn >= black_pawn for white_pawn in white_pawns_column[5]) and \
                all(white_pawn >= black_pawn for white_pawn in white_pawns_column[6]):
            passed_pawn_black_points += location_points[7 - black_pawn]

    for black_pawn in black_pawns_column[6]:
        if all(white_pawn >= black_pawn for white_pawn in white_pawns_column[5]) and \
                all(white_pawn >= black_pawn for white_pawn in white_pawns_column[6]) and \
                all(white_pawn >= black_pawn for white_pawn in white_pawns_column[7]):
            passed_pawn_black_points += location_points[7 - black_pawn]

    for black_pawn in black_pawns_column[7]:
        # we are given the row of the pawn
        # if all the pawns of black is in a row lower than white's pawn we are good
        if all(white_pawn >= black_pawn for white_pawn in white_pawns_column[6]) and \
                all(white_pawn >= black_pawn for white_pawn in white_pawns_column[7]):
            passed_pawn_black_points += location_points[7 - black_pawn]

    return passed_pawn_white_points, passed_pawn_black_points


def open_and_semiopen(wr, br, wp, bp, open, semi_open):
    """
    given the rooks, give points based on if the rook is on a semi-opened or opened file
    opened files are defined as having no pawns of either color on the same file
    while semiopened files are files where theres only opposing pawns on the same file
    """
    white_rook_points = 0
    black_rook_points = 0

    # check how many pawns on each file for black and white
    wp_column = [0 for _ in range(8)]
    for pawn in wp:
        wp_column[pawn % 8] += 1

    bp_column = [0 for _ in range(8)]
    for pawn in bp:
        bp_column[pawn % 8] += 1

    for rook in wr:
        # if theres a white pawn on the same column then its not an opened or semi opened file
        if wp_column[rook % 8] >= 1:
            continue

        # else if theres a black pawn on the same column, its a semi opened_file
        if bp_column[rook % 8] >= 1:
            white_rook_points += semi_open
            continue

        # else then its an opened file as there was no white or black pawns
        white_rook_points += open

    # do the same for black

    for rook in br:
        # if theres a black pawn on the same column then its not an opened or semi opened file
        if bp_column[rook % 8] >= 1:
            continue

        # else if theres a white pawn on the same column, its a semi opened_file
        if wp_column[rook % 8] >= 1:
            black_rook_points += semi_open
            continue

        # else then its an opened file as there was no white or black pawns
        black_rook_points += open

    return white_rook_points, black_rook_points
