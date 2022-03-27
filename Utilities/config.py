SUMO = {
    
    "gui" : True,
    
    #Collisions
    "--collision.action" : "warn",
    "--collision.check-junctions": True, 
    "--collision.stoptime": 50,

    # Logging
    "--error-log" : "Utilities/error-log.txt",

    # Smooth lane changing
    "--lanechange.duration": 2,

    #Random trips
    #"-r":"Utilities/trips.trips.xml",
    "-r": "trips.trips.xml",
    # Split lanes
    #"--lateral-resolution" : "5.5",

    # Traci Connection
    #"--num-clients" : 1,
    ##"--remote-port" : 5522,

    # Parking Options
    #"--additional-files" : "Utilities/parkinglot.net.xml",
    #"--parking.maneuver" : True,

    # GUI Options
    "--delay" : 200,
    #"--start" : "--quit-on-end",

    # RNG
    #"--seed" : 333
}