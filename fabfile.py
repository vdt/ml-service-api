from __future__ import with_statement
from fabric.api import local, lcd, run, env, cd, settings, prefix, sudo, shell_env
from fabric.contrib.console import confirm
from fabric.operations import put
from fabric.contrib.files import exists

env.hosts = ['vik@sandbox-service-api-001.m.edx.org']
#env.key_filename = ''

def prepare_deployment():
    local('git add -p && git commit')
    local("git push")

def deploy():
    code_dir = '/opt/wwc/ml-service-api'
    ml_code_dir = '/opt/wwc/machine-learning'
    up_one_level_dir = '/opt/wwc'
    database_dir = '/opt/wwc/db'
    remote_ssh_dir = '/home/vik/.ssh'
    local_dir = '/home/vik/mitx_all'
    nltk_data_dir = '/usr/share/nltk_data'

    sudo('sysctl vm.overcommit_memory=1')
    with lcd(local_dir), settings(warn_only=True):
        with cd(remote_ssh_dir):
            put('service-id_rsa','id_rsa', use_sudo=True)
            put('service-id_rsa.pub','id_rsa.pub', use_sudo=True)
            sudo('chmod 400 id_rsa')

    with settings(warn_only=True):
        sudo('service celery stop')
        sudo('service ml-service-api stop')
        repo_exists = exists(code_dir, use_sudo=True)
        if not repo_exists:
            sudo('apt-get install git python')
            up_one_level_exists = exists(up_one_level_dir, use_sudo=True)
            if not up_one_level_exists:
                sudo('mkdir {0}'.format(up_one_level_dir))
            with cd(up_one_level_dir):
                #TODO: Insert repo name here
                run('git clone git@github.com:VikParuchuri/service-api.git')
                sudo('mv service-api ml-service-api')

        ml_repo_exists = exists(ml_code_dir, use_sudo=True)
        if not ml_repo_exists:
            with cd(up_one_level_dir):
                run('git clone git@github.com:MITx/machine-learning.git')
        db_exists = exists(database_dir, use_sudo=True)
        if not db_exists:
            sudo('mkdir {0}'.format(database_dir))

        sudo('chown -R vik {0}'.format(up_one_level_dir))

    with cd(ml_code_dir), settings(warn_only=True):
        run('git pull')

    with cd(code_dir), settings(warn_only=True):
        # With git...
        run('git pull')
        run('sudo apt-get update')
        run('sudo apt-get upgrade gcc')
        sudo('xargs -a apt-packages.txt apt-get install')
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
        sudo('mkdir {0}'.format(nltk_data_dir))
        if not exists(nltk_data_dir):
            sudo('python -m nltk.downloader -d {0} all'.format(nltk_data_dir))
        sudo('chown -R vik {0}'.format(nltk_data_dir))

        with cd(code_dir):
            run('pip install -r requirements.txt')

            # With both
            run('python manage.py syncdb --settings=ml_service_api.aws --pythonpath={0}'.format(code_dir))
            run('python manage.py migrate --settings=ml_service_api.aws --pythonpath={0}'.format(code_dir))
            sudo('chown -R www-data {0}'.format(up_one_level_dir))

        with cd(ml_code_dir):
            sudo('xargs -a install/apt-packages.txt apt-get install')
            run('pip install -r install/pre-requirements.txt')
            run('pip install -r install/requirements.txt')

    with lcd(local_dir), settings(warn_only=True):
        with cd(up_one_level_dir):
            put('service-auth.json', 'auth.json', use_sudo=True)
            put('service-env.json', 'env.json', use_sudo=True)
        with cd('/etc/init'):
            put('service-celery.conf', 'celery.conf', use_sudo=True)
            put('service-ml-service-api.conf', 'ml-service-api.conf', use_sudo=True)
        with cd('/etc/nginx/sites-available'):
            put('service-nginx', 'default', use_sudo=True)

    sudo('service celery start')
    sudo('service ml-service-api start')
    sudo('service nginx restart')