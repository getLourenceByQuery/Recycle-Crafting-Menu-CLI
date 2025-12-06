#♻️ Recycle Crafting Menu CLI
This project is a Command Line Interface (CLI) application built in Python that guides users through various crafting instructions using recycled household materials like plastic bottles, cardboard, glass jars, and more. It utilizes the powerful rich library to provide a clean, visually appealing, and organized terminal experience.

✨ Key Features
Material-Based Browsing: Users can browse crafting projects organized by the primary recyclable material (e.g., Plastic Bottle, Cardboard, Aluminum Can).

Product Search: A comprehensive search function allows users to find specific projects quickly by keyword (e.g., "Pencil Holder").

Detailed Instructions: Each project displays a clear, step-by-step guide, including a list of MATERIALS NEEDED and TOOLS NEEDED.

Admin Instruction Management (Login Required): Includes a secure administrative function (username: admin, password: 1234) that allows new crafting projects and instructions to be added and saved directly to the underlying products.json data file.

Rich CLI Experience: Leverages rich for professional terminal formatting, featuring custom panels, aligned text, colorful headings, and structured menus for improved usability.

Persistent Data Storage: Crafting instructions are stored and managed in a structured products.json file, ensuring data persists across application runs.

🛠️ Technology Stack
Language: Python 3

Primary Libraries:

rich: For enhanced console output, including panels, columns, rules, and advanced styling.

json: For reading and writing the structured crafting data.

getpass: For securely handling the admin password input.

🚀 How to Run
Clone the repository:

Bash

git clone [your-repo-link]
cd [your-repo-name]
Install the required libraries:

Bash

pip install rich
Run the application:

Bash

python final.py
