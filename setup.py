from setuptools import setup

setup(name='joke',
      version='0.1',
      description='The funniest joke in the world',
      url='http://github.com/adimitrova/joke',
      author='Anelia Dimitrova',
      author_email='joke@example.com',
      license='MIT',
      packages=['joke'],
      install_requires=[
          'markdown', 'tweepy', 'pyspark', 'pandas', 'boto3'
      ],
      zip_safe=False)
