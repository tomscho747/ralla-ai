
# Face Verification & Analysis API Documentation

## 📍 Endpoint 1: POST `${BASE_URL}/verify`

This endpoint verifies whether two face images belong to the same person.

---

### 🔐 Headers

```
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY
```

---

### 📥 Request Body

```json
{
  "img1_path": "https://raw.githubusercontent.com/serengil/deepface/master/tests/dataset/img1.jpg",
  "img2_path": "https://raw.githubusercontent.com/serengil/deepface/master/tests/dataset/img2.jpg"
}
```

#### 🧾 Field Definitions

| Field        | Type   | Required | Description                                              |
|--------------|--------|----------|----------------------------------------------------------|
| `img1_path`  | string | ✅       | Public URL of the first image.                          |
| `img2_path`  | string | ✅       | Public URL of the second image.                         |

---

### 📤 Example Response

```json
{
  "detector_backend": "opencv",
  "distance": 0.42272907319751785,
  "facial_areas": {
    "img1": {
      "h": 768,
      "left_eye": [850, 524],
      "right_eye": [571, 517],
      "w": 768,
      "x": 339,
      "y": 218
    },
    "img2": {
      "h": 491,
      "left_eye": [858, 388],
      "right_eye": [663, 390],
      "w": 491,
      "x": 524,
      "y": 201
    }
  },
  "model": "VGG-Face",
  "similarity_metric": "cosine",
  "threshold": 0.68,
  "time": 3.39,
  "verified": true
}
```

#### 🧾 Response Fields

| Field               | Type     | Description                                                       |
|--------------------|----------|-------------------------------------------------------------------|
| `detector_backend` | string   | Face detection backend used.                                     |
| `distance`         | float    | Distance metric value between faces.                             |
| `facial_areas`     | object   | Bounding box and eye locations per image.                        |
| `model`            | string   | Face recognition model used (e.g., VGG-Face).                    |
| `similarity_metric`| string   | Similarity function used (e.g., cosine, euclidean).              |
| `threshold`        | float    | Decision threshold for face matching.                           |
| `time`             | float    | Time taken to process (in seconds).                             |
| `verified`         | boolean  | Whether the two faces are considered the same person.           |

---

## 📍 Endpoint 2: POST `${BASE_URL}/analyze`

This endpoint performs face analysis to predict age, gender, emotion, and race.

---

### 🔐 Headers

```
Content-Type: application/json
Authorization: Bearer YOUR_API_KEY
```

---

### 📥 Request Body

```json
{
  "img_path": "https://raw.githubusercontent.com/serengil/deepface/master/tests/dataset/img1.jpg",
  "actions": ["age", "gender", "emotion", "race"]
}
```

#### 🧾 Field Definitions

| Field       | Type     | Required | Description                                              |
|-------------|----------|----------|----------------------------------------------------------|
| `img_path`  | string   | ✅       | Public URL of the image to analyze.                      |
| `actions`   | string[] | ✅       | List of analyses to perform (`"age"`, `"gender"`, etc). |

---

### 📤 Example Response

```json
{
  "results": [
    {
      "age": 31,
      "dominant_emotion": "sad",
      "dominant_gender": "Man",
      "dominant_race": "white",
      "emotion": { "angry": 10.38, "disgust": 0.34, "fear": 41.99, "happy": 0.03, "neutral": 2.44, "sad": 44.47, "surprise": 0.34 },
      "face_confidence": 0.89,
      "gender": { "Man": 99.99, "Woman": 0.01 },
      "race": { "asian": 1.66, "black": 0.26, "indian": 1.17, "latino hispanic": 41.77, "middle eastern": 10.03, "white": 45.10 },
      "region": { "h": 681, "w": 681, "x": 1436, "y": 336 }
    },
    {
      "age": 31,
      "dominant_emotion": "neutral",
      "dominant_gender": "Woman",
      "dominant_race": "white",
      "emotion": { "angry": 0.05, "disgust": 0.00, "fear": 0.36, "happy": 43.93, "neutral": 54.20, "sad": 1.25, "surprise": 0.20 },
      "face_confidence": 0.92,
      "gender": { "Man": 0.02, "Woman": 99.98 },
      "race": { "asian": 0.26, "black": 0.02, "indian": 0.23, "latino hispanic": 5.22, "middle eastern": 8.17, "white": 86.11 },
      "region": { "h": 758, "w": 758, "x": 326, "y": 542, "left_eye": [833, 819], "right_eye": [553, 860] }
    }
  ]
}
```

#### 🧾 Response Fields

| Field                | Type    | Description                                                             |
|---------------------|---------|-------------------------------------------------------------------------|
| `results`           | array   | Array of analysis results (one per detected face).                      |
| `age`               | integer | Estimated age.                                                          |
| `dominant_emotion`  | string  | Most likely emotion.                                                    |
| `dominant_gender`   | string  | Most likely gender.                                                     |
| `dominant_race`     | string  | Most likely race.                                                       |
| `emotion`           | object  | Confidence scores for each emotion.                                     |
| `gender`            | object  | Confidence scores for each gender.                                      |
| `race`              | object  | Confidence scores for each race.                                        |
| `face_confidence`   | float   | Confidence in face detection.                                           |
| `region`            | object  | Bounding box of the face (and eyes if available).                       |
