"""Provides a scripting component.
    Inputs:
        x: The x script variable
        y: The y script variable
    Output:
        a: The a output variable"""

import rhinoscriptsyntax as rs
import ghpythonlib as gh

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

# create a function to rotate the shading.
def RotateShading(edge, shading, angle) :
    rotAxisStart = rs.CurveStartPoint(edge)
    rotAxisEnd = rs.CurveEndPoint(edge)
    rotAxis = rs.VectorCreate(rotAxisStart, rotAxisEnd)
    rotCtr = rs.CurveMidPoint(edge)
    rotMod = 90 - angle
    rotShd = rs.RotateObject(shading, rotCtr, rotMod, rotAxis)
    
    return rotShd

# create a function to sort each edges into V-H orientation.
def EdgeSort2VH(edges):
    edgeH = []
    edgeV_L = []
    edgeV_R = []

    for edge in edges:
        edgeMid = rs.CurveMidPoint(edge)
        edgeDir = rs.VectorCreate(edgeMid, faceCtr)
        if edgeDir[2] > 0 and rs.IsVectorParallelTo(edgeDir, [0 ,0 ,1]) :
            print("H")
            edgeH.append(edge)
        elif edgeDir[1] > 0 and rs.IsVectorPerpendicularTo(edgeDir, [0 ,0 ,1]) :
            print("V1_L")
            edgeV_L.append(edge)
        elif edgeDir[1] < 0 and rs.IsVectorPerpendicularTo(edgeDir, [0 ,0 ,1]) :
            print("V1_R")
            edgeV_R.append(edge)
        elif edgeDir[0] > 0 and rs.IsVectorPerpendicularTo(edgeDir, [0 ,0 ,1]) :
            print("V2_L")
            edgeV_L.append(edge)
        elif edgeDir[0] < 0 and rs.IsVectorPerpendicularTo(edgeDir, [0 ,0 ,1]) :
            print("V2_R")
            edgeV_R.append(edge)
    
    return edgeH, edgeV_L, edgeV_R

faceCtr, faceNormal = ExtractFace(_windows)

edges = rs.DuplicateEdgeCurves(_windows)
pathMod = rs.VectorScale(faceNormal, _depth)
moveCtr = rs.CopyObject(faceCtr, pathMod)
path = rs.AddLine(faceCtr, moveCtr)

H, V_L, V_R = EdgeSort2VH(edges)

shadingH = rs.ExtrudeCurve(H, path)
shadingV_L = rs.ExtrudeCurve(V_L, path)
a = RotateShading( V_L, shadingV_L, _rotation)