from enum import Enum


class JobSource(str, Enum):
    gupy = 'gupy'


class JobLevel(str, Enum):
    junior = 'junior'
    pleno = 'pleno'
    senior = 'senior'
    estagio = 'estagio'
    trainee = 'trainee'


class WorkplaceType(str, Enum):
    remote = 'remote'
    hybrid = 'hybrid'
    on_site = 'on-site'


class Keyword(str, Enum):
    python = 'python'
    fastapi = 'fastapi'
    django = 'django'
    flask = 'flask'
    sqlalchemy = 'sqlalchemy'
    docker = 'docker'
    kubernetes = 'kubernetes'
    java = 'java'
    spring = 'spring'
    golang = 'golang'
    javascript = 'javascript'
    react = 'react'
    angular = 'angular'
    vue = 'vue'
    frontend = 'frontend'
    backend = 'backend'
