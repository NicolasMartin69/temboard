import json
import re
import time

from urllib2 import HTTPError
from test.temboard import init_env, drop_env, rand_string, temboard_request
import test.configuration as cf
from test.spc import connector, error

ENV = {}
XSESSION = ''

class TestDashboard:

    @classmethod
    def setup_class(cls):
        global ENV
        ENV = init_env()

    @classmethod
    def teardown_class(cls):
        drop_env(ENV)

    def _temboard_login(self):
        (status, res) = temboard_request(
                ENV['g_ssl_cert_file_path'],
                method = 'POST',
                url = 'https://%s:%s/login' % (cf.G_HOST, cf.G_PORT),
                headers = {"Content-type": "application/json"},
                data = {'username': cf.G_USER, 'password': cf.G_PASSWORD})
        return json.loads(res)['session']

    def test_00_env_pg(self):
        """
        [dashboard] 00: PostgreSQL instance is up & running
        """
        conn = connector(
            host = ENV['pg_sockdir'],
            port = cf.PG_PORT,
            user = cf.PG_USER,
            password = cf.PG_PASSWORD,
            database = 'postgres'
        )
        try:
            conn.connect()
            conn.close()
            global XSESSION
            XSESSION = self._temboard_login()
            assert True
        except error as e:
            assert False

    def test_01_dashboard_ok(self):
        """
        [dashboard] 01: GET /dashboard : HTTP return code is 200 and the data structure is right
        """
        (status, res) = temboard_request(
                ENV['g_ssl_cert_file_path'],
                method = 'GET',
                url = 'https://%s:%s/dashboard' % (cf.G_HOST, cf.G_PORT),
                headers = {
                    "Content-type": "application/json",
                    "X-Session": XSESSION
                })

        dict_data = json.loads(res)
        assert status == 200 \
                and 'active_backends' in dict_data \
                and 'loadaverage' in dict_data \
                and 'os_version' in dict_data \
                and 'pg_version' in dict_data \
                and 'n_cpu' in dict_data \
                and 'hitratio' in dict_data \
                and 'databases' in dict_data \
                and 'memory' in dict_data \
                and 'hostname' in dict_data \
                and 'cpu' in dict_data \
                and 'buffers' in dict_data

    def test_02_dashboard_buffers_ok(self):
        """
        [dashboard] 02: GET /dashboard/buffers : HTTP return code is 200 and the data structure is right
        """
        (status, res) = temboard_request(
                ENV['g_ssl_cert_file_path'],
                method = 'GET',
                url = 'https://%s:%s/dashboard/buffers' % (cf.G_HOST, cf.G_PORT),
                headers = {
                    "Content-type": "application/json",
                    "X-Session": XSESSION
                })
 
        dict_data = json.loads(res)
        assert status == 200 \
                and 'buffers' in dict_data \
                    and 'nb' in dict_data['buffers'] \
                    and type(dict_data['buffers']['nb']) == int \
                    and 'time' in dict_data['buffers'] \
                    and type(dict_data['buffers']['time']) == float

    def test_03_dashboard_hitratio_ok(self):
        """
        [dashboard] 03: GET /dashboard/hitratio : HTTP return code is 200 and the data structure is right
        """
        (status, res) = temboard_request(
                ENV['g_ssl_cert_file_path'],
                method = 'GET',
                url = 'https://%s:%s/dashboard/hitratio' % (cf.G_HOST, cf.G_PORT),
                headers = {
                    "Content-type": "application/json",
                    "X-Session": XSESSION
                })

        dict_data = json.loads(res)
        assert status == 200 \
                and 'hitratio' in dict_data \
                and type(dict_data['hitratio']) == float

    def test_04_dashboard_active_backends_ok(self):
        """
        [dashboard] 04: GET /dashboard/active_backends : HTTP return code is 200 and the data structure is right
        """
        (status, res) = temboard_request(
                ENV['g_ssl_cert_file_path'],
                method = 'GET',
                url = 'https://%s:%s/dashboard/active_backends' % (cf.G_HOST, cf.G_PORT),
                headers = {
                    "Content-type": "application/json",
                    "X-Session": XSESSION
                })

        dict_data = json.loads(res)
   
        assert status == 200 \
                and 'active_backends' in dict_data \
                    and 'nb' in dict_data['active_backends'] \
                    and type(dict_data['active_backends']['nb']) == int \
                    and 'time' in dict_data['active_backends'] \
                    and type(dict_data['active_backends']['time']) == float

    def test_05_dashboard_cpu_ok(self):
        """
        [dashboard] 05: GET /dashboard/cpu : HTTP return code is 200 and the data structure is right
        """
        (status, res) = temboard_request(
                ENV['g_ssl_cert_file_path'],
                method = 'GET',
                url = 'https://%s:%s/dashboard/cpu' % (cf.G_HOST, cf.G_PORT),
                headers = {
                    "Content-type": "application/json",
                    "X-Session": XSESSION
                })

        dict_data = json.loads(res)
        assert status == 200 \
                and 'cpu' in dict_data \
                    and 'iowait' in dict_data['cpu'] \
                    and type(dict_data['cpu']['iowait']) == float \
                    and dict_data['cpu']['iowait'] >= 0 \
                    and dict_data['cpu']['iowait'] <= 100 \
                    and 'idle' in dict_data['cpu'] \
                    and type(dict_data['cpu']['idle']) == float \
                    and dict_data['cpu']['idle'] >= 0 \
                    and dict_data['cpu']['idle'] <= 100 \
                    and 'steal' in dict_data['cpu'] \
                    and type(dict_data['cpu']['steal']) == float \
                    and dict_data['cpu']['steal'] >= 0 \
                    and dict_data['cpu']['steal'] <= 100 \
                    and 'user' in dict_data['cpu'] \
                    and type(dict_data['cpu']['user']) == float \
                    and dict_data['cpu']['user'] >= 0 \
                    and dict_data['cpu']['user'] <= 100 \
                    and 'system' in dict_data['cpu'] \
                    and type(dict_data['cpu']['system']) == float \
                    and dict_data['cpu']['system'] >= 0 \
                    and dict_data['cpu']['system'] <= 100 \
                    and dict_data['cpu']['iowait'] + dict_data['cpu']['idle'] + dict_data['cpu']['steal'] + dict_data['cpu']['user'] + dict_data['cpu']['system'] >= 99.5 \
                    and dict_data['cpu']['iowait'] + dict_data['cpu']['idle'] + dict_data['cpu']['steal'] + dict_data['cpu']['user'] + dict_data['cpu']['system'] <= 100.5

    def test_06_dashboard_loadaverage_ok(self):
        """
        [dashboard] 06: GET /dashboard/loadaverage : HTTP return code is 200 and the data structure is right
        """
        (status, res) = temboard_request(
                ENV['g_ssl_cert_file_path'],
                method = 'GET',
                url = 'https://%s:%s/dashboard/loadaverage' % (cf.G_HOST, cf.G_PORT),
                headers = {
                    "Content-type": "application/json",
                    "X-Session": XSESSION
                })

        dict_data = json.loads(res)

        assert status == 200 \
                and 'loadaverage' in dict_data \
                and type(dict_data['loadaverage']) == float

    def test_07_dashboard_memory_ok(self):
        """
        [dashboard] 07: GET /dashboard/memory : HTTP return code is 200 and the data structure is right
        """
        (status, res) = temboard_request(
                ENV['g_ssl_cert_file_path'],
                method = 'GET',
                url = 'https://%s:%s/dashboard/memory' % (cf.G_HOST, cf.G_PORT),
                headers = {
                    "Content-type": "application/json",
                    "X-Session": XSESSION
                })

        dict_data = json.loads(res)

        assert status == 200 \
                and 'memory' in dict_data \
                    and 'total' in dict_data['memory'] \
                    and type(dict_data['memory']['total']) == int \
                    and 'active' in dict_data['memory'] \
                    and type(dict_data['memory']['active']) == float \
                    and dict_data['memory']['active'] >= 0 \
                    and dict_data['memory']['active'] <= 100 \
                    and 'cached' in dict_data['memory'] \
                    and type(dict_data['memory']['cached']) == float \
                    and dict_data['memory']['cached'] >= 0 \
                    and dict_data['memory']['cached'] <= 100 \
                    and 'free' in dict_data['memory'] \
                    and type(dict_data['memory']['free']) == float \
                    and dict_data['memory']['free'] >= 0 \
                    and dict_data['memory']['free'] <= 100 \
                    and dict_data['memory']['active'] + dict_data['memory']['cached'] + dict_data['memory']['free'] >= 99.5 \
                    and dict_data['memory']['active'] + dict_data['memory']['cached'] + dict_data['memory']['free'] <= 100.5

    def test_08_dashboard_hostname_ok(self):
        """
        [dashboard] 08: GET /dashboard/hostname : HTTP return code is 200 and the data structure is right
        """
        (status, res) = temboard_request(
                ENV['g_ssl_cert_file_path'],
                method = 'GET',
                url = 'https://%s:%s/dashboard/hostname' % (cf.G_HOST, cf.G_PORT),
                headers = {
                    "Content-type": "application/json",
                    "X-Session": XSESSION
                })

        dict_data = json.loads(res)

        assert status == 200 \
                and 'hostname' in dict_data \
                and type(dict_data['hostname']) == unicode

    def test_09_dashboard_os_version_ok(self):
        """
        [dashboard] 09: GET /dashboard/os_version : HTTP return code is 200 and the data structure is right
        """
        (status, res) = temboard_request(
                ENV['g_ssl_cert_file_path'],
                method = 'GET',
                url = 'https://%s:%s/dashboard/os_version' % (cf.G_HOST, cf.G_PORT),
                headers = {
                    "Content-type": "application/json",
                    "X-Session": XSESSION
                })

        dict_data = json.loads(res)

        assert status == 200 \
                and 'os_version' in dict_data \
                and type(dict_data['os_version']) == unicode

    def test_10_dashboard_databases_ok(self):
        """
        [dashboard] 10: GET /dashboard/databases : HTTP return code is 200 and the data structure is right
        """
        (status, res) = temboard_request(
                ENV['g_ssl_cert_file_path'],
                method = 'GET',
                url = 'https://%s:%s/dashboard/databases' % (cf.G_HOST, cf.G_PORT),
                headers = {
                    "Content-type": "application/json",
                    "X-Session": XSESSION
                })

        dict_data = json.loads(res)

        assert status == 200 \
                and 'databases' in dict_data \
                    and 'total_size' in dict_data['databases'] \
                    and type(dict_data['databases']['total_size']) == unicode \
                    and 'time' in dict_data['databases'] \
                    and type(dict_data['databases']['time']) == unicode \
                    and 'databases' in dict_data['databases'] \
                    and type(dict_data['databases']['databases']) == int \
                    and dict_data['databases']['databases'] >= 0 \
                    and 'total_commit' in dict_data['databases'] \
                    and type(dict_data['databases']['total_commit']) == int \
                    and 'total_rollback' in dict_data['databases'] \
                    and type(dict_data['databases']['total_rollback']) == int

    def test_11_dashboard_pg_version_ok(self):
        """
        [dashboard] 11: GET /dashboard/pg_version : HTTP return code is 200 and the data structure is right
        """
        (status, res) = temboard_request(
                ENV['g_ssl_cert_file_path'],
                method = 'GET',
                url = 'https://%s:%s/dashboard/pg_version' % (cf.G_HOST, cf.G_PORT),
                headers = {
                    "Content-type": "application/json",
                    "X-Session": XSESSION
                })

        dict_data = json.loads(res)

        assert status == 200 \
                and 'pg_version' in dict_data \
                and type(dict_data['pg_version']) == unicode

    def test_12_dashboard_n_cpu_ok(self):
        """
        [dashboard] 12: GET /dashboard/n_cpu : HTTP return code is 200 and the data structure is right
        """
        (status, res) = temboard_request(
                ENV['g_ssl_cert_file_path'],
                method = 'GET',
                url = 'https://%s:%s/dashboard/n_cpu' % (cf.G_HOST, cf.G_PORT),
                headers = {
                    "Content-type": "application/json",
                    "X-Session": XSESSION
                })

        dict_data = json.loads(res)

        assert status == 200 \
                and 'n_cpu' in dict_data \
                and type(dict_data['n_cpu']) == int
