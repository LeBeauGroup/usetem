def vector(instr, vec=(0,0)):
    """
    For some reason, vectors cannot be created with instrument object
    Using a preallocated one instead and setting to zero
    """
    newVec = instr.projection.DiffractionShift
    newVec.X = vec[0]
    newVec.Y = vec[1]

    return newVec
