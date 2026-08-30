from backend.ingestion.repo_loader import RepoLoader


loader = RepoLoader()


repo_url = input(
    "\nEnter GitHub repository URL: "
)


repo_path = loader.clone_repository(
    repo_url
)


print(
    f"\nRepository available at:"
    f"\n{repo_path}"
)