import os, sys, time, json
from kafka import KafkaProducer

# SUMO tools
SUMO_TOOLS = "C:/Program Files (x86)/Eclipse/Sumo/tools"
if SUMO_TOOLS not in sys.path:
    sys.path.append(SUMO_TOOLS)

import traci

SUMO_BINARY = "C:/Program Files (x86)/Eclipse/Sumo/bin/sumo-gui"
SUMO_CONFIG = "network.sumocfg"

producer = KafkaProducer(
    bootstrap_servers=['localhost:29092'],  # 29092 *** 9092
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def run():
    traci.start([SUMO_BINARY, "-c", SUMO_CONFIG])
    print("SUMO started")

    step = 0
    MAX_STEPS = 1000

    while step < MAX_STEPS:
        traci.simulationStep()
        t = traci.simulation.getTime()

        veh_ids = traci.vehicle.getIDList()
        print(f"step={step}, time={t}, vehicles={len(veh_ids)}")

        for vid in veh_ids:
            x, y = traci.vehicle.getPosition(vid)
            speed = traci.vehicle.getSpeed(vid)
            lane = traci.vehicle.getLaneID(vid)
            edge = traci.vehicle.getRoadID(vid)

            msg = {
                "time": t,
                "veh_id": vid,
                "x": x,
                "y": y,
                "speed": speed,
                "lane": lane,
                "edge": edge
            }

            producer.send("vehTelemetry", msg)
            print("Sent:", msg)

        step += 1
        time.sleep(0.05)  # slow down for GUI visibility

    producer.flush()
    producer.close()
    traci.close()
    print("Simulation finished")

if __name__ == "__main__":
    run()
