# **GCS Document Retrieval Agent Setup Guide**

This guide provides step-by-step instructions to set up, configure, and run the Document Retrieval Agent in a new ADK (Agent Development Kit) environment.

## **Prerequisites**

* Python 3.11 or higher installed  
* Google Cloud SDK (gcloud CLI) installed and authenticated  
* ADK CLI installed on your system

## **Step 1: Create and Activate a Virtual Environment**

It is highly recommended to run this agent inside an isolated virtual environment to prevent dependency conflicts. First, we will create the root project folder and set up the environment.

1. Open your terminal, create a root directory for your ADK project, and navigate into it:  
   mkdir my-adk-project  
   cd my-adk-project

2. Create the virtual environment:  
   python3 \-m venv .venv

3. Activate the virtual environment:  
   * **On macOS/Linux:**  
     source .venv/bin/activate

   * **On Windows:**  
     .venv\\Scripts\\activate

## **Step 2: Install Required Dependencies**

With your virtual environment activated, install the necessary Python packages. Based on the imports in agent.py, run the following command:

pip install python-dotenv google-cloud-discoveryengine google-adk

*(Note: If you have a requirements.txt file, you can alternatively run pip install \-r requirements.txt)*

## **Step 3: Create ADK Agent and Project Structure**

Now that the environment is ready, set up your ADK agent.

1. Create the ADK agent:  
   adk create agent\_gcs\_datastore

2. Place your agent.py code inside the newly created agent\_gcs\_datastore directory, replacing the default file.

### **Move .env one level up**

It is crucial that your .env file is located at the root of your project, *outside* of the specific agent directory, so that the ADK environment can load it properly. Move the file by running:

mv agent\_gcs\_datastore/.env .


Open the .env file and ensure it contains the following required variables:

GOOGLE\_GENAI\_USE\_VERTEXAI=1  
GOOGLE\_CLOUD\_PROJECT=\<CHANGE-ME\>  
GOOGLE\_CLOUD\_LOCATION=global

Your folder structure should look like this:

my-adk-project/  
├── .env                        \<-- MUST be here (one level above the agent directory)  
├── .venv/                       \<-- Your virtual environment folder

├── README.md                       \<-- Your virtual environment folder  
└── agent\_gcs\_datastore/  
    └────		 agent.py  
    └────		 \_\_init\_\_.py

## **Step 4: Update Configuration Variables**

Before running the agent, open agent\_gcs\_datastore/agent.py and ensure the variables in the \# \--- CONFIGURATION \--- section match your target Google Cloud environment:

\# \--- CONFIGURATION \---  
PROJECT\_ID \= "gcp-project-id" \#\#\# \<CHANGE-ME\>

\# Datastore / Discovery Engine Configuration  
ENGINE\_ID \= "gemini\_app\_id" \#\#\# \<CHANGE-ME\>  
DATA\_STORE\_ID \= "example-gcs\_1769807395048\_gcs\_store" \#\#\# \<CHANGE-ME\>  
DATASTORE\_LOCATION \= "us" \#\#\# \<CHANGE-ME\>. can be global, etc ...

\# Model Configuration  
MODEL\_NAME \= "gemini-3.1-pro-preview" \#\#\# \<CHANGE-ME\>

*Make sure PROJECT\_ID, ENGINE\_ID, and DATA\_STORE\_ID point to the correct Vertex AI Search datastore you intend to query.*

## **Step 5: Run the Agent**

Ensure you are in the root directory (where your .env file is located) and your virtual environment is activated.

Start the agent using the ADK CLI by running:

adk run agent\_gcs\_datastore

If everything is configured correctly, the ADK orchestrator will initialize the agent and it will be ready to accept document retrieval queries\!
