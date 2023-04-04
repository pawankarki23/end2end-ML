from setuptools import find_packages,setup
from typing import List
# '-e .' in the file requirements.txt is to just trigger the execution of setup.py.....we do not need to do anything with it...so remove it from the requirements list
# because of '-e .', the setup.py will execute itself and package will be built 

# pip install -r requirements.txt - command to setup the pre-requisites for a project



HYPEN_E_DOT='-e .'
def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements] # replace the \n at the end of the line with blank 

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements

setup(
name='mlproject',
version='0.0.1',
author='Pawan',
author_email='pawankarki5@gmail.com',
packages=find_packages(),
install_requires=get_requirements('requirements.txt')
)