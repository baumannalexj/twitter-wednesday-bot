#!/bin/bash
set -e

cd ~/sideprojects/twitter-wednesday-bot

# 1. Create new directories
mkdir -p core/src \
  clients/src/aws \
  clients/src/twitter/responses \
  app_lambda_handler_isitwednesday_cron/src \
  app_lambda_handler_social_listener/src

# 2. Move files
mv src/core/* core/src/
mv src/clients/aws/* clients/src/aws/
mv src/clients/twitter/* clients/src/twitter/
mv src/clients/__init__.py clients/src/__init__.py
mv src/app_lambda_handler_isitwednesday_cron/* app_lambda_handler_isitwednesday_cron/src/
mv src/app_lambda_handler_social_listener/* app_lambda_handler_social_listener/src/

# 3. Add top-level __init__.py files
touch core/__init__.py clients/__init__.py \
  app_lambda_handler_isitwednesday_cron/__init__.py \
  app_lambda_handler_social_listener/__init__.py

# 4. Remove old src/ directory
rm -rf src/

# 5. Update imports

# core
sed -i '' 's/from src\.core/from core.src/g' core/src/tweet_builder.py

# clients
sed -i '' 's/from src\.clients\.twitter/from clients.src.twitter/g' clients/src/twitter/twitter_client.py
sed -i '' 's/from src\.clients\.twitter/from clients.src.twitter/g' clients/src/twitter/stream.py

# cron handler
sed -i '' 's/from src import is_wednesday_for_tz/from core.src.date_helper import is_wednesday_for_tz/g' app_lambda_handler_isitwednesday_cron/src/lambda_handler.py
sed -i '' 's/from src\.core/from core.src/g' app_lambda_handler_isitwednesday_cron/src/lambda_handler.py
sed -i '' 's/from src\.clients/from clients.src/g' app_lambda_handler_isitwednesday_cron/src/lambda_handler.py

# social listener handler
sed -i '' 's/from src\.core/from core.src/g' app_lambda_handler_social_listener/src/lambda_handler.py
sed -i '' 's/from src\.clients/from clients.src/g' app_lambda_handler_social_listener/src/lambda_handler.py

# fix self-referencing __init__.py imports
sed -i '' 's/from app_lambda_handler_isitwednesday_cron import/from src import/g' app_lambda_handler_isitwednesday_cron/src/__init__.py
sed -i '' 's/from app_lambda_handler_social_listener import/from src import/g' app_lambda_handler_social_listener/src/__init__.py

echo "Done! Review changes with: git diff --stat"
