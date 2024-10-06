import numpy as np
import cv2
import math
import logging
from ultralytics import YOLO
from sort import Sort

# Constants
video_file = "car_video.mp4"
mask_file = "mask.png"
model_file = "yolov8n.pt"
class_names = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck"]
limits = [450, 600, 1450, 600]  # Coordinates for the detection line

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


# Initialize the video capture, YOLO model, mask, and tracker
def initialize_components() -> tuple:
    # Initialize video capture
    cap = cv2.VideoCapture(video_file)
    # Load the YOLO model for object detection
    model = YOLO(model_file)
    # Read the mask image for masking specific regions in the frame
    mask = cv2.imread(mask_file)
    # Initialize the SORT tracker for object tracking
    tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)
    return cap, model, mask, tracker


# Perform object detection on the specified image region using the YOLO model
def detect_objects(model: YOLO, img_region: np.ndarray) -> np.ndarray:
    # Perform object detection using the YOLO model
    results = model(img_region, stream=True)
    detections = np.empty((0, 5))

    # Iterate through each detection result
    for r in results:
        for box in r.boxes:
            # Extract bounding box coordinates and convert them to integers
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            # Calculate confidence score and round it to two decimal places
            conf = math.ceil((box.conf[0] * 100)) / 100
            cls = int(box.cls[0])
            current_class = class_names[cls]

            # Filter for specific vehicle types with confidence above the threshold
            if current_class in ["car", "truck", "bus"] and conf > 0.3:
                current_array = np.array([x1, y1, x2, y2, conf])
                detections = np.vstack((detections, current_array))  # Stack the detected objects
    return detections


# Draw bounding boxes for tracked objects on the image
def draw_bounding_boxes(img: np.ndarray, results_tracker: list) -> None:
    # Loop through each tracked object and draw its bounding box and ID
    for result in results_tracker:
        x1, y1, x2, y2, obj_id = map(int, result)
        # Draw a green rectangle for the bounding box
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)  # Green box with thickness of 2
        # Display the object ID near the top-left corner of the bounding box
        cv2.putText(img, f'ID: {int(obj_id)}', (x1, y1 - 10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)


# Update the vehicle count if a tracked object crosses the detection line
def update_vehicle_count(results_tracker: list, total_count: list, img: np.ndarray) -> None:
    # Loop through each tracked object to check if it crosses the detection line
    for result in results_tracker:
        x1, y1, x2, y2, obj_id = map(int, result)
        w, h = x2 - x1, y2 - y1
        cx, cy = x1 + w // 2, y1 + h // 2  # Calculate the center point of the bounding box

        # Check if the object's center point crosses the predefined detection line
        if limits[0] < cx < limits[2] and limits[1] - 15 < cy < limits[1] + 15:
            if obj_id not in total_count:  # Ensure that each object is only counted once
                total_count.append(obj_id)
                cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)  # Draw a green line
                logging.info(f"Veiculo com id {obj_id} contado. Contagem total:: {len(total_count)}")


# Main function to initialize components and process video frames for vehicle detection and tracking
def main() -> None:
    cap, model, mask, tracker = initialize_components()
    total_count = []

    # Check if video capture is successfully opened
    if not cap.isOpened():
        logging.error("Erro: Falha ao abrir o video.")
        return

    while cap.isOpened():
        success, img = cap.read()
        if not success:
            logging.warning("Alerta: Falha ao processar frame do video.")
            break

        # Apply mask to the image region for processing
        img_region = cv2.bitwise_and(img, mask)
        detections = detect_objects(model, img_region)  # Detect objects in the masked region
        results_tracker = tracker.update(detections)  # Update tracker with new detections

        # Draw detection line on the image
        cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 0, 255), 5)  # Red detection line

        # Draw bounding boxes and update the vehicle count
        draw_bounding_boxes(img, results_tracker)
        update_vehicle_count(results_tracker, total_count, img)

        # Display the total vehicle count on the image
        cv2.putText(img, f'Carros: {len(total_count)}', (10, 100), cv2.FONT_HERSHEY_PLAIN, 4, (90, 90, 90), 5)
        cv2.imshow("Contagem de Carros", img)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit the loop
            logging.info("Encerrando programa.")
            break

    cap.release()  # Release the video capture object
    cv2.destroyAllWindows()  # Close all OpenCV windows
    logging.info("Programa encerrado com sucesso.")


if __name__ == "__main__":
    main()
