"""
This component extracts and groups all faces from input
building envelope to each orientation.

    Args:
        _walls: Input building envelope geometry.
        _north: Input north direction.

    Returns:
        readme! : readme!
        N : Faces facing north direction.
        NE : Faces facing northeast direction.
        E : Faces facing east direction.
        SE : Faces facing southeast direction.
        S : Faces facing south direction.
        SW : Faces facing southwest direction.
        W : Faces facing west direction.
        NW : Faces facing northwest direction.

"""

ghenv.Component.Name = "groupFacesbyOrient"
ghenv.Component.NickName = 'OTTV'
ghenv.Component.Message = '0.0.1'

import rhinoscriptsyntax as rs
import ghpythonlib as gh

# create a function to define north(rotated) direction.
def defineNorth(north):
    world = (0, 0, 0)

    trueN = rs.VectorCreate([0, 1, 0], world)
    rotation = 360 - abs(int(north))
    rotatedN = rs.VectorRotate(trueN, rotation, [0,0,1])

    return rotatedN

# create a function to extract faces normal.
def extractFace(face):

    faceCtr = rs.SurfaceAreaCentroid(face)
    faceUV = rs.SurfaceClosestPoint(face, faceCtr[0])
    faceNormal = rs.SurfaceNormal(face, [faceUV[0], faceUV[1]])
    
    return faceCtr[0], faceNormal

# create a function to check filtered faces for correct orientation vs north.
def checkAngle(face, faceCtr, faceNormal):
    
    perpNormal = rs.VectorRotate(faceNormal, 90, [0,0,1])
    basePlane = rs.CreatePlane(faceCtr,perpNormal,faceNormal)
    offsetN = rs.CopyObject(faceCtr, rotatedN)
    offsetNormal = rs.CopyObject(faceCtr, faceNormal)
    
    checkAngle = rs.Angle(offsetN, offsetNormal, basePlane)
    resultAngle = checkAngle[0]*2
    
    return resultAngle

# create a function to check if face is facing z+ or z-. 
def eligibleFace(face, faceNormal):
    
    if faceNormal[2] != 1 and faceNormal[2] != -1 :
        return True
    else :
        return False

# create a function to check face orientation.
def checkOrient(result):
    
    if checkResult >= 0 and checkResult < 22.5 :
        return "N"
    elif checkResult >= 22.5 and checkResult < 45 :
        return "NW"
    elif checkResult >= 45 and checkResult < 67.5 :
        return "NW"
    elif checkResult >= 67.5 and checkResult < 90 :
        return "W"
    elif checkResult >= 90 and checkResult < 112.5 :
        return "W"
    elif checkResult >= 112.5 and checkResult < 135 :
        return "SW"
    elif checkResult >= 135 and checkResult < 157.5 :
        return "SW"
    elif checkResult >= 157.5 and checkResult < 180 :
        return "S"
    elif checkResult >= 180 and checkResult < 202.5 :
        return "S"
    elif checkResult >= 202.5 and checkResult < 225 :
        return "SE"
    elif checkResult >= 225 and checkResult < 247.5 :
        return "SE"
    elif checkResult >= 247.5 and checkResult < 270 :
        return "E"
    elif checkResult >= 270 and checkResult < 292.5 :
        return "E"
    elif checkResult >= 292.5 and checkResult < 315 :
        return "NE"
    elif checkResult >= 315 and checkResult < 337.5 :
        return "NE"
    else :
        return "N"

# create a function to sort each edges into V-H orientation.
def edgeSort2VH(edges):
    edgeH = []
    edgeV_L = []
    edgeV_R = []

    for edge in edges:
        edgeMid = rs.CurveMidPoint(edge)
        edgeDir = rs.VectorCreate(edgeMid, faceCtr)
        if edgeDir[2] > 0 and rs.IsVectorParallelTo(edgeDir, [0 ,0 ,1]) :
            edgeH.append(edge)
        elif edgeDir[1] > 0 and rs.IsVectorPerpendicularTo(edgeDir, [0 ,0 ,1]) :
            edgeV_L.append(edge)
        elif edgeDir[1] < 0 and rs.IsVectorPerpendicularTo(edgeDir, [0 ,0 ,1]) :
            edgeV_R.append(edge)
        elif edgeDir[0] > 0 and rs.IsVectorPerpendicularTo(edgeDir, [0 ,0 ,1]) :
            edgeV_L.append(edge)
        elif edgeDir[0] < 0 and rs.IsVectorPerpendicularTo(edgeDir, [0 ,0 ,1]) :
            edgeV_R.append(edge)
    
    return edgeH, edgeV_L, edgeV_R

# create a function to rotate shading(for SC).
def rotateShading(edge, shading, angle) :
    axisPtStart = rs.CurveStartPoint(edge)
    axisPtEnd = rs.CurveEndPoint(edge)
    rotationAxis = rs.VectorCreate(axisPtStart, axisPtEnd)
    axisCtr = rs.CurveMidPoint(edge)
    rotation = 90 - angle
    rotatedShading = rs.RotateObject(shading, axisCtr, rotation, rotationAxis)
    
    return rotatedShading

# list of variables.
faces = []
facesSel = []

# 1. define north direction.
rotatedN = defineNorth(_north)
    
# 2. explodes volume to get a list of surfaces.
if rs.IsPolysurface(_walls):
    faces = rs.ExplodePolysurfaces(_walls)
else :
    faces = _walls

# 3. select eligible faces.
for face in faces:
    faceCtr, faceNormal = extractFace(face)
    if eligibleFace(face, faceNormal) is True:
        facesSel.append(face)

# 4. output eligible faces orientation.
for face in facesSel:
    faceCtr, faceNormal = extractFace(face)
    checkResult = checkAngle(face, faceCtr, faceNormal)
    print(checkOrient(checkResult))
