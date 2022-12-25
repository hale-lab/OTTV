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
ghenv.Component.NickName = 'h a l e °'
ghenv.Component.Message = '0.0.1'

import rhinoscriptsyntax as rs

# create a function to extract faces normal.
def ExtractFace(face):

    faceCtr = rs.SurfaceAreaCentroid(face)
    faceUV = rs.SurfaceClosestPoint(face, faceCtr[0])
    faceNormal = rs.SurfaceNormal(face, [faceUV[0], faceUV[1]])
    
    return faceCtr[0], faceNormal

# create a function to check filtered faces for correct orientation vs north.
def CheckAngle(face, faceCtr, faceNormal):
    
    perpNormal = rs.VectorRotate(faceNormal, 90, [0,0,1])
    basePlane = rs.CreatePlane(faceCtr,perpNormal,faceNormal)
    offsetN = rs.CopyObject(faceCtr, rotatedN)
    offsetNormal = rs.CopyObject(faceCtr, faceNormal)
    
    checkAngle = rs.Angle(offsetN, offsetNormal, basePlane)
    resultAngle = checkAngle[0]*2
    
    return resultAngle

# list of variables
world = (0, 0, 0)
faceSel = []
N = []
NE = []
E = []
SE = []
S = []
SW = []
W = []
NW = []

    
# explodes volume to get a list of surfaces.
if rs.IsPolysurface(_walls):
    faces = rs.ExplodePolysurfaces(_walls)
else :
    faces = _walls

# define north direction.
try :
    trueN = rs.VectorCreate([0, 1, 0], world)
    rotation = 360 - abs(int(_north))
    rotatedN = rs.VectorRotate(trueN, rotation, [0,0,1])
except :
    print('Please provide only numerical values for _north.')

# get filtered faces.
try :
    
    for face in faces:
        faceCtr, faceNormal = ExtractFace(face)
    
        #remove all faces facing z+ and z-.
    
        if faceNormal[2] != 1 and faceNormal[2] != -1 :
            faceSel.append(face)
        
    for face in faceSel:
        faceCtr, faceNormal = ExtractFace(face)
        checkResult = CheckAngle(face, faceCtr, faceNormal)
    
        #group faces from similar orientation.
        if checkResult >= 0 and checkResult < 22.5 :
            N.append(face)
        elif checkResult >= 22.5 and checkResult < 45 :
            NW.append(face)
        elif checkResult >= 45 and checkResult < 67.5 :
            NW.append(face)
        elif checkResult >= 67.5 and checkResult < 90 :
            W.append(face)
        elif checkResult >= 90 and checkResult < 112.5 :
            W.append(face)
        elif checkResult >= 112.5 and checkResult < 135 :
            SW.append(face)
        elif checkResult >= 135 and checkResult < 157.5 :
            SW.append(face)
        elif checkResult >= 157.5 and checkResult < 180 :
            S.append(face)
        elif checkResult >= 180 and checkResult < 202.5 :
            S.append(face)
        elif checkResult >= 202.5 and checkResult < 225 :
            SE.append(face)
        elif checkResult >= 225 and checkResult < 247.5 :
            SE.append(face)
        elif checkResult >= 247.5 and checkResult < 270 :
            E.append(face)
        elif checkResult >= 270 and checkResult < 292.5 :
            E.append(face)
        elif checkResult >= 292.5 and checkResult < 315 :
            NE.append(face)
        elif checkResult >= 315 and checkResult < 337.5 :
            NE.append(face)
        else :
            N.append(face)

except :
    print("Error! Please input list of surfaces or one polysurface as the whole building envelope, not both types eg: list of surfaces and polysurfaces.")