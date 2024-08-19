from flaskBlog import app

if __name__ == '__main__':
    app.run(debug=True)

""" Description """

# Create a Virtual Environment: python -m venv .venv

# 2. If Virtual Environment Already Created: First Activate the Virtual Environment: .\.venv\Scripts\activate

# To run application directly using python: python run.py

# debug=True means run app in Debug Mode

# __name__ == '__main__':
""" 
Ye if wali condition check karti hai ke agar ye script directly run ho rahi hai (matlab, import nahi ho rahi dusri file se), 
toh app.run(debug=True) run ho otherwise python flaskBlog.py command not work
"""
