# ADK Agent: Reference-Based Image Generator

This agent is designed to generate or edit images using `gemini-3.1-flash-image-preview` based on user prompts and uploaded reference files (Text, CSV, Images) inside **Gemini Enterprise**.

---

## 📂 Code Structure
Everything is consolidated into a single file for deployment stability:
- **`agent.py`**: Contains the `Agent` definition, custom tools, and prompt orchestration instructions.
- **`deploy_global_env.py`**: Script to programmatically deploy the agent to Vertex AI Agent Engine with `GOOGLE_CLOUD_LOCATION="global"` fixed variables.

---

## 🚀 1. Deployment to Vertex AI Agent Engine

To deploy or update this agent, run the following command from your gcloud authenticated workspace:

```bash
python3 deploy_global_env.py
```

* **Important Environment Details**: 
  * Orchestration uses `gemini-3.1-flash-lite-preview` inside location `global`.
  * Image generation uses `gemini-3.1-flash-image-preview` inside location `global`.
  * The Agent Engine container deploys into `us-central1`.

---

## 🔗 2. Registration in Gemini Enterprise

Once deployed, you must link the agent to your Gemini Enterprise application using the **Google Cloud Console**:

1. Go to the [Gemini Enterprise](https://console.cloud.google.com/gemini-enterprise/) dashboard.
2. Click on the name of your specific **App Layer** workspace.
3. Select the **Agents** tab on the left.
4. Click **`[+] Add agent`** or **`Add custom agent via Agent Engine`**.
5. **Configure the Identity**:
   * **Agent Name**: `Image Generator Agent V1`
   * **Description**: Clarify that this agent reads attached datasets or images to generate images using multimodal support.
   * **Reasoning Engine Resource Path**:
     Use your deployed LRO Resource URI ending in your ID:
     `https://us-central1-aiplatform.googleapis.com/v1/projects/agentspace-452714/locations/us-central1/reasoningEngines/9116920619588386816`

6. Click **Create** to activate the stream.

---

## 💡 3. Critical Tooling Rules (Updating the Brain)

* **Strict Argument Naming**: Custom tools interacting with artifacts **MUST** name the context parameter **`tool_context`** exactly, enabling ADK `FunctionTool` method lookups.
* **Canvas Image-to-Image Multimodal Handling**: To modify images consistently without style drift, use `load_artifact` iterate list sets to load original layers and append them into the overall `generate_content()` stack *before* appending prompt text streams.
* **Inspect.isawaitable Safety**: Support buffered write flushes surrounding `tool_context.save_artifact()` with a buffer-wait loop to safely commit rendered PNG files back to GE view screens.

---

## ⚙️ 4. Project Configuration Variable Updates

When copying this agent to a **new Google Cloud Project**, you must update the following variables in **`deploy_global_env.py`** to avoid deployment errors:

*   **`project="YOUR_PROJECT_ID"`** (Line 30): Update to your target space.
*   **`GCS_BUCKET="gs://YOUR_BUCKET_NAME"`** (Line 14): Verify your location-bound bucket string has bucket write permissions.
*   **API Endpoint endpoints (Line 11)**: Ensure `VERTEX_AI_API_ENDPOINT` matches your regional router setup if default binds pick local targets instead of global loads.

---

## 💻 5. Local Evaluation & Testing with ADK CLI

You can evaluate the agent's logic and tools locally before deploying to Agent Engine.

1.  **Ensure Authentication**:
    Make sure your local bash shell is authenticated to the project:
    ```bash
    gcloud auth application-default login
    ```

2.  **Run with Web UI (Recommended)**:
    Execute the ADK web dashboard and chat client to visually test image results rendering using canvas widgets:
    ```bash
    adk web
    ```
    Ensure you run this command **inside** the `orbital_galileo` directory to avoid session app name mismatches. Access at `http://127.0.0.1:8000`.

3.  **Run with interactive CLI (Alternative)**:
    ```bash
    adk run .
    ```

---

## 🧪 6. Live Verification

After deployment, you can verify connection to the deployed agent using the helper script:

```bash
python3 test_live_agent.py
```
This script initializes Vertex AI to the target workspace project space and streams a prompt to verify execution.

