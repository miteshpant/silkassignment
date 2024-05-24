# Silk Data Pipeline

## Overview
This project is designed to build a scalable data pipeline using Flask and MongoDB to handle, deduplicate, and analyze data from multiple sources. It fetches data from APIs, translates it into a common model, deduplicates hosts, and stores the data in MongoDB. The project also includes visualization capabilities to generate insights from the data.

## Features
- Data Fetching: Retrieve data from multiple APIs.
- Data Transformation: Translate data from different models to a common model.
- Deduplication: Ensure no duplicate hosts exist within each source and across sources.
- Data Storage: Store the processed data in MongoDB.
- Visualization: Generate visual insights from the stored data.
- Scalability: Handle large datasets efficiently.
- Logging: Track the pipeline's operations and errors.

## Prerequisites
- Python 3.10+
- MongoDB
- Node.js (for running the MongoDB setup script)

## Installation
- Clone the Repository:
  -- git clone https://github.com/miteshpant/silkassignment.git
  -- cd silkassignment
  -- pip install -r requirements.txt
- Set up MongoDB
  -- node setup_mongo.js

## Running the Application
- Update your authentication token in app/config.py TOKEN
- python run.py
- curl  http://127.0.0.1:5000/data
- login to mongodb on shell
- use silk 
-  db.common_model.find();

## Visualization
- python visualize_hosts.py

![dom](https://github.com/miteshpant/silkassignment/assets/290845/68885a56-3cbf-41fe-b6c5-10569dd8ef39)
![DOOS](https://github.com/miteshpant/silkassignment/assets/290845/fa844e0a-fccb-4611-b72a-0de04532d56d)

  
  
