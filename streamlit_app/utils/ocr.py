import easyocr
import numpy as np

reader = easyocr.Reader(['en'], gpu=False)

def perform_ocr(image):
    image_np = np.array(image)
    results = reader.readtext(image_np, detail=1)

    text_with_conf = []
    text_without_conf = []
    confidences = []

    for res in results:
        word, conf = res[1], res[2]
        if conf < 0.5:
            word = f"{word} 🚨"
        text_with_conf.append(f"{word} [Conf: {conf:.2f}]")
        text_without_conf.append(word)
        confidences.append(conf)

    avg_conf = sum(confidences) / len(confidences) if confidences else 0.0
    return "\n".join(text_with_conf), " ".join(text_without_conf), avg_conf
