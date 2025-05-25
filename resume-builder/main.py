import yaml
from generate_pdfs import save_as_pdf

def load_resume_skeleton(file_path="resume_skeleton.yaml"):
    """Load the resume skeleton from a YAML file."""
    with open(file_path, "r") as file:
        return yaml.safe_load(file)

def main():

    # Step 1: Load Resume Skeleton
    resume_skeleton = load_resume_skeleton()

    save_as_pdf(resume_skeleton, pdf_file="resume.pdf")
    
if __name__ == "__main__":
    main()
