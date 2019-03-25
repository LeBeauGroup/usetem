def vector(instr, vec=(0,0)):
    """
    For some reason, vectors cannot be created with instrument object
    Using a preallocated one instead and setting to zero
    """
    newVec = instr.projection.DiffractionShift
    newVec.X = vec[0]
    newVec.Y = vec[1]

    return newVec

def temPositionFromDict(instr,posDict):

    pos = instr.Stage.Position

    pos.X = posDict['x']
    pos.Y = posDict['y']
    pos.Z = posDict['z']
    pos.A = posDict['A']
    pos.B = posDict['B']

    return pos

def positionDict(x,y,z,A,B):

    posDict = dict()
    posDict['x'] = x
    posDict['y'] = y
    posDict['z'] = z
    posDict['A'] = A
    posDict['B'] = B

    return posDict

def positionDictFromTem(position):

    posDict = dict()
    posDict['x'] = position.X
    posDict['y'] = position.y
    posDict['z'] = position.z
    posDict['A'] = position.A
    posDict['B'] = position.B

    return posDict
