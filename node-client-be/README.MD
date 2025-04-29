# 📸 Image Processing API

**Version**: 1.0.0  
**Base URL**: `http://localhost:3000`

An API for processing images, generating QR codes, comparing image differences, and evaluating happiness levels in photos.

---

## 🔍 Endpoints

### 1. `POST /v1/best-shots`

**Description**: Finds the best matching image based on a textual query.

**Request**:
- **Content-Type**: `multipart/form-data`
- **Body Parameters**:
  - `image`: Array of images (`binary`)
  - `query`: Textual query (`string`)

**Responses**:
- `200 OK`:  
  ```json
  {
    "success": true,
    "filename": "best-match.jpg"
  }
  ```
- `400 Bad Request`:  
  ```json
  {
    "success": false,
    "message": "No picture matches the query."
  }
  ```

---

### 2. `POST /v1/generate-qr`

**Description**: Generates a QR code from the provided data.

**Request**:
- **Content-Type**: `application/json`
- **Body Parameters**:
  - `data`: Arbitrary key-value JSON object

**Response**:
- `200 OK`:  
  Returns a QR code image as `image/png`.

---

### 3. `POST /v1/before-after`

**Description**: Compares two images and identifies visual differences.

**Request**:
- **Content-Type**: `multipart/form-data`
- **Body Parameters**:
  - `image`: Array of 2 images (`binary`)

**Response**:
- `200 OK`:  
  ```json
  {
    "success": true,
    "message": "Differences found."
  }
  ```

---

### 4. `POST /v1/happiness`

**Description**: Evaluates happiness levels from one or more images.

**Request**:
- **Content-Type**: `multipart/form-data`
- **Body Parameters**:
  - `image`: Array of images (`binary`)
  - `query`: Textual query (`string`)

**Responses**:
- `200 OK`:  
  ```json
  {
    "success": true,
    "filename": "happiest.jpg",
    "score": 87
  }
  ```
- `400 Bad Request`:  
  ```json
  {
    "success": false,
    "message": "No picture matches the query."
  }
  ```
