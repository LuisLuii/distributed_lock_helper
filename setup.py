from setuptools import setup, find_packages


print("""

- upload
    - build wheel: python setup.py bdist_wheel
    - upload to server: python setup.py sdist upload -r internal

- download
    - Just pip install <package>

""")

if __name__ == '__main__':
    packageName ='distrilockper'
    try:
        with open("requirements.txt", 'r') as file:
            requirement = [req.rstrip().replace("==", "==") for req in file.readlines()]
    except Exception as e:
        with open("{}.egg-info/requires.txt".format(packageName), 'r') as file:
            requirement = [req.rstrip() for req in file.readlines()]
        pass
    setup(
        name=packageName,
        version='0.0.1-Alpha-03',
        description='Distributed Lock with using Redis',
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        author='Louis Lui',
        author_email='wilsom20012@gmail.com',
        url='https://gitlab.com/wilsom20012/distributed_lock_helper',
        license="MIT License",
        packages=find_packages(),
        # packages=find_packages(
        #     exclude='testcase,playground,ReadMe.md,play_lock,requirements.txt'.format(packageName).split(',')),
        # package_dir={'': ''},
        setup_requires=["setuptools>=31.6.0"],
        classifiers=[
            "Development Status :: 2 - Pre-Alpha",
            "Environment :: Console",
            "Intended Audience :: Developers",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 3",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Topic :: System :: Software Distribution",
        ],
        include_package_data=True,
        keywords=['Lock','Distributed'],
        install_requires = requirement,
    )