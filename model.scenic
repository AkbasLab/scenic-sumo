"""Scenic model for Sumo scenarios."""

#Set up workspace
width = 10
length = 10
workspace = Workspace(RectangularRegion(0 @ 0, 0, width, length))

#Types of Objects

class Car:
    """Car"""
    name: ""
    route: ""
    distance: 0
    lane: 0
    xPos: 0
    yPos: 0
    angle: -1073741824.0
    vehPlacement: 1
    speed: -1
    speedMode: ""
    track: 0
    color: ""
    size: 5
    changeSpeed: ""
    tau: 0
    carParam: 0
    laneMode: 0
    laneChanges: ""
    parkPos: ""

class TrafficLight:
    """TrafficLight"""
    name: ""
    state: ""
    duration: ""


class Pedestrian:
    """Pedestrian"""
    name: ""
    route: ""
    departTime: 0
    distance: 0
    arrivalPos: 10

class ParkingLot:
    """Parking Lot"""
    name: ""
    lane: ""
    startPos: 0
    endPos: 0
    capacity: 0 
    angle: 90