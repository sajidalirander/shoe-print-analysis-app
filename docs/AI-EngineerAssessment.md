# Technical Assessment: Shoeprint Analysis Application

## Objective:
Build a simple shoeprint analysis application that allows users to:

 - Upload a shoeprint image.
 - Extract key features from the shoeprint.
 - Match the uploaded shoeprint against a small database of existing prints.
 - View a ranked list of the closest matches.



## Requirements:
### Backend:
Implement a REST API with the following operations:

 - POST /api/upload: Accept a shoeprint image, process it, and return extracted features.
 - GET /api/match/:id: Compare a given shoeprint to the stored database and return a ranked list of similar prints.
 - GET /api/shoeprints: Retrieve all stored shoeprint records.

### Data Processing:
Preprocess the uploaded shoeprint image (e.g., grayscale conversion, edge detection, feature extraction).
Extract unique features using SIFT, ORB, or deep learning-based embeddings (e.g., a pre-trained CNN or Vision Transformer).
Store extracted features in an in-memory structure (array), a JSON file, or a database (SQLite, MongoDB, etc.).

### Frontend:
Use any coding style (e.g. React, Vue, Angular, or plain JavaScript) to build a simple UI.

The frontend should:
 - Allow users to upload a shoeprint image.
 - Display the top 5 closest matching shoeprints from the database.
 - Show a visual comparison of the uploaded shoeprint with the closest match.



## Instructions:
### Backend:
 - Implement the REST API with the required routes.
 - For data storage, choose either an in-memory structure, a JSON file, or a database (SQLite, MongoDB, etc.).
 - Use OpenCV or TensorFlow/PyTorch for feature extraction.

### Frontend:
 - Create a simple UI with:
 - An upload button for shoeprint images.
 - A results section displaying matching shoeprints with similarity scores.
 - Ensure the UI makes requests to the backend API for processing and matching.

### README:
Provide a README file with setup instructions for both backend and frontend:

 - How to install dependencies.
  -How to run the backend and frontend.
 - How to test the application.
 - Any environment variables or configurations required (if applicable).



## Evaluation Criteria:
### Code Quality
 - Is the code clean, structured, and easy to understand?
### Functionality
 - Does the application correctly process and match shoeprint images?
### Machine Learning Implementation
 - Are relevant AI techniques applied effectively?
### Frontend Interaction
 - Does the UI allow users to upload images and view results properly?
### Performance & Optimization
 - Does the system efficiently process and retrieve shoeprint data?



## Submission Instructions:
### Submission Format:
1. Zip File Submission:
 - Compress the project into a .zip file.
 - Send the .zip file to the following email address: sascha.seibel@luxolis.ai.
OR
2. GitHub Submission:
 - Create a new public repository on GitHub.
 - Upload the project files to the repository.
 - Share the repository access with sascha.seibel@luxolis.ai.



## Submission Content:
 - README: Simple setup instructions for both backend and frontend.
 - Code: All files necessary to run the application.
