# ChatGPT generated Summary of Our Discussion on this Deploy module

## Architecture & CI/CD Planning

### Design Principles

- **Deploy Module Purpose**: Provides a unified, Pythonic interface to deploy containers either locally or to cloud providers, abstracting away provider-specific details.  
- **Layered Structure**:  
  - `BaseDeployer` handles deployment workflow (bundle, build, launch).  
  - **Mixins** provide modular “capabilities” (Cloud, Docker, Bash, Versioning, Packaging) that can be composed as needed.  
  - `CloudMixin` acts as a bridge between `BaseDeployer` and cloud providers, delegating provider-specific logic to `BaseCloudProvider` subclasses (e.g., `AzureProvider`, `GCPProvider`).  
- **Inheritance + Mixins**: Combines classical inheritance for cloud provider specialization and mixins for reusable capabilities, minimizing tangled code while maximizing modularity.  

### Deployment Flow

- Local vs Cloud: `BaseDeployer` can operate either locally or in the cloud by using `CloudMixin`.  
- Cloud provider classes handle the internal details of interacting with specific cloud APIs or CLIs.  
- Docker integration is abstracted via `DockerMixin`, supporting both local builds and cloud registry pushes.  
- Versioning is automated via `VersionMixin`, generating semantic + timestamped tags.  

### CLI vs SDK Considerations

- **Current Approach**: Uses CLI commands for cloud interactions, which allows quick iterative testing in a terminal.  
- **Future SDK Integration**:  
  - SDKs offer structured objects, programmatic error handling, and tighter CI/CD integration.  
  - Plan: prototype with CLI, then gradually migrate core operations to SDK calls for reliability and maintainability.  

### CI/CD Planning

- Deploy module is **CI/CD agnostic**: designed to run as a one-line Python script in any environment.  
- CI/CD workflows (e.g., GitHub Actions) can invoke the deploy module directly without needing deep integration.  
- Local testing remains easy: module can be run interactively before integrating into automated pipelines.  

### Key Benefits

- Modular and reusable architecture reduces duplication and complexity.  
- Clear separation of concerns: deployment logic, cloud specifics, Docker management, and versioning are all encapsulated.  
- Flexible to adopt new cloud providers or deployment strategies without rewriting core workflows.

---

Collection of Bash scripts for Cloud Deployment

Due to unplanned-go-as-you-code building, and own
conceptual knowledge/programming preferences,
do not have DockerFiles directly in server/ and client/
subdirs. Instead want to "modularize" the different
tools into their own encapsulated folders.

# Just thought of Future Feature (Dev Ops)

Curate (hopefully useful) scripts for quick local developing/debugging


# Enforcing a suitable directory to run the scripts
Hoping to have just one script I can run to setup everything 
for production.

Simplest to me as of now is:
video-stream/cloud/deploy

However, I am building solely the server/setup.sh and 
testing it in isolation to avoid the client-side npm build everytime.
Q: How can I write these scripts to facilitate this?
A?: for development of the server/setup.sh, just run from same subdir

# New sub-branch: project/integrate-cloud-runs--deploy-isolated
Want to be able to deploy client on it's own so as to not mess up the cloud-server-instance

# New sub-branch: project/integrate-cloud-runs--deploy-cloud
FINALLY gonna work on integrating the Client instance to fetch from the server instance
OR
just see if the deploy module works in the cloud shell

# New sub-branch: project/refactor-deploy
Want to be able to deploy client on it's own so as to not mess up the cloud-server-instance

# New sub-sub-branch: centralize-cloud-providers--deploy-azure--versioning
Deploying to azure has issue where pushing same-named tags to ACR seems to cause
cached older versions to be used
Attempt to build into current deploy module an automatic versioning incrementing 
func or hook thing