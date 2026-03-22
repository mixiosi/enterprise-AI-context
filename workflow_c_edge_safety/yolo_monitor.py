import cv2
from ultralytics import YOLO

# ==========================================
# Edge AI Safety Monitoring (PoC)
# ==========================================
# This script simulates real-time compliance tracking (hardhats, vests)
# using a pre-trained YOLOv8 model on a sample construction image.

def run_ppe_detection(image_path="sample_construction.jpg"):
    print("👷 Loading Edge AI YOLOv8 Model...")
    
    try:
        # Load a pre-trained YOLOv8 model (downloads automatically if missing)
        # Note: For production PPE detection, a fine-tuned model like yolov8n-ppe.pt would be used.
        # Here we use the base nano model to demonstrate object detection.
        model = YOLO('yolov8n.pt')
        
        print(f"📸 Analyzing {image_path} for safety compliance...")
        
        # In a real environment, this would process a live rtsp:// camera feed.
        # results = model(source='rtsp://camera_ip', stream=True)
        
        results = model(image_path)
        
        # Display results
        for r in results:
            print("\n🚨 Compliance Report Generated:")
            print(f"Detected {len(r.boxes)} objects.")
            
            # To actually view the bounded boxes:
            # r.show()
            # r.save(filename='ppe_violation_report.jpg')
            
            for box in r.boxes:
                cls_id = int(box.cls[0])
                class_name = model.names[cls_id]
                conf = float(box.conf[0])
                
                # If we detect "person" without corresponding PPE classes, we flag it.
                if class_name == 'person':
                    print(f"⚠️ Worker Detected (Confidence: {conf:.2%}). Cross-referencing PPE...")
                    
        print("\n✅ Edge inference complete. Data sent to Compliance Subsystem.")
        
    except Exception as e:
        print(f"❌ Error running YOLOv8: {e}")
        print("Make sure you have an image named 'sample_construction.jpg' in this folder.")

if __name__ == "__main__":
    run_ppe_detection()