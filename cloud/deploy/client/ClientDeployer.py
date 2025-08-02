from common.base import BaseDeployer

class ClientDeployer(BaseDeployer):
    def setup_os_env(self):
        # Setup bashrc and install Node modules
        bashrc_file = self.project_root / "deploy" / "os" / "linux" / (
            ".bashrc.cloud.example" if self.deploy_env == "cloud" else ".bashrc.local.example"
        )
        print(f"Appending {bashrc_file} to ~/.bashrc")
        with open(bashrc_file) as src, open(Path.home() / ".bashrc", "a") as dest:
            dest.write("\n# ClientDeployer setup\n")
            dest.write(src.read())

        print("Installing Node dependencies...")
        self.run_cmd("npm install")

    def build_docker_image(self):
        print("Building client Docker image...")
        self.run_cmd(
            "docker build -t client-engine-dev -f cloud/Docker/client/client.Dockerfile client"
        )

    def launch_instance(self):
        if self.deploy_env == "cloud":
            print("Deploying client via gcloud build...")
            self.run_cmd(
                "gcloud builds submit client "
                "--tag gcr.io/$GOOGLE_CLOUD_PROJECT/client-dev-test:1.0.0"
            )
        else:
            print("Running client Docker container locally...")
            self.run_cmd(
                "docker run -p 8080:8080 client-engine-dev"
            )
