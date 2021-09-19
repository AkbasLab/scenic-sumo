SUMO = {
    
    "gui" : True,
    # Street network
    #"--net-file" : "Map/FourWayIntersection/FourWayIntersection.net.xml",
    
    #Collisions
    "--collision.action" : "warn",
    "--collision.check-junctions": True, 
    "--collision.stoptime": 50,

    # Logging
    ##"--error-log" : "log/error-log.txt",

    # Smooth lane changing
    "--lanechange.duration": 2,

    # Split lanes
    #"--lateral-resolution" : "5.5",

    # Traci Connection
    #"--num-clients" : 1,
    ##"--remote-port" : 5522,

    # Parking Options
    #"--additional-files" : "parkinglot.net.xml",
    #"--parking.maneuver" : True,

    # GUI Options
    "--delay" : 200,
    #"--start" : "--quit-on-end",

    # RNG
    #"--seed" : 333
}