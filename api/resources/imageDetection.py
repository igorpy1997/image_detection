import base64
import logging
from io import BytesIO
from typing import TYPE_CHECKING
from flask import request, jsonify
from flask_restful import Resource
import numpy as np
import cv2
from ultralytics import YOLO
from PIL import Image

model = YOLO("models/yolov9t.pt")

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from ultralytics.engine.results import Results


class ImageDetection(Resource):
    def post(self):
        logger.info("Received a POST request for image detection.")
        data = request.get_json()
        if "InputBase64" not in data:
            logger.error("No 'InputBase64' key found in the request JSON.")
            return jsonify({"error": "No image data provided"}), 400
        try:
            logger.info("Decoding the base64 image data.")
            image_data = base64.b64decode(data["InputBase64"])
            image_np = np.frombuffer(image_data, np.uint8)
            image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

            logger.info("Running the model on the decoded image.")
            results = model(image)

            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    label = model.names[int(box.cls.item())]
                    confidence = float(box.conf.item())
                    cv2.rectangle(image, (x1, y1), (x2, y2), (173, 216, 230), 2)
                    cv2.putText(image, f"{label} {confidence:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 153), 3)
                    cv2.putText(image, f"{label} {confidence:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1)
            buffer = BytesIO()
            pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            pil_image.save(buffer, format="JPEG")

            output_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

            return {"OutputBase64": output_base64}

        except Exception as e:
            logger.error(f"Error during detection: {e}")
            return jsonify({"error": "Detection processing error"}), 500
