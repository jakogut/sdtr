from setuptools import setup

setup(
        name='SDTR: Simulated Distance Target Renderer',
        version='1.0',
        description='Simulated Distance Target Renderer',
        author='Joseph Kogut',
        author_email='joseph.kogut@gmail.com',
        url='https://github.com/jakogut/sdtr.git',
        packages=['sdtr'],
        install_requires=[
            'opencv-python==3.1.0.3'
        ],
)
