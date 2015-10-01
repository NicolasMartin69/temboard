from setuptools import setup

requires = [ 'tornado>=3.2' ]

setup(
    name = 'ganesh',
    version = '0.0.1',
    author = 'Julien Tachoires',
    license = 'Postgresql',
    packages = ['ganeshwebui', 'ganeshwebui.handlers'],
    scripts = ['ganesh-web-client'],
    include_package_data=True,
    zip_safe=False,
    url = '',
    description = 'PostgreSQL Administration & Monitoring web client.',
    data_files = [('/usr/share/ganesh/', [
            'share/ganesh.conf.sample',
            'share/ssl/ganesh_CHANGEME.pem',
            'share/ssl/ganesh_CHANGEME.key',
            'share/ssl/ca_certs.pem']
    )]
)