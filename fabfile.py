from __future__ import with_statement
from fabric.api import local, lcd, run, env, cd, settings, prefix, sudo, shell_env
from fabric.contrib.console import confirm
from fabric.operations import put

env.hosts = ['vik@sandbox-service-api-001.m.edx.org']
#env.key_filename = ''

def prepare_deployment():
    local('git add -p && git commit')
    local("git push")

def deploy():
    code_dir = '/opt/wwc/ml-service-api'
    up_one_level_dir = '/opt/wwc'
    remote_ssh_dir = '~/.ssh'
    local_dir = '~/mitx_all'
    with lcd(local_dir), settings(warn_only=True):
        with cd(remote_ssh_dir):
            put('service-id_rsa','id_rsa', use_sudo=True)
            put('service-id_rsa.pub','id_rsa.pub', use_sudo=True)

    with settings(warn_only=True):
        sudo('chown -R vik {0}'.format(up_one_level_dir))
        sudo('service celery stop')
        sudo('service ml-service-api stop')
    with cd(code_dir), settings(warn_only=True):
        # With git...
        run('git pull')
        run('sudo apt-get update')
        run('sudo apt-get upgrade gcc')
        run('sudo xargs -a apt-packages.txt apt-get install')
        result = run('source /opt/edx/bin/activate')
        if result.failed:
            sudo('apt-get install python-pip')
            sudo('pip install virtualenv')
            sudo('mkdir /opt/edx')
            sudo('virtualenv "/opt/edx"')
            sudo('chown -R vik /opt/edx')

    with prefix('source /opt/edx/bin/activate'), settings(warn_only=True):
        #sudo('apt-get build-dep python-scipy')
        run('pip install numpy')
        run('pip install scipy')

        with cd(code_dir):
            run('pip install -r requirements.txt')

            # With both
            run('python manage.py syncdb --settings=ml_service_api.aws --pythonpath={0}'.format(code_dir))
            run('python manage.py migrate --settings=ml_service_api.aws --pythonpath={0}'.format(code_dir))
            sudo('chown -R www-data {0}'.format(up_one_level_dir))

    with lcd(local_dir), settings(warn_only=True):
        with cd(up_one_level_dir):
            put('service-auth.json', 'auth.json', use_sudo=True)
            put('service-env.json', 'env.json', use_sudo=True)
        with cd('/etc/init'):
            put('service-celery.conf', 'celery.conf', use_sudo=True)
            put('service-ml-service-api.conf', 'ml-service-api.conf', use_sudo=True)

    sudo('service celery start')
    sudo('service ml-service-api start')