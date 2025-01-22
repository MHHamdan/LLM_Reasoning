{\rtf1\ansi\ansicpg1252\cocoartf2761
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx566\tx1133\tx1700\tx2267\tx2834\tx3401\tx3968\tx4535\tx5102\tx5669\tx6236\tx6803\pardirnatural\partightenfactor0

\f0\fs24 \cf0 from alembic import context\
from sqlalchemy import engine_from_config, pool\
from logging.config import fileConfig\
import os\
import sys\
from dotenv import load_dotenv\
\
# Load environment variables\
load_dotenv()\
\
# Add parent directory to path\
sys.path.append(os.path.dirname(os.path.dirname(__file__)))\
\
# Import your models\
from database import Base\
\
# This is the Alembic Config object\
config = context.config\
\
# Configure logging\
fileConfig(config.config_file_name)\
\
# Set database URL\
config.set_main_option('sqlalchemy.url', os.getenv('DATABASE_URL'))\
\
target_metadata = Base.metadata\
\
def run_migrations_online():\
    connectable = engine_from_config(\
        config.get_section(config.config_ini_section),\
        prefix='sqlalchemy.',\
        poolclass=pool.NullPool,\
    )\
\
    with connectable.connect() as connection:\
        context.configure(\
            connection=connection,\
            target_metadata=target_metadata\
        )\
\
        with context.begin_transaction():\
            context.run_migrations()\
\
if context.is_offline_mode():\
    run_migrations_offline()\
else:\
    run_migrations_online()\
\
}