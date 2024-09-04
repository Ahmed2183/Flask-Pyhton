from flaskBlog import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)

""" Description """

# Create a Virtual Environment: python -m venv .venv

# 2. If Virtual Environment Already Created: First Activate the Virtual Environment: .\.venv\Scripts\activate

# To run application directly using python: python run.py

# debug=True means run app in Debug Mode

# __name__ == '__main__':
""" 
Ye if wali condition check karti hai ke agar ye script directly run ho rahi hai (matlab, import nahi ho rahi dusri file se), 
toh app.run(debug=True) run ho otherwise if run.py kisi or file mai import horhi ho or us file ko directly run kra 
toh app.run(debug=True) run nh hoga sirf woi file run hogi
If you print(__name__):
If this file run.py directly run 'python run.py' then print output is __main__
If this file run.py import in another file and run that file like 'python another_file.py' then print output is run 
"""
