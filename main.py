import time
import json
import logging
from src.simulator import simulate_sensor_data
from src.anomaly_detector import detect_anomaly
from src.llm_agent import get_llm_action, execute_action
from src.mqtt_client import setup_mqtt, publish_data
from src.database import init_db, store_data
from src.digital_twin import simulate_scenario

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload)
        logger.info(f"Received data for Rack {data['rack_id']}: {data}")

        # Store data in SQLite
        store_data(data)

        # Detect anomalies
        anomaly_type = detect_anomaly(data)
        if anomaly_type:
            logger.info(f"Anomaly detected in Rack {data['rack_id']}: {anomaly_type}")

            # Get LLM action
            action = get_llm_action(data, anomaly_type)
            command = execute_action(action)
            logger.info(f"Rack {data['rack_id']}: Action: {action}, Command: {command}")

            # Publish action
            publish_data("data_center/actions", {"rack_id": data["rack_id"], "command": command})

        # Run digital twin
        scenario = simulate_scenario(data)
        logger.info(f"Digital Twin for Rack {data['rack_id']}: {scenario}")

    except Exception as e:
        logger.error(f"Error processing message: {e}")


if __name__ == "__main__":
    # Initialize database
    init_db()
    logger.info("Initialized SQLite database")

    # Setup MQTT client
    mqtt_client = setup_mqtt(on_message)
    logger.info("MQTT client started")

    # Simulate multiple racks (2 racks for testing)
    try:
        while True:
            for rack_id in range(1, 3):
                data = simulate_sensor_data(rack_id)
                publish_data("data_center/racks", data)
                logger.info(f"Simulated data for Rack {rack_id}: {data}")
                time.sleep(2)  # Simulate data every 2 seconds
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        mqtt_client.loop_stop()
        mqtt_client.disconnect()