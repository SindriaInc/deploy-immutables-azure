#!/usr/bin/env bash

source .env

# shellcheck disable=SC2046
docker run --rm -t --env IAC_MODE=${IAC_MODE} --env AZURE_SUBSCRIPTION_ID=${AZURE_SUBSCRIPTION_ID} --env AZURE_CLIENT_ID=${AZURE_CLIENT_ID} --env AZURE_SECRET=${AZURE_SECRET} --env AZURE_TENANT=${AZURE_TENANT} --env AZURE_RESOURCE_GROUP=${AZURE_RESOURCE_GROUP} --env AZURE_STORAGE_ACCOUNT=${AZURE_STORAGE_ACCOUNT} --env AZURE_STORAGE_ACCESS_KEY=${AZURE_STORAGE_ACCESS_KEY} --env AZURE_STORAGE_CONNECTION_STRING=${AZURE_STORAGE_CONNECTION_STRING} --env IAC_GIT_USERNAME=${IAC_GIT_USERNAME} --env IAC_GIT_PASSWORD=${IAC_GIT_PASSWORD} --env IAC_GIT_PROVIDER=${IAC_GIT_PROVIDER} --env IAC_GIT_NAMESPACE=${IAC_GIT_NAMESPACE} --env IAC_INFRA_NAME=${IAC_INFRA_NAME} --env IAC_LIVE_CACHE=${IAC_LIVE_CACHE} --env IAC_CURRENT_INFRA=${IAC_CURRENT_INFRA} --env IMMUTABLE_NAME=${IMMUTABLE_NAME} --env IMMUTABLE_REFER=${IMMUTABLE_REFER} --env IMMUTABLE_TYPE=${IMMUTABLE_TYPE} --env IMMUTABLE_BUNDLE=${IMMUTABLE_BUNDLE} --env IMMUTABLE_ZONE=${IMMUTABLE_ZONE} sindriainc/deploy-immutables-azure:1.1.0