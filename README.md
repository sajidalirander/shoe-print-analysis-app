# Installation steps

## Clone the repository
```TypeScript
git clone https://github.com/sajidalirander/shoe-print-analysis-app.git
cd shoe-print-analysis-app
```

## Create environment
Creating a virtual environment named `.venv_shoeprint`
```TypeScript
python3 -m venv .venv_shoeprint
```

Activate the environement
```TypeScript
source .venv_shoeprint/bin/activate
```

Install other dependencies in the virtual environment using the [requirement.txt](./requirements.txt):
```TypeScript
python3 -m pip install -r requirements.txt 
```

# Directory Structure

* `./assets/`: include the repo assets as results.
* `./backend/`: contains the FastAPI application code.
* `./database/`: stores the dataset used in the project.
* `./docs/`: report related to the project.
* `./experiments/`: contains experimental scripts and tests, with mongoDB.
* `./src/`: the PyQt5 frontend application source code.

# Running the application
A shell script is written to run the backend and frontend simultaneously. \
Make it executable:
```TypeScript
chmod +x run.sh
```

Then run with:
```TypeScript
./run.sh
```