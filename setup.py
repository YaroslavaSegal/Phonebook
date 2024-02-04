from setuptools import setup, find_packages

setup(name='Phonebook',
      version='0.0.1',
      description='Console bot for work with phone book',
      url="https://github.com/YaroslavaSegal/Phonebook",
      author='Yaroslava_Segal',
      author_email='yaroslavasiehal@gmail.com',
      license='MIT',
      packages=find_packages(),
      entry_points={'console_scripts': ['Phonebook = Phonebook.main:main']},
      zip_safe=False)
