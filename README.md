git clone https://github.com/<your-username>/notesappmulti-tenant.git
cd notesappmulti-tenant

2.Create an Environment
python -m venv .venv

.\.venv\Scripts\activate   # Windows

source .venv/bin/activate  # macOS/Linux

3.Install Dependencies

pip install -r requirements.txt

4. Install MongoDB Community Server

Download from MongoDB Community Download Center

Choose Windows → msi → install with defaults

During setup, enable “Run as a Service”

After installation MongoDB will start automatically.

5. Configure Your Environment Variables

Create a file named .env in your project root (same level as Dockerfile and requirements.txt):

MONGODB_URI=mongodb://localhost:27017

DB_NAME=notes_multi_tenant

HEADER_ORG=X-Org-ID


HEADER_USER=X-User-ID

MONGODB_URI points to your local Mongo service

OR

You get org_id when creating an organization

You get user_id when creating a user inside that organization



The two header variables are used for tenant/user identification

6.open localhost:8000/docs for api endpoint
